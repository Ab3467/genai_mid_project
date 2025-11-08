import os
import json
import requests
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise ValueError("❌ OPENROUTER_API_KEY not found in .env")

MODEL_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def call_llm_and_parse_json(system_prompt: str, user_prompt: str):
    """
    Calls OpenRouter API and parses JSON output from a model.
    """
    payload = {
        "model": "mistralai/mistral-7b-instruct",  # ✅ free model
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 600
    }

    response = requests.post(MODEL_URL, headers=HEADERS, json=payload)
    if response.status_code != 200:
        print("🔥 API error:", response.text)
        raise ValueError(f"OpenRouter API Error {response.status_code}: {response.text}")

    data = response.json()
    text = data["choices"][0]["message"]["content"]

    try:
        return json.loads(text)
    except Exception:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            try:
                return json.loads(text[start:end+1])
            except Exception:
                pass
        raise ValueError(f"⚠️ Model returned non-JSON:\n{text}")
