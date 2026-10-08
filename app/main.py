from fastapi import FastAPI
from pydantic import BaseModel
from app.summarizer import summarize

app = FastAPI(title="AI Summarizer API")


class SummarizeRequest(BaseModel):
    text: str


class SummarizeResponse(BaseModel):
    summary: str


@app.get("/")
def root():
    return {"service": "ai-summarizer-api", "status": "running"}


@app.post("/summarize", response_model=SummarizeResponse)
def summarize_endpoint(payload: SummarizeRequest):
    return SummarizeResponse(summary=summarize(payload.text))