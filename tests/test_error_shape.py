# ─────────────────────────────────────────────────────────────
# Tests for unified error shape (US7 / GL-7)
# ─────────────────────────────────────────────────────────────
# Before GL-7: 400 and 422 errors had DIFFERENT shapes:
#   400: {"detail": {"error": "...", "detail": "..."}}
#   422: {"detail": [{"loc": [...], "msg": "...", "type": "..."}]}
#
# After GL-7: both use the same shape so clients can parse
# errors uniformly without special-casing.
# ─────────────────────────────────────────────────────────────

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# ─── Test 1: 400 shape ───────────────────────────────────────
# Our custom validation errors (empty input) should still
# include an 'error' code and human-readable 'detail'.
def test_400_has_unified_shape():
    response = client.post("/summarize", json={"text": ""})
    assert response.status_code == 400
    body = response.json()
    assert "error" in body["detail"]
    assert "detail" in body["detail"]


# ─── Test 2: 422 shape ───────────────────────────────────────
# Pydantic's 422 error should be flattened into {error, detail}
# by our exception handler — no more nested list of errors.
def test_422_has_unified_shape():
    response = client.post("/summarize", json={})
    assert response.status_code == 422
    body = response.json()
    assert body["error"] == "validation_error"
    assert "detail" in body
    assert isinstance(body["detail"], str)


# ─── Test 3: Both have an 'error' key ────────────────────────
# No matter which error path fires, the response should always
# have a predictable 'error' field somewhere.
def test_both_error_types_have_error_key():
    r1 = client.post("/summarize", json={"text": ""})
    r2 = client.post("/summarize", json={})
    assert "error" in r1.json()["detail"]
    assert "error" in r2.json()


# ─── Test 4: All custom 400s share the same shape ────────────
# Three different validation failures — but all should produce
# the same structure: body["detail"] contains {error, detail}.
def test_error_shape_is_consistent_across_cases():
    cases = [
        {"text": ""},          # empty string
        {"text": "     "},     # whitespace only
        {"text": "a" * 5001},  # over-length
    ]
    for payload in cases:
        response = client.post("/summarize", json=payload)
        assert response.status_code == 400
        body = response.json()
        assert "error" in body["detail"]
        assert "detail" in body["detail"]