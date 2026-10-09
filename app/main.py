from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.summarizer import summarize

app = FastAPI(title="AI Summarizer API")

MAX_TEXT_LENGTH = 5000


class SummarizeRequest(BaseModel):
    text: str = Field(..., description="Text to summarize")


class SummarizeResponse(BaseModel):
    summary: str


class ErrorResponse(BaseModel):
    error: str
    detail: str


@app.get("/")
def root():
    return {"service": "ai-summarizer-api", "status": "running"}


@app.post(
    "/summarize",
    response_model=SummarizeResponse,
    responses={400: {"model": ErrorResponse}},
)
def summarize_endpoint(payload: SummarizeRequest):
    text = payload.text

    if text is None or not isinstance(text, str):
        raise HTTPException(
            status_code=400,
            detail={"error": "invalid_input", "detail": "Field 'text' must be a string."},
        )

    if text.strip() == "":
        raise HTTPException(
            status_code=400,
            detail={"error": "empty_input", "detail": "Field 'text' must not be empty."},
        )

    if len(text) > MAX_TEXT_LENGTH:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "input_too_long",
                "detail": f"Field 'text' must be at most {MAX_TEXT_LENGTH} characters.",
            },
        )

    return SummarizeResponse(summary=summarize(text))