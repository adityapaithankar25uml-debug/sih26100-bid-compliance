def test_health_probe(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "sih26100-backend"
    assert "X-Correlation-ID" in response.headers


def test_readiness_probe(client):
    response = client.get("/api/v1/readiness")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "components" in data
    assert "database" in data["components"]
