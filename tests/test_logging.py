# ─────────────────────────────────────────────────────────────
# Tests for logging behavior (GL-6)
# ─────────────────────────────────────────────────────────────
# Logging middleware should not change endpoint behavior —
# these tests verify that normal requests still work with
# logging turned on.
# ─────────────────────────────────────────────────────────────

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_still_works_with_logging():
    """The /health endpoint should still return 200 with logging on."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_summarize_still_works_with_logging():
    """The /summarize endpoint should still return a summary."""
    response = client.post(
        "/summarize",
        json={"text": "Hello world. This is a test. It works fine."},
    )
    assert response.status_code == 200
    assert "summary" in response.json()