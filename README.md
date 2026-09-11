# 🤖 AI Instructor Chatbot
**Python Flask backend + HTML/CSS/JS frontend**
Powered by **OpenRouter** (use any LLM model!)

---

## 📁 Project Structure

```
ai-instructor/
├── app.py                ← Python Flask backend
├── requirements.txt      ← Python dependencies
├── templates/
│   └── index.html        ← Frontend (HTML / CSS / JS)
└── README.md
```

---

## ⚙️ Setup — 3 Aasaan Steps

### Step 1 — Dependencies install karo
```bash
pip install -r requirements.txt
```

### Step 2 — OpenRouter API Key daalo
`app.py` mein yeh line dhundho:
```python
OPENROUTER_API_KEY = "YOUR_OPENROUTER_API_KEY"
```
Key yahan se FREE mein lo: https://openrouter.ai/keys

### Step 3 — Server chalao
```bash
python app.py
```
Browser mein kholo → **http://localhost:5000**

---

## 🧠 Model Change Karna

`app.py` mein `MODEL` variable update karo:

| Model                                      | Cost       |
|--------------------------------------------|------------|
| `meta-llama/llama-3.3-8b-instruct:free`    | ✅ Free    |
| `mistralai/mistral-7b-instruct:free`        | ✅ Free    |
| `openai/gpt-4o-mini`                        | 💰 Paid    |
| `anthropic/claude-3-haiku`                  | 💰 Paid    |
| `google/gemini-flash-1.5`                   | 💰 Paid    |

Saare models dekhne ke liye: https://openrouter.ai/models

---

## 🔗 API Endpoints

| Method | URL           | Description                    |
|--------|---------------|--------------------------------|
| GET    | `/`           | Frontend serve karta hai       |
| POST   | `/chat`       | OpenRouter se reply leta hai   |
| GET    | `/model-info` | Current model naam return karta hai |

### POST /chat — Request
```json
{
  "history": [
    { "role": "user", "content": "What is machine learning?" }
  ]
}
```

### POST /chat — Response
```json
{
  "reply": "Machine learning is..."
}
```

---

## ✅ Features
- Sirf AI topics par jawab deta hai
- Off-topic sawaal ko politely reject karta hai ⚠️
- Multi-turn conversation (full history)
- Koi bhi OpenRouter model use kar sakte ho
- Clean light UI with topic chips
