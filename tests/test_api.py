"""Tests for API."""
import pytest
import json
from src.api.main import create_app


@pytest.fixture
def client():
    """Create test client."""
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "healthy"
    assert data["service"] == "finagent-unified"


def test_chat_endpoint(client):
    """Test chat endpoint."""
    response = client.post(
        "/api/v1/chat",
        json={"message": "查询持仓情况"},
        content_type="application/json"
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "session_id" in data
    assert "response" in data


def test_chat_with_session_id(client):
    """Test chat with existing session ID."""
    session_id = "test-session-123"
    response = client.post(
        "/api/v1/chat",
        json={"message": "查询客户", "session_id": session_id},
        content_type="application/json"
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["session_id"] == session_id


def test_set_customer(client):
    """Test set customer endpoint."""
    response = client.post(
        "/api/v1/session/test-session/customer",
        json={
            "customer_id": "C001",
            "name": "王总",
            "total_assets": 5000000,
            "risk_level": "R4"
        },
        content_type="application/json"
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "success"
    assert data["customer"]["name"] == "王总"


def test_status_endpoint_new_session(client):
    """Test status endpoint for new session."""
    response = client.get("/api/v1/session/new-session/status")
    assert response.status_code == 404


def test_status_endpoint_existing_session(client):
    """Test status endpoint for existing session."""
    # First create a session
    chat_response = client.post(
        "/api/v1/chat",
        json={"message": "你好"},
        content_type="application/json"
    )
    session_id = json.loads(chat_response.data)["session_id"]

    # Then check status
    response = client.get(f"/api/v1/session/{session_id}/status")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "session_id" in data
    assert "registered_agents" in data


def test_list_sessions(client):
    """Test listing sessions."""
    response = client.get("/api/v1/sessions")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "sessions" in data
    assert "count" in data