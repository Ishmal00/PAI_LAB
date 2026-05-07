import numpy as np
import faiss
from flask import Flask, render_template, request, jsonify
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

# 1. Dataset (Questions and Answers)
qa_data = [
    {"q": "What is minimalist style?", "a": "Minimalist style is about neutral colors like white, beige, and black with clean, simple lines."},
    {"q": "How to look vintage?", "a": "For a vintage look, try 90s denim, oversized sweaters, and retro patterns from Pinterest."},
    {"q": "Suggest a streetwear outfit.", "a": "Streetwear is all about comfort: oversized hoodies, cargo pants, and chunky sneakers."},
    {"q": "What is the aesthetic vibe?", "a": "The aesthetic vibe focuses on pastels, soft lighting, and Y2K inspired accessories."},
    {"q": "What should I wear to a formal event?", "a": "A sharp blazer with tailored trousers or a sleek midi dress is perfect for formal occasions."},
    {"q": "How to style a party look?", "a": "Go for sequins, bold colors, and statement jewelry to stand out at any party."}
]

questions = [item["q"] for item in qa_data]
answers = [item["a"] for item in qa_data]

# 2. Initialize Model (Hugging Face MiniLM)
model = SentenceTransformer('all-MiniLM-L6-v2')

# 3. Create Embeddings and FAISS Index
question_embeddings = model.encode(questions)
dimension = question_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(question_embeddings).astype('float32'))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask_bot():
    user_query = request.json.get("text")
    
    # User query ko embedding mein convert karna
    query_embedding = model.encode([user_query])
    
    # FAISS search (find the closest match)
    D, I = index.search(np.array(query_embedding).astype('float32'), k=1)
    
    # Agar match acha hai toh answer dena, warna default
    if D[0][0] < 1.5:  # Similarity threshold
        reply = answers[I[0][0]]
    else:
        reply = "I'm not sure about that specific vibe, but I can help with Minimalist, Vintage, or Streetwear!"
        
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)