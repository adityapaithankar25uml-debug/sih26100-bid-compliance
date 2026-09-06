def test_auth_login_and_me(client, test_officer_user):
    login_resp = client.post(
        "/api/v1/auth/login",
        json={"email": "officer_test@cpcl.gov.in", "password": "TestPass123!"},
    )
    assert login_resp.status_code == 200
    token_data = login_resp.json()
    assert "access_token" in token_data
    assert token_data["role"] == "ProcurementOfficer"

    # Get /me with token
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    me_resp = client.get("/api/v1/auth/me", headers=headers)
    assert me_resp.status_code == 200
    assert me_resp.json()["email"] == "officer_test@cpcl.gov.in"


def test_rbac_auditor_access_control(client, auditor_headers):
    # Auditor should be forbidden from creating tenders (requires ProcurementOfficer/SeniorReviewer)
    tender_payload = {
        "tender_number": "TENDER-UNAUTH-001",
        "title": "Unauthorized Tender Creation Attempt",
    }
    resp = client.post("/api/v1/tenders", json=tender_payload, headers=auditor_headers)
    assert resp.status_code == 403
    assert "Access denied" in resp.json()["detail"]

    # Auditor SHOULD be allowed to access audit endpoints
    audit_resp = client.get("/api/v1/audit/events", headers=auditor_headers)
    assert audit_resp.status_code == 200
