import os
import requests
from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv  # 1. Import the loader

# 2. Load the variables from the .env file
load_dotenv()

app = Flask(__name__)

tasks = {}  
next_id = 1 
done_count = 0 

# 3. Get the key from the environment instead of hardcoding it
GEMINI_KEY = os.getenv("GEMINI_KEY")

@app.route("/")
def home():
    global done_count
    if not tasks:
        done_count = 0
        progress = 0
    else:
        total = len(tasks) + done_count
        progress = int((done_count / total) * 100)
    return render_template("index.html", tasks=tasks, progress=progress)

# ... [Keep your /add and /done routes as they were] ...

@app.route("/ai/<task_text>")
def ai_help(task_text):
    # Use the model name from your discovery list (e.g., gemini-2.0-flash)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_KEY}"
    payload = {"contents": [{"parts": [{"text": f"Give a short 1-sentence pro-tip for: {task_text}"}]}]}
    
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        answer = data['candidates'][0]['content']['parts'][0]['text']
    except:
        answer = "Stay focused and take it one step at a time!"
        
    return f"<html><body style='font-family:sans-serif;padding:50px;'><h2>AI Tip for: {task_text}</h2><p>{answer}</p></body></html>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
