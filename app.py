import os
import uuid
import json
import pdfplumber
import docx
import chromadb

from google import genai
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

# =========================================
#              Configuration
# =========================================
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

client = genai.Client(api_key=API_KEY)
#MODEL_ID = "gemini-2.0-flash-lite" 
MODEL_ID = "gemini-2.5-flash" 
# أو يمكنك استخدام "gemini-flash-latest"

EMBEDDER = SentenceTransformer("all-MiniLM-L6-v2")

# =========================================
#              Flask Setup
# =========================================
app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="documents")


# =========================================
#           Helper Functions
# =========================================
def extract_text(path):
    ext = path.split(".")[-1].lower()
    try:
        if ext == "pdf":
            with pdfplumber.open(path) as pdf:
                return "".join([p.extract_text() or "" for p in pdf.pages])
        if ext == "docx":
            doc = docx.Document(path)
            return "\n".join([p.text for p in doc.paragraphs])
        if ext == "txt":
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
    except Exception as e:
        print(f"Error extracting text: {e}")
    return ""


def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=100)
    return splitter.split_text(text)


def generate_text(prompt):
    try:
        response = client.models.generate_content(model=MODEL_ID, contents=prompt)
        return response.text if response.text else "No text generated."
    except Exception as e:
        print(f"Error generating text: {e}")
        return f"Error generating response: {str(e)}"


# =========================================
#                Routes
# =========================================
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    try:
        file = request.files.get("file")
        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        text = extract_text(file_path)
        if not text.strip():
            return jsonify({"error": "Could not extract text from file"}), 400

        chunks = chunk_text(text)
        embeddings = EMBEDDER.encode(chunks).tolist()
        ids = [str(uuid.uuid4()) for _ in chunks]
        collection.add(embeddings=embeddings, documents=chunks, ids=ids)

        summary_prompt = f"""
        Read the following text carefully and provide a comprehensive, well-structured summary.
        Use clear bullet points with emoji icons for each key point.
        Make it informative and easy to read.

        Text:
        {text[:4000]}

        Format:
        ## Document Summary

        * [key point 1]
        * [key point 2]
        * [key point 3]
        ... (as many as needed)


        ## Main Topics
        [list the main topics covered]
        """
        summary = generate_text(summary_prompt)

        mcq_prompt = f"""
        Based on the following text, generate exactly 10 multiple choice questions.
        Return ONLY a valid JSON array. No extra text, no markdown, no explanation.

        Text:
        {text[:4000]}

        Return this exact JSON format:
        [
          {{
            "question": "Question text here?",
            "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
            "correct": "A",
            "explanation": "Brief explanation why this is correct"
          }}
        ]
        """
        mcq_raw = generate_text(mcq_prompt)

        mcqs = []
        try:
            clean = mcq_raw.strip()
            if "```json" in clean:
                clean = clean.split("```json")[1].split("```")[0].strip()
            elif "```" in clean:
                clean = clean.split("```")[1].split("```")[0].strip()
            mcqs = json.loads(clean)
        except Exception as e:
            print(f"Error parsing MCQs: {e}")
            mcqs = []

        return jsonify({
            "status": "success",
            "summary": summary,
            "mcqs": mcqs,
            "filename": file.filename,
            "chunks_count": len(chunks)
        })

    except Exception as e:
        print(f"Error in upload: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.json
        question = data.get("question")
        if not question:
            return jsonify({"error": "Question is required"}), 400

        query_embedding = EMBEDDER.encode([question]).tolist()
        results = collection.query(query_embeddings=query_embedding, n_results=3)

        if not results.get("documents") or not results["documents"][0]:
            return jsonify({"answer": "No relevant information found in the document."})

        context = "\n".join(results["documents"][0])

        prompt = f"""
        Use ONLY the following context to answer the question accurately and concisely.
        If the answer is not in the context, say "This information is not available in the document."

        Context:
        {context}

        Question: {question}

        Answer:
        """

        answer = generate_text(prompt).strip()
        return jsonify({"answer": answer})

    except Exception as e:
        print(f"Error in ask: {e}")
        return jsonify({"answer": "An error occurred while processing your question."}), 500


# =========================================
#             Run App
# =========================================
if __name__ == "__main__":
    print("App running on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)