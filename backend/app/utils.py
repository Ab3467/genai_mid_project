import os
import json
import requests # type: ignore
from dotenv import load_dotenv # pyright: ignore[reportMissingImports]
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise ValueError("❌ OPENROUTER_API_KEY not found in .env")

MODEL_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "HTTP-Referer": "http://localhost:5173",  # REQUIRED
    "X-Title": "AI Code Reviewer",            # REQUIRED
    "Content-Type": "application/json",
}

def call_llm_and_parse_json(system_prompt: str, user_prompt: str):
    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 600
    }

    res = requests.post(MODEL_URL, headers=HEADERS, json=payload)

    if res.status_code != 200:
        print("🔥 API error:", res.text)
        raise ValueError(f"OpenRouter API Error {res.status_code}: {res.text}")

    text = res.json()["choices"][0]["message"]["content"]

    # Extract JSON
    try:
        return json.loads(text)
    except:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            return json.loads(text[start:end+1])
        raise ValueError(f"⚠ Model returned non-JSON:\n{text}")
