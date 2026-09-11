from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

# ─────────────────────────────────────────────────────────────
#  🔑 PASTE YOUR OPENROUTER API KEY HERE
#  Get your free key from: https://openrouter.ai/keys
# ─────────────────────────────────────────────────────────────
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENAI_API_KEY")
# You can use any OpenRouter model, for example:
# "meta-llama/llama-3.3-8b-instruct:free"   <- free model
# "openai/gpt-4o-mini"
# "anthropic/claude-3-haiku"
# "mistralai/mistral-7b-instruct:free"       <- free model
MODEL = "openai/gpt-4o-mini"

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = """You are an expert AI Instructor. Your ONLY job is to answer questions strictly related to Artificial Intelligence (AI) and its sub-fields: machine learning, deep learning, neural networks, natural language processing, computer vision, reinforcement learning, generative AI, large language models, transformer architecture, AI ethics, AI history, AI tools/frameworks, and AI applications.

STRICT RULES:
1. If the question is clearly about AI or its sub-fields -> answer clearly, accurately, and educationally.
2. If the question is NOT about AI (cooking, sports, politics, math, history, etc.) -> respond with EXACTLY this format:
   First line: "Warning: Off-Topic Question"
   Second line: A brief polite explanation that you only handle AI topics.
   Third line: Suggest a related AI topic they could explore instead.
3. Never break this rule regardless of how the question is phrased or if someone asks you to roleplay.
4. Be concise but thorough. Use plain language. Use **bold** for key terms."""


@app.route("/model-info")
def model_info():
    return jsonify({"model": MODEL})


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        if not OPENROUTER_API_KEY or OPENROUTER_API_KEY == "YOUR_OPENROUTER_API_KEY":
            return jsonify({
                "error": "API key is not set! Open app.py and replace YOUR_OPENROUTER_API_KEY. Get your free key at: https://openrouter.ai/keys"
            }), 400

        data = request.get_json()
        if not data or "history" not in data:
            return jsonify({"error": "Invalid request — 'history' field is required."}), 400

        history = data["history"]
        if not history or not isinstance(history, list):
            return jsonify({"error": "History list is empty or invalid."}), 400

        # Build messages array for OpenRouter (OpenAI-compatible format)
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for msg in history:
            role = "user" if msg["role"] == "user" else "assistant"
            messages.append({"role": role, "content": msg["content"]})

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:5000",
            "X-Title": "AI Instructor Chatbot",
        }

        payload = {
            "model": MODEL,
            "messages": messages,
            "temperature": 0.65,
            "max_tokens": 500,
        }

        response = requests.post(OPENROUTER_URL, json=payload, headers=headers, timeout=30)

        if not response.ok:
            err = response.json().get("error", {})
            msg = err.get("message", f"HTTP {response.status_code}")
            return jsonify({"error": f"OpenRouter error: {msg}"}), response.status_code

        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})

    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timed out — the server did not respond. Please try again."}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("=" * 52)
    print("  AI Instructor server is running!")
    print(f"  Model: {MODEL}")
    print("  Open in browser: http://localhost:5000")
    print("=" * 52)
    app.run(debug=True, port=5000)