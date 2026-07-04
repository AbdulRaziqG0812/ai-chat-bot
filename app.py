from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("GROQ_API_KEY")

API_URL = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    # 1. Frontend se puri messages ki list (history) lein
    history = request.json.get("messages", [])

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": history,  # 2. Ab hum puri history bhej rahe hain
        "temperature": 0.7
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    print("\n===== GROQ DEBUG =====")
    print("STATUS:", response.status_code)
    print("======================\n")

    data = response.json()

    if response.status_code != 200:
        return jsonify({"reply": "API Error: " + str(data)})

    try:
        reply = data["choices"][0]["message"]["content"]
    except Exception as e:
        print("PARSE ERROR:", e)
        reply = "Sorry, I couldn't process that."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)