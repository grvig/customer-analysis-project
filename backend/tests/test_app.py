import sys
import os
os.environ["JWT_SECRET"] = "test_secret_for_pytest"
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app import app
from auth import create_access_token

client = TestClient(app)


@pytest.fixture
def auth_headers():
    token = create_access_token("testuser")
    return {"Authorization": f"Bearer {token}"}


# --- Health & Home ---

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["status"] == "healthy"


# --- Auth ---

def test_protected_endpoint_without_token():
    response = client.get("/dashboard")
    assert response.status_code in (401, 403)

def test_protected_endpoint_with_invalid_token():
    response = client.get("/dashboard", headers={"Authorization": "Bearer invalid.token.here"})
    assert response.status_code == 401


# --- SQL Injection Protection ---
# /query endpoint was removed — direct SQL execution is not exposed at all

def test_query_endpoint_does_not_exist():
    response = client.post("/query", json={"sql": "SELECT * FROM customers"})
    assert response.status_code == 404

def test_drop_table_no_endpoint():
    response = client.post("/query", json={"sql": "DROP TABLE customers;"})
    assert response.status_code == 404

def test_delete_no_endpoint():
    response = client.post("/query", json={"sql": "DELETE FROM customers WHERE 1=1;"})
    assert response.status_code == 404


# --- Dashboard ---

def test_dashboard_structure(auth_headers):
    mock_rows = [(100,)]
    mock_complaints = [("Engine", 50)]
    mock_revenue = [("Oil Change", 1000.0)]
    mock_ratings = [("Anna Nagar", 4.2)]

    with patch("app.execute_query") as mock_query:
        mock_query.side_effect = [
            mock_rows, mock_rows, mock_rows, mock_rows,
            mock_complaints, mock_revenue, mock_ratings
        ]
        response = client.get("/dashboard", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "summary" in data
    assert "complaints" in data
    assert "revenue" in data
    assert "ratings" in data


# --- Report endpoint ---

def test_report_invalid_type(auth_headers):
    with patch("app.generate_report", return_value=None):
        response = client.post("/report", json={"report_type": "nonexistent"}, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["success"] is False
    assert response.json()["error"] == "Invalid report type"

def test_report_valid_type(auth_headers):
    with patch("app.generate_report", return_value="# Report Content"):
        response = client.post("/report", json={"report_type": "complaint"}, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["report"] == "# Report Content"
    assert "generation_time" in data

def test_report_aliases(auth_headers):
    with patch("app.generate_report", return_value="# Report") as mock_gen:
        client.post("/report", json={"report_type": "complaints"}, headers=auth_headers)
        mock_gen.assert_called_with("complaint")

        client.post("/report", json={"report_type": "revenue report"}, headers=auth_headers)
        mock_gen.assert_called_with("revenue")


# --- Custom report ---

def test_custom_report(auth_headers):
    with patch("app.generate_custom_report", return_value="# Custom Report"):
        response = client.post("/report/custom", json={"question": "Show top branches"}, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["report"] == "# Custom Report"
    assert "generation_time" in data
    assert data["question"] == "Show top branches"


# --- Ask endpoint ---

def test_ask_success(auth_headers):
    mock_result = {
        "success": True,
        "sql": "SELECT COUNT(*) FROM customers",
        "rows": [(100,)],
        "answer": "There are 100 customers.",
        "execution_time": 1.5,
        "error": None
    }
    with patch("app.ask_ai", return_value=mock_result):
        response = client.post("/ask", json={"question": "How many customers?"}, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["success"] is True

def test_ask_failure(auth_headers):
    mock_result = {
        "success": False,
        "sql": None,
        "rows": [],
        "answer": None,
        "execution_time": 1.0,
        "error": "AI model error"
    }
    with patch("app.ask_ai", return_value=mock_result):
        response = client.post("/ask", json={"question": "gibberish question"}, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["success"] is False
