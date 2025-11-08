import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pathlib import Path

from .prompts import SYSTEM_PROMPT, make_user_prompt
from .utils import call_llm_and_parse_json

# ✅ Load .env file explicitly
env_path = Path(__file__).resolve().parent.parent / ".env"

if load_dotenv(dotenv_path=env_path):
    print("✅ .env file loaded successfully!")
else:
    print("⚠️ .env file not found or not loaded!")

print("🔑 Loaded OPENROUTER_API_KEY:", os.getenv("OPENROUTER_API_KEY"))

app = FastAPI(title="AI Code Reviewer")

# ✅ Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Request model
class ReviewRequest(BaseModel):
    code: str
    language: str = "python"
    depth: str = "quick"
    context: Optional[str] = None


# ✅ Health check
@app.get("/health")
async def health():
    return {"status": "ok"}


# ✅ Code review endpoint
@app.post("/review")
async def review(req: ReviewRequest):
    print("📩 Incoming request:", req.dict())

    if not os.environ.get("OPENROUTER_API_KEY"):
        print("❌ API key missing!")
        raise HTTPException(status_code=500, detail="OPENROUTER_API_KEY not set on server")

    if not req.code or not req.language:
        raise HTTPException(status_code=400, detail="code and language are required")

    user_prompt = make_user_prompt(req.code, req.language, req.depth, req.context)
    print("🧠 Prompt prepared successfully")

    try:
        parsed = call_llm_and_parse_json(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )
        print("✅ LLM responded successfully")
        return {"ok": True, "review": parsed}

    except ValueError as e:
        print("⚠️ JSON parse error:", e)
        return {"ok": False, "error": str(e)}

    except Exception as e:
        print("🔥 Backend error:", e)
        raise HTTPException(status_code=500, detail=str(e))
