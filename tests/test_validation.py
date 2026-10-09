from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_valid_input_returns_200():
    response = client.post(
        "/summarize",
        json={"text": "Python is a language. Python is used widely. Python is popular."},
    )
    assert response.status_code == 200
    assert "summary" in response.json()


def test_empty_string_returns_400():
    response = client.post("/summarize", json={"text": ""})
    assert response.status_code == 400
    body = response.json()
    assert body["detail"]["error"] == "empty_input"


def test_whitespace_only_returns_400():
    response = client.post("/summarize", json={"text": "     "})
    assert response.status_code == 400
    body = response.json()
    assert body["detail"]["error"] == "empty_input"


def test_missing_text_field_returns_422():
    response = client.post("/summarize", json={})
    assert response.status_code == 422


def test_non_string_text_returns_422():
    response = client.post("/summarize", json={"text": 12345})
    assert response.status_code == 422


def test_over_length_returns_400():
    long_text = "a" * 5001
    response = client.post("/summarize", json={"text": long_text})
    assert response.status_code == 400
    body = response.json()
    assert body["detail"]["error"] == "input_too_long"


def test_exactly_max_length_returns_200():
    text = ("word " * 1000).strip()
    response = client.post("/summarize", json={"text": text})
    assert response.status_code == 200