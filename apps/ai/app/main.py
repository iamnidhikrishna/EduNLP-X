from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="EduNLP-X AI")

@app.get("/health")
def health():
    return {"status":"ok","service":"fastapi-ai"}

class Prompt(BaseModel):
    text: str

@app.post("/infer")
def infer(p: Prompt):
    # placeholder inference
    return {"answer": f"Echo: {p.text}"}
