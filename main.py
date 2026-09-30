from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import google.generativeai as genai
import os
from dotenv import load_dotenv

# API Key Setup
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

app = FastAPI(title="EduGenie")

# --- HTML & CSS in a single variable ---
# (Ithukku index.html matrum style.css thevai illai)
HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head>
    <title>EduGenie - AI Assistant</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f4f8; text-align: center; padding: 40px; }
        .card { background: white; max-width: 600px; margin: 0 auto; padding: 30px; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        input { padding: 12px; width: 65%; border: 1px solid #ccc; border-radius: 5px; font-size: 16px; }
        button { padding: 12px 20px; background-color: #3b82f6; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        button:hover { background-color: #2563eb; }
        .output { margin-top: 20px; padding: 15px; background: #e5e7eb; border-radius: 8px; text-align: left; }
    </style>
</head>
<body>
    <h1>Welcome to EduGenie 🧠✨</h1>
    <p>Your personal AI tutor for learning support!</p>
    
    <div class="card">
        <h3>Ask EduGenie a Question:</h3>
        <input type="text" id="question" placeholder="Why is the sky blue?">
        <button onclick="getAnswer()">Get Answer</button>
        <div id="result" class="output" style="display: none;"></div>
    </div>

    <script>
        async function getAnswer() {
            const q = document.getElementById('question').value;
            const resultDiv = document.getElementById('result');
            resultDiv.style.display = 'block';
            resultDiv.innerHTML = "<b>Loading... Please wait...</b>";
            
            const response = await fetch('/qa?question=' + encodeURIComponent(q));
            const data = await response.json();
            resultDiv.innerHTML = "<b>Answer:</b><br><br>" + data.answer;
        }
    </script>
</body>
</html>
"""

# 1. Direct HTML Response (No folders needed)
@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML_CONTENT

# QnA API (Fixed latest model)
@app.get("/qa")
async def answer_question(question: str = Query(...)):
    try:
        # Error varama irukka Google sonna latest model-ah direct-a kudukkurom
        model = genai.GenerativeModel("gemini-3.8-flash")
        
        response = model.generate_content(question)
        return {"answer": response.text.strip()}
    except Exception as e:
        return {"answer": f"⚠️ Error: {e}"}