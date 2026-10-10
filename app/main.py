# ─────────────────────────────────────────────────────────────
# AI Summarizer API — Main Application
# ─────────────────────────────────────────────────────────────
# This file defines the FastAPI app with three endpoints:
#   1. GET  /          → service info (liveness)
#   2. GET  /health    → health check (GL-5)
#   3. POST /summarize → summarize text (GL-1 + GL-2 validation)
#
# GL-6: adds request logging middleware so every request is recorded.
# ─────────────────────────────────────────────────────────────

import logging
import time

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from app.summarizer import summarize

# ─── Logging setup (GL-6) ────────────────────────────────────
# Configure how log lines look and at what level they are recorded.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("ai-summarizer-api")

# ─── App setup ───────────────────────────────────────────────
app = FastAPI(title="AI Summarizer API")

# Maximum allowed length of input text (in characters)
MAX_TEXT_LENGTH = 5000


# ─── Logging middleware (GL-6) ───────────────────────────────
# This function runs on EVERY request. It records:
#   - HTTP method (GET, POST, ...)
#   - Requested path (/health, /summarize, ...)
#   - Response status code (200, 400, 422, ...)
#   - Time taken (in milliseconds)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log every request: method, path, status, duration."""
    start = time.time()
    response = await call_next(request)
    duration_ms = (time.time() - start) * 1000
    logger.info(
        f"{request.method} {request.url.path} "
        f"-> {response.status_code} ({duration_ms:.1f}ms)"
    )
    return response


# ─── Request / Response models (Pydantic) ────────────────────
class SummarizeRequest(BaseModel):
    """Shape of the POST /summarize request body."""
    text: str = Field(..., description="Text to summarize")


class SummarizeResponse(BaseModel):
    """Shape of a successful /summarize response."""
    summary: str


class ErrorResponse(BaseModel):
    """Shape of a 400 error response."""
    error: str
    detail: str


# ─── Endpoint 1: Root (service info) ─────────────────────────
@app.get("/")
def root():
    """Simple info endpoint — used to confirm the service is up."""
    return {"service": "ai-summarizer-api", "status": "running"}


# ─── Endpoint 2: Health check (GL-5) ─────────────────────────
@app.get("/health")
def health():
    """Liveness check — monitoring tools ping this to verify the service is alive."""
    return {"status": "ok"}


# ─── Endpoint 3: Summarize (GL-1 + GL-2) ─────────────────────
@app.post(
    "/summarize",
    response_model=SummarizeResponse,
    responses={400: {"model": ErrorResponse}},
)
def summarize_endpoint(payload: SummarizeRequest):
    """
    Summarize the given text.

    Validation rules (GL-2):
      - text must be a string             → 400 invalid_input
      - text must not be empty/whitespace → 400 empty_input
      - text must be ≤ 5000 characters    → 400 input_too_long
    """
    text = payload.text

    # Rule 1: text must be a string (defensive — Pydantic already enforces this)
    if text is None or not isinstance(text, str):
        raise HTTPException(
            status_code=400,
            detail={"error": "invalid_input", "detail": "Field 'text' must be a string."},
        )

    # Rule 2: text must not be empty or whitespace-only
    if text.strip() == "":
        raise HTTPException(
            status_code=400,
            detail={"error": "empty_input", "detail": "Field 'text' must not be empty."},
        )

    # Rule 3: text must not exceed the maximum length
    if len(text) > MAX_TEXT_LENGTH:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "input_too_long",
                "detail": f"Field 'text' must be at most {MAX_TEXT_LENGTH} characters.",
            },
        )

    # All checks passed — run the summarizer and return the result
    return SummarizeResponse(summary=summarize(text))