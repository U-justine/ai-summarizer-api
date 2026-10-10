# ─────────────────────────────────────────────────────────────
# Tests for input validation (US2 / GL-2 + US7 / GL-7)
# ─────────────────────────────────────────────────────────────
# What these tests check:
#   - Happy path (valid input)              → 200 with summary
#   - Empty string                          → 400 empty_input
#   - Whitespace only                       → 400 empty_input
#   - Missing field                         → 422 unified shape (GL-7)
#   - Non-string type                       → 422 unified shape (GL-7)
#   - Over-length text (>5000 chars)        → 400 input_too_long
#   - Boundary: exactly max length (5000)   → 200 success
#
# Why these matter:
#   These tests act as a contract for the API. If someone breaks
#   validation rules in the future, these tests fail immediately.
#   They cover all three branches of the GL-2 validation logic plus
#   the GL-7 unified error shape.
# ─────────────────────────────────────────────────────────────

from fastapi.testclient import TestClient
from app.main import app

# TestClient lets us call the FastAPI app directly in tests —
# no real HTTP server needed.
client = TestClient(app)


# ─── Test 1: Happy path ──────────────────────────────────────
# Verify that valid input still works after all validation rules
# were added. This is the "everything is fine" scenario.
def test_valid_input_returns_200():
    response = client.post(
        "/summarize",
        json={"text": "Python is a language. Python is used widely. Python is popular."},
    )
    assert response.status_code == 200
    assert "summary" in response.json()


# ─── Test 2: Empty string ────────────────────────────────────
# Sending "" as text should be rejected with 400, not processed.
# The error body should say specifically WHY: "empty_input".
def test_empty_string_returns_400():
    response = client.post("/summarize", json={"text": ""})
    assert response.status_code == 400
    body = response.json()
    assert body["detail"]["error"] == "empty_input"


# ─── Test 3: Whitespace-only ─────────────────────────────────
# Sending "     " (only spaces) should also be rejected. Users
# who paste blank content shouldn't get a 200 back.
def test_whitespace_only_returns_400():
    response = client.post("/summarize", json={"text": "     "})
    assert response.status_code == 400
    body = response.json()
    assert body["detail"]["error"] == "empty_input"


# ─── Test 4: Missing field (US7 / GL-7) ──────────────────────
# Sending {} — no "text" key at all — is caught by Pydantic
# BEFORE our code runs. FastAPI would normally return a list-shaped
# 422 error, but our GL-7 handler converts it to {error, detail}.
def test_missing_text_field_returns_422():
    response = client.post("/summarize", json={})
    assert response.status_code == 422
    body = response.json()
    assert body["error"] == "validation_error"
    assert "detail" in body


# ─── Test 5: Non-string type (US7 / GL-7) ────────────────────
# Sending a number instead of a string is also a Pydantic error.
# Same unified shape applies thanks to GL-7.
def test_non_string_text_returns_422():
    response = client.post("/summarize", json={"text": 12345})
    assert response.status_code == 422
    body = response.json()
    assert body["error"] == "validation_error"
    assert "detail" in body


# ─── Test 6: Over-length input ───────────────────────────────
# Anything over 5000 characters should be rejected to prevent
# abuse (huge payloads slow down summarization).
def test_over_length_returns_400():
    long_text = "a" * 5001
    response = client.post("/summarize", json={"text": long_text})
    assert response.status_code == 400
    body = response.json()
    assert body["detail"]["error"] == "input_too_long"


# ─── Test 7: Boundary case ───────────────────────────────────
# Exactly 5000 characters should be allowed (the limit is
# "at most 5000", not "less than 5000"). Boundary tests catch
# off-by-one errors in comparison operators.
def test_exactly_max_length_returns_200():
    text = ("word " * 1000).strip()   # 4999 chars — just under the limit
    response = client.post("/summarize", json={"text": text})
    assert response.status_code == 200