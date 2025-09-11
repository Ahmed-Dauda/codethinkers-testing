from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from django.conf import settings  # if you’re mixing with Django settings

# ✅ Create a client instance with API key
client = OpenAI(api_key=settings.OPENAI_API_KEY)

app = FastAPI()

class CodeRequest(BaseModel):
    html: str
    css: str
    js: str
    prompt: str

@app.post("/api/generate")
async def generate_code(req: CodeRequest):
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": "You are an expert web developer. Only return JSON with html, css, js."},
            {"role": "user", "content": f"""
            Current project:
            HTML: {req.html}
            CSS: {req.css}
            JS: {req.js}

            User request:
            {req.prompt}
            """}
        ]
    )

    ai_text = response.choices[0].message.content.strip()
    return {
        "html": req.html,
        "css": req.css,
        "js": req.js,
        "ai_text": ai_text
    }
