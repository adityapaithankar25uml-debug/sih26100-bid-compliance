def test_bidder_and_submission_workflow(client, officer_headers):
    # 1. Create tender
    tender_resp = client.post(
        "/api/v1/tenders",
        json={
            "tender_number": "TENDER-SUB-001",
            "title": "Tender for Submission Workflow Test",
        },
        headers=officer_headers,
    )
    tender_data = tender_resp.json()
    tender_id = tender_data["id"]
    version_id = tender_data["versions"][0]["id"]

    # 2. Register bidder
    bidder_resp = client.post(
        "/api/v1/bidders",
        json={
            "bidder_name": "Zenith Engineering Pvt Ltd",
            "registration_number": "REG-ZENITH-01",
            "pan": "AAACA9999F",
        },
        headers=officer_headers,
    )
    assert bidder_resp.status_code == 200
    bidder_id = bidder_resp.json()["id"]

    # 3. Create submission bound to TenderVersion
    sub_resp = client.post(
        "/api/v1/submissions",
        json={
            "bidder_id": bidder_id,
            "tender_id": tender_id,
            "tender_version_id": version_id,
            "submission_reference": "SUB-REF-ZENITH-01",
        },
        headers=officer_headers,
    )
    assert sub_resp.status_code == 200
    sub_data = sub_resp.json()
    assert sub_data["submission_reference"] == "SUB-REF-ZENITH-01"
    assert sub_data["tender_version_id"] == version_id
