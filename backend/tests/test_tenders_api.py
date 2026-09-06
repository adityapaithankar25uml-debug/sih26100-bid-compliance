def test_create_and_list_tenders(client, officer_headers):
    # 1. Create tender
    payload = {
        "tender_number": "TENDER-API-001",
        "title": "API Test Tender for Pumps",
        "organization": "CPCL",
        "description": "Initial specification",
    }
    response = client.post("/api/v1/tenders", json=payload, headers=officer_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["tender_number"] == "TENDER-API-001"
    assert len(data["versions"]) == 1
    tender_id = data["id"]
    version_id = data["versions"][0]["id"]

    # 2. Add requirement to tender version
    req_payload = {
        "requirement_code": "REQ-API-001",
        "category": "TECHNICAL",
        "requirement_text": "Experience in oil refineries required",
        "is_mandatory": True,
    }
    req_resp = client.post(
        f"/api/v1/tenders/versions/{version_id}/requirements",
        json=req_payload,
        headers=officer_headers,
    )
    assert req_resp.status_code == 200
    assert req_resp.json()["requirement_code"] == "REQ-API-001"

    # 3. List tenders
    list_resp = client.get("/api/v1/tenders", headers=officer_headers)
    assert list_resp.status_code == 200
    assert len(list_resp.json()) >= 1
