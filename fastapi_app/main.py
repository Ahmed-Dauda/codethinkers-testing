from fastapi import FastAPI
from pydantic import BaseModel
import asyncio

app = FastAPI()

class AIRequest(BaseModel):
    prompt: str

# Simulate AI task with async processing
@app.post("/ai/generate")
async def generate_ai(req: AIRequest):
    await asyncio.sleep(1)  # simulate async heavy task
    # Example output (can store in DB here)
    return {"html": f"<h1>{req.prompt}</h1>", "css": "h1 {color:blue;}", "js": "console.log('done');"}
