# ─────────────────────────────────────────────────────────────
# AI Summarizer API — Main Application
# ─────────────────────────────────────────────────────────────
# This file defines the FastAPI app with three endpoints:
#   1. GET  /          → service info (liveness)
#   2. GET  /health    → health check (GL-5)
#   3. POST /summarize → summarize text (GL-1 + GL-2 validation)
#
#   US1 (GL-1): POST /summarize — extractive summarization
#   US2 (GL-2): input validation — 400 errors for bad input
#   US5 (GL-5): GET /health — liveness check
#   US6 (GL-6): request logging middleware
#   US7 (GL-7): unified error shape for 422 responses
# ─────────────────────────────────────────────────────────────

import logging
import time

# ─── US7 (GL-7): imports for the unified error handler ──
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from app.summarizer import summarize


# ═════════════════════════════════════════════════════════════
# US6 (GL-6): Logging setup
# ═════════════════════════════════════════════════════════════
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("ai-summarizer-api")


# ═════════════════════════════════════════════════════════════
# App setup
# ═════════════════════════════════════════════════════════════
app = FastAPI(title="AI Summarizer API")

# Maximum allowed length of input text (in characters) — US2 (GL-2)
MAX_TEXT_LENGTH = 5000


# ═════════════════════════════════════════════════════════════
# US7 (GL-7): Unified error handler for 422 (Pydantic) responses
# ═════════════════════════════════════════════════════════════
# Makes Pydantic's 422 errors use the same {error, detail} shape
# as our custom 400 errors, so clients see one format.
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Convert Pydantic 422 errors to our standard {error, detail} shape."""
    errors = exc.errors()
    detail = errors[0].get("msg", "Invalid input.") if errors else "Invalid input."

    return JSONResponse(
        status_code=422,
        content={"error": "validation_error", "detail": detail},
    )


# ═════════════════════════════════════════════════════════════
# US6 (GL-6): Request logging middleware
# ═════════════════════════════════════════════════════════════
# Runs on EVERY request. Records:
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


# ═════════════════════════════════════════════════════════════
# Request / Response models (Pydantic)
# ═════════════════════════════════════════════════════════════
class SummarizeRequest(BaseModel):
    """US1 (GL-1): Shape of the POST /summarize request body."""
    text: str = Field(..., description="Text to summarize")


class SummarizeResponse(BaseModel):
    """US1 (GL-1): Shape of a successful /summarize response."""
    summary: str


class ErrorResponse(BaseModel):
    """US2 (GL-2): Shape of a 400 error response."""
    error: str
    detail: str


# ═════════════════════════════════════════════════════════════
# US1 (GL-1): Endpoint 1 — Root (service info)
# ═════════════════════════════════════════════════════════════
@app.get("/")
def root():
    """Simple info endpoint — used to confirm the service is up."""
    return {"service": "ai-summarizer-api", "status": "running"}


# ═════════════════════════════════════════════════════════════
# US5 (GL-5): Endpoint 2 — Health check
# ═════════════════════════════════════════════════════════════
@app.get("/health")
def health():
    """Liveness check — monitoring tools ping this to verify the service is alive."""
    return {"status": "ok"}


# ═════════════════════════════════════════════════════════════
# US1 (GL-1) + US2 (GL-2): Endpoint 3 — Summarize
# ═════════════════════════════════════════════════════════════
@app.post(
    "/summarize",
    response_model=SummarizeResponse,
    responses={400: {"model": ErrorResponse}},
)
def summarize_endpoint(payload: SummarizeRequest):
    """
    Summarize the given text.

    Validation rules (US2 / GL-2):
      - text must be a string             → 400 invalid_input
      - text must not be empty/whitespace → 400 empty_input
      - text must be ≤ 5000 characters    → 400 input_too_long
    """
    text = payload.text

    # ─── US2 (GL-2): Rule 1 — must be a string ────────────────
    if text is None or not isinstance(text, str):
        raise HTTPException(
            status_code=400,
            detail={"error": "invalid_input", "detail": "Field 'text' must be a string."},
        )

    # ─── US2 (GL-2): Rule 2 — must not be empty/whitespace ────
    if text.strip() == "":
        raise HTTPException(
            status_code=400,
            detail={"error": "empty_input", "detail": "Field 'text' must not be empty."},
        )

    # ─── US2 (GL-2): Rule 3 — must not exceed max length ──────
    if len(text) > MAX_TEXT_LENGTH:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "input_too_long",
                "detail": f"Field 'text' must be at most {MAX_TEXT_LENGTH} characters.",
            },
        )

    # ─── US1 (GL-1): all checks passed → run the summarizer ───
    return SummarizeResponse(summary=summarize(text))