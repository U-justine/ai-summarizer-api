# ─────────────────────────────────────────────────────────────
# Tests for the /health endpoint (GL-5)
# ─────────────────────────────────────────────────────────────
# The health endpoint is used by monitoring tools, load balancers,
# and container orchestrators to check if the service is alive.
# ─────────────────────────────────────────────────────────────

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_returns_200():
    """The endpoint should return HTTP 200 when the service is alive."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_returns_status_ok():
    """The response body should be exactly {"status": "ok"}."""
    response = client.get("/health")
    assert response.json() == {"status": "ok"}


def test_health_has_json_content_type():
    """The response should be JSON."""
    response = client.get("/health")
    assert response.headers["content-type"].startswith("application/json")