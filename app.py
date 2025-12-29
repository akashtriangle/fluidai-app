import requests
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

tasks = {}  
next_id = 1 
done_count = 0 
GEMINI_KEY = "AIzaSyCQ7fy6DQSvOPD5hr8YezklumjpV9E2Xy8"

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

@app.route("/add", methods=["POST"])
def add():
    global next_id
    title = request.form.get("title")
    if title:
        tasks[next_id] = title
        next_id += 1
    return redirect("/")

@app.route("/ai/<task_text>")
def ai_help(task_text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    payload = {"contents": [{"parts": [{"text": f"Give a short 1-sentence pro-tip for: {task_text}"}]}]}
    
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        answer = data['candidates'][0]['content']['parts'][0]['text']
    except:
        answer = "Unsuccessful call, please try later"
    return f"<html><body style='font-family:sans-serif;padding:50px;'><h2>AI Tip for: {task_text}</h2><p>{answer}</p></body></html>"

@app.route("/done/<int:tid>", methods=["POST"])
def done(tid):
    global done_count
    if tid in tasks:
        tasks.pop(tid)
        done_count += 1
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)