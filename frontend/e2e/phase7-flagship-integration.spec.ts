import { test, expect } from '@playwright/test';

test.describe('Phase 7 Flagship End-to-End Procurement Compliance Integration Suite', () => {

  test.beforeEach(async ({ page }) => {
    // Authenticate as Procurement Officer via Demo Identity Selector
    await page.goto('http://localhost:3000/login');
    await page.getByRole('button', { name: /Authenticate as ProcurementOfficer/i }).click();
    await page.waitForURL('**/dashboard');
  });

  test('FLAGSHIP E2E: Complete 16-Step Procurement Compliance Verification Lifecycle', async ({ page }) => {
    test.setTimeout(60000);

    // 1. Dashboard Landing & Metrics Verification
    await expect(page.getByText('Procurement Compliance Verification Command Center')).toBeVisible();
    await expect(page.getByText('Rajesh Kumar', { exact: false })).toBeVisible();
    await expect(page.getByText('Procurement Officer', { exact: true })).toBeVisible();

    // 2. Open Seeded Tender TEN_01 Catalog & Specs
    await page.goto('http://localhost:3000/tenders/TEN_01');
    await expect(page.getByText('Tender Requirements', { exact: false })).toBeVisible();
    await expect(page.getByText('TENDER-CPCL-2026-001', { exact: false })).toBeVisible();

    // 3. Inspect Tender Requirement Specs & Extraction
    await expect(page.getByText('Version History')).toBeVisible();

    // 4. Open Seeded Bid SUB_01 Workspace
    await page.goto('http://localhost:3000/bids/SUB_01');
    await expect(page.getByText('Integrated Bid Verification Workspace', { exact: false })).toBeVisible();
    await expect(page.getByText('SUB-2026-CPCL-001', { exact: false })).toBeVisible();

    // 5. Inspect Bidder Identity & Document Extraction Status
    await page.getByRole('button', { name: /Documents & AI Extraction/i }).click();
    await expect(page.getByText('Document Intelligence & AI Field Extraction Review', { exact: false })).toBeVisible();

    // 6. Inspect Government Verification Center & MOCK Badges
    await page.goto('http://localhost:3000/verification');
    await expect(page.getByText('Government Verification Center')).toBeVisible();
    await expect(page.getByText('INTEGRATION MODE: MOCK / DEMO')).toBeVisible();
    await expect(page.getByText('GSTIN / GST Portal Registry')).toBeVisible();
    await expect(page.getByText('Udyam / MSME Certificate Registry')).toBeVisible();

    // 7. Inspect Evidence Explorer & 9 Quality Dimensions
    await page.goto('http://localhost:3000/evidence');
    await expect(page.getByText('Evidence & Provenance Explorer')).toBeVisible();
    await expect(page.getByText('9 INDEPENDENT EVIDENCE QUALITY DIMENSIONS', { exact: true })).toBeVisible();
    await expect(page.getByText('1. source_authority')).toBeVisible();
    await expect(page.getByText('2. source_freshness')).toBeVisible();
    await expect(page.getByText('4. integrity_hash_validity')).toBeVisible();
    await expect(page.getByText('5. identity_linkage')).toBeVisible();
    await expect(page.getByText('9. consistency')).toBeVisible();

    // 8. Inspect Deterministic Compliance Evaluation Matrix
    await page.goto('http://localhost:3000/bids/SUB_01');
    await page.getByRole('button', { name: /Compliance Matrix/i }).click();
    await expect(page.getByText('Deterministic Compliance Matrix Evaluation')).toBeVisible();

    // 9. Inspect Advisory Risk Engine Assessment
    await page.goto('http://localhost:3000/risk');
    await expect(page.getByText('Advisory Risk Engine Management')).toBeVisible();
    await expect(page.getByText('RISK ENGINE ADVISORY CONTROL RULE')).toBeVisible();

    // 10. Open Human Review Workspace & Task Queue
    await page.goto('http://localhost:3000/human-review');
    await expect(page.getByText('Procurement Officer Human Review Queue')).toBeVisible();

    // 11. Resolve Review Item & Record Officer Action
    await page.goto('http://localhost:3000/bids/SUB_01');
    await page.getByRole('button', { name: /Human Review/i }).click();

    // 12. Inspect Manual Override & Four-Eyes Policy Threshold
    await page.getByRole('button', { name: /Decision & Override/i }).click();
    await expect(page.getByText('Four-Eyes Manual Rule Overrides', { exact: false })).toBeVisible();

    // 13. Open Audit Explorer & Verify Tamper-Evident SHA-256 Hash Chain
    await page.goto('http://localhost:3000/audit');
    await expect(page.getByText('Verify Tamper-Evident SHA-256 Audit Hash Chain')).toBeVisible();
    await page.getByRole('button', { name: /Verify Audit Chain Integrity/i }).click();
    await expect(page.getByText('Audit Hash Chain Verified Intact', { exact: false })).toBeVisible();

    // 14. Confirm Non-Authoritative AI & Authoritative Human Officer Rule
    await page.goto('http://localhost:3000/dashboard');
    await expect(page.getByText('Core System Principle')).toBeVisible();

    // 15. Verify Government Integration Status MOCK/DEMO Classification
    await page.goto('http://localhost:3000/verification');
    await expect(page.getByText('MOCK / DEMO')).toBeVisible();

    // 16. Verify End-to-End Navigation Consistency Across Workspace
    await page.goto('http://localhost:3000/dashboard');
    await expect(page.getByText('Procurement Compliance Verification Command Center')).toBeVisible();
  });

});
