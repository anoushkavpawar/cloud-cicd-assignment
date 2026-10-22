from app import app

def test_home():
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert b"Version 2" in response.data

def test_health():
    response = app.test_client().get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"