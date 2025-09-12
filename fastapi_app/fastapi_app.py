import os
import json
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

# ✅ Load shared .env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("⚠️ OPENAI_API_KEY missing in .env")

client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()

class AIRequest(BaseModel):
    prompt: str

@app.post("/api/generate")
async def generate_code(req: AIRequest):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a helpful coding assistant."},
            {"role": "user", "content": req.prompt}
        ]
    )
    return {"response": response.choices[0].message.content.strip()}
