from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_metrics_endpoint():
    response = client.get("/stores/STORE_001/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "total_entries" in data
    assert "unique_visitors" in data
    assert "conversion_rate" in data


def test_funnel_endpoint():
    response = client.get("/stores/STORE_001/funnel")
    assert response.status_code == 200
    assert "funnel" in response.json()


def test_heatmap_endpoint():
    response = client.get("/stores/STORE_001/heatmap")
    assert response.status_code == 200
    assert "heatmap" in response.json()


def test_anomalies_endpoint():
    response = client.get("/stores/STORE_001/anomalies")
    assert response.status_code == 200
    assert "anomalies" in response.json()