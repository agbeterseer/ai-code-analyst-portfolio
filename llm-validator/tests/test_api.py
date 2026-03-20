from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_validate():
    res = client.post("/validate", json={
        "prompt": "What is the capital of France?",
        "response": "The capital of France is Paris.",
        "expected_schema": {}
    })
    assert res.status_code == 200
    assert "toxicity_score" in res.json()