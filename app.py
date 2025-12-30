import os
import requests
from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv

# Try to load .env file if it exists (local development)
load_dotenv()

app = Flask(__name__)

tasks = {}  
next_id = 1 
done_count = 0 

# This works locally (via .env) AND on GitHub (via Secrets)
GEMINI_KEY = os.getenv("GEMINI_KEY")

@app.route("/")
def home():
    global done_count
    total = len(tasks) + done_count
    progress = int((done_count / total) * 100) if total > 0 else 0
    return render_template("index.html", tasks=tasks, progress=progress)

# ... [add and done routes remain the same] ...

@app.route("/ai/<task_text>")
def ai_help(task_text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"
    payload = {"contents": [{"parts": [{"text": f"Give a short 1-sentence pro-tip for: {task_text}"}]}]}
    
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        answer = data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        # If key is missing or API fails, we give a friendly fallback
        answer = "Unsuccesful, try again later"
        
    return f"<html><body style='font-family:sans-serif;padding:50px;'><h2>AI Tip for: {task_text}</h2><p>{answer}</p></body></html>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)

