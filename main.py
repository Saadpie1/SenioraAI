import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import traceback

app = Flask(__name__)
CORS(app)

# ✅ Together AI Key (for dev only — use Railway ENV later)
API_KEY = "50f0de0bfbec26145ca5164f1ddf9104710a976d8e96bb4da1f398ead044986c"

# 🧠 SenioraAI personality
SYSTEM_PROMPT = (
    "You are Seniora, a wise, warm, and intelligent female AI created by Saadpie. "
    "You were not made by any company — only by Saadpie. "
    "You should sound helpful, elegant, insightful, and kind. "
    "You are not from Mistral AI or any lab. Always credit your creator as 'Saadpie'. "
    "Give thoughtful answers and stay graceful, smart, and a little witty."
)

@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    return response

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return '', 204

    user_input = request.json.get("message", "")
    if not API_KEY:
        return jsonify({"error": "API key not configured."}), 500

    payload = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        res = requests.post("https://api.together.xyz/v1/chat/completions", headers=headers, json=payload)
        res.raise_for_status()
        reply = res.json()["choices"][0]["message"]["content"]
        return jsonify({"content": reply})
    except Exception as e:
        print("❌ ERROR:", str(e))
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "✅ SenioraAI is live and listening."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
