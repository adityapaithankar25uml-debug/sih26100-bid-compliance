import { test, expect } from '@playwright/test';

test.describe('Phase 6 Procurement Dashboard & Complete Frontend E2E Suite', () => {

  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000/login');
    await page.getByRole('button', { name: /Authenticate as ProcurementOfficer/i }).click();
    await page.waitForURL('**/dashboard');
  });

  test('TEST 1: Authentication & Authorized Demo Identity / Role-Aware UI', async ({ page }) => {
    // Verify Demo Account Selector notice on login page
    await page.goto('http://localhost:3000/login');
    await expect(page.getByText('Government Procurement Demo Identity Authentication Portal')).toBeVisible();
    await expect(page.getByText('MANDATORY RBAC CONTROL NOTICE')).toBeVisible();
    await page.getByRole('button', { name: /Authenticate as ProcurementOfficer/i }).click();
    await page.waitForURL('**/dashboard');
    await expect(page.getByText('Procurement Compliance Verification Command Center')).toBeVisible();
    await expect(page.getByText('Rajesh Kumar', { exact: false })).toBeVisible();
    await expect(page.getByText('Procurement Officer', { exact: true })).toBeVisible();
  });

  test('TEST 2: Procurement Dashboard Load & Metrics', async ({ page }) => {
    await page.goto('http://localhost:3000/dashboard');
    await expect(page.getByText('Active Tenders', { exact: true })).toBeVisible();
    await expect(page.getByText('Bid Submissions', { exact: true }).first()).toBeVisible();
    await expect(page.getByText('Pending Officer Tasks')).toBeVisible();
    await expect(page.getByText('Audit Chain Integrity')).toBeVisible();
    await expect(page.getByText('Core System Principle')).toBeVisible();
  });

  test('TEST 3: Tender Catalog Navigation & Search', async ({ page }) => {
    await page.goto('http://localhost:3000/tenders');
    await expect(page.getByText('Procurement Tender Catalog')).toBeVisible();
    await expect(page.getByPlaceholder('Search tender number or title...')).toBeVisible();
  });

  test('TEST 4: Tender Workspace & Requirement Specs', async ({ page }) => {
    await page.goto('http://localhost:3000/tenders/TEN_01');
    await expect(page.getByText('Tender Requirements')).toBeVisible();
    await expect(page.getByText('Version History')).toBeVisible();
  });

  test('TEST 5: Bid Submission Workspace Directory', async ({ page }) => {
    await page.goto('http://localhost:3000/bids');
    await expect(page.getByText('Bid Submissions Registry')).toBeVisible();
  });

  test('TEST 6: Bid Workspace — Compliance Matrix Status Separation', async ({ page }) => {
    await page.goto('http://localhost:3000/bids/SUB_01');
    await expect(page.getByText('Integrated Bid Verification Workspace')).toBeVisible();
    await page.getByRole('button', { name: /Compliance Matrix/i }).click();
    await expect(page.getByText('Deterministic Compliance Matrix Evaluation')).toBeVisible();
  });

  test('TEST 7: Government Verification Center & MOCK Badges', async ({ page }) => {
    await page.goto('http://localhost:3000/verification');
    await expect(page.getByText('Government Verification Center')).toBeVisible();
    await expect(page.getByText('INTEGRATION MODE: MOCK / DEMO')).toBeVisible();
    await expect(page.getByText('GSTIN / GST Portal Registry')).toBeVisible();
    await expect(page.getByText('Udyam / MSME Certificate Registry')).toBeVisible();
    await expect(page.getByText('Ministry of Corporate Affairs (CIN/DIN)')).toBeVisible();
    await expect(page.getByText('GeM / Central Procurement Debarment List')).toBeVisible();
  });

  test('TEST 8: Evidence Explorer & 9 Quality Dimensions', async ({ page }) => {
    await page.goto('http://localhost:3000/evidence');
    await expect(page.getByText('Evidence & Provenance Explorer')).toBeVisible();
    await expect(page.getByText('9 INDEPENDENT EVIDENCE QUALITY DIMENSIONS', { exact: true })).toBeVisible();
    await expect(page.getByText('1. source_authority')).toBeVisible();
    await expect(page.getByText('2. source_freshness')).toBeVisible();
    await expect(page.getByText('4. integrity_hash_validity')).toBeVisible();
    await expect(page.getByText('5. identity_linkage')).toBeVisible();
    await expect(page.getByText('9. consistency')).toBeVisible();
  });

  test('TEST 9: Advisory Risk Engine Panel', async ({ page }) => {
    await page.goto('http://localhost:3000/risk');
    await expect(page.getByText('Advisory Risk Engine Management')).toBeVisible();
    await expect(page.getByText('RISK ENGINE ADVISORY CONTROL RULE')).toBeVisible();
  });

  test('TEST 10: Human Review Officer Workspace Queue', async ({ page }) => {
    await page.goto('http://localhost:3000/human-review');
    await expect(page.getByText('Procurement Officer Human Review Queue')).toBeVisible();
  });

  test('TEST 11: Tamper-Evident SHA-256 Audit Hash Chain Explorer', async ({ page }) => {
    await page.goto('http://localhost:3000/audit');
    await expect(page.getByText('Verify Tamper-Evident SHA-256 Audit Hash Chain')).toBeVisible();
    await expect(page.getByRole('button', { name: /Verify Audit Chain Integrity/i })).toBeVisible();
  });

});
