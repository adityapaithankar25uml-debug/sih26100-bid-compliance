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


def test_idempotency_vs_correlation_headers(client):
    headers = {
        "X-Correlation-ID": "test-correlation-id-12345",
        "X-Idempotency-Key": "test-idempotency-key-abcde",
    }
    response = client.get("/api/v1/health", headers=headers)
    assert response.status_code == 200
    assert response.headers["X-Correlation-ID"] == "test-correlation-id-12345"
    assert response.headers["X-Idempotency-Key"] == "test-idempotency-key-abcde"

