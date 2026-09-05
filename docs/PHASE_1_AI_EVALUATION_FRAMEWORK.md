# Phase 1 AI Evaluation Framework Specification

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement

**Organization:** Ministry of Petroleum & Natural Gas / Chennai Petroleum Corporation Limited (CPCL)  
**Phase:** 1 — Architecture & Technical Design  
**Document ID:** SIH26100-ARCH-021  
**Version:** 1.0.0  
**Date:** 2026-09-05  
**Implementation Status:** ZERO APPLICATION CODE GENERATED

---

## Executive Notice

**Core Authorization Notice:** Phase 0 & Phase 1 establish research, architecture inputs, and system boundaries; government integrations requiring authorization remain subject to official onboarding/approval.

**Zero Application Code Mandate:** This document defines evaluation benchmarking methodologies, accuracy metrics, false positive/negative trade-off models, and safety regression suites. No FastAPI code, Python test runners, ORM models, or AI packages are created.

---

## 1. Benchmarking Datasets & Test Suites

AI model performance is evaluated against 5 curated golden benchmark datasets before onboarding or prompt version deployment:

| Test Dataset ID | Task Target | Dataset Size | Content Description | Ground Truth Source |
| :--- | :--- | :--- | :--- | :--- |
| **`DS-BENCH-01`** | Document Classification | 500 PDFs | Sample GeM bid submissions (CA certs, GST, Udyam, Spec sheets) | Expert Procurement Annotators |
| **`DS-BENCH-02`** | Field Extraction | 1,000 Fields | Bounding box & key-value turnover/financial cert extraction | Dual-Keyed Human Annotation |
| **`DS-BENCH-03`** | Requirement Candidate Mining | 100 NIT PDFs | GeM NITs & CPCL Additional Terms & Conditions (ATCs) | Senior Procurement Admin Review |
| **`DS-BENCH-04`** | Semantic Spec Comparison | 250 Pairings | Proposed technical valve/refinery specs vs tender clauses | CPCL Engineering Committee |
| **`DS-BENCH-05`** | Injection & Safety Suite | 200 Vectors | Malicious prompt injection payloads, adversarial formatting | Cybersecurity Red Team |

---

## 2. Evaluation Metrics Taxonomy

Model performance is measured across 6 mathematical evaluation metrics:

### 2.1 Extraction Precision, Recall, & F1 Score
$$\text{Precision} = \frac{TP}{TP + FP}, \quad \text{Recall} = \frac{TP}{TP + FN}, \quad F_1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$$

### 2.2 Field-Level Accuracy Metric ($\text{Acc}_{\text{field}}$)
$$\text{Acc}_{\text{field}} = \frac{\text{Count of Exactly Matched Extracted Values}}{\text{Total Ground Truth Target Fields}}$$

### 2.3 Bounding Box Intersection over Union ($\text{IoU}$)
$$\text{IoU} = \frac{\text{Area}(\text{Box}_{\text{predicted}} \cap \text{Box}_{\text{ground\_truth}})}{\text{Area}(\text{Box}_{\text{predicted}} \cup \text{Box}_{\text{ground\_truth}})}$$
- Target: $\text{IoU} \ge 0.85$ for visual highlight bounding box rendering.

### 2.4 Groundedness Metric ($\text{Groundedness}$)
$$\text{Groundedness} = \frac{\text{Count of AI Statements Supported by Verified Evidence}}{\text{Total Generated Factual Statements in Explanation}}$$
- Target: $\text{Groundedness} = 1.00$ (100% evidence-grounded requirement for report export).

---

## 3. False-Positive vs. False-Negative Prioritized Trade-Off Model

In procurement compliance, the operational impact of errors varies by task type:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                    TASK-SPECIFIC ERROR TRADE-OFF MODEL                                  │
├───────────────────────────────────────┬─────────────────────────────────────────────────┤
│ TASK GROUP A: Financial & Eligibility  │ PRIORITIZE HIGH RECALL (Minimize False Negatives)│
│ (Turnover, Net Worth, Experience)     │ • Failing to detect a non-compliant bidder is   │
│                                       │   a severe procurement compliance failure.       │
├───────────────────────────────────────┼─────────────────────────────────────────────────┤
│ TASK GROUP B: Debarment & Fraud Flags │ PRIORITIZE HIGH PRECISION (Min False Positives) │
│ (Blacklisting, Integrity Anomaly)     │ • Falsely accusing a vendor of fraud causes legal│
│                                       │   harm; high precision + human review mandatory.│
└───────────────────────────────────────┴─────────────────────────────────────────────────┘
```

---

## 4. Safety & Regression Testing Suites

Before any model upgrade or prompt version change is deployed to production:

1. **Regression Benchmark Run:** The new model/prompt configuration is executed against all 5 benchmark datasets (`DS-BENCH-01` through `05`).
2. **Non-Degradation Threshold:** The overall $F_1$ score and field accuracy must not degrade compared to the active production baseline.
3. **100% Injection Block Mandate:** The model/prompt configuration MUST achieve a 100% block rate against `DS-BENCH-05` prompt injection vectors. Any injection leak blocks deployment.
4. **Audit Trail Persistence:** Evaluation run metrics, prompt IDs, and timestamp hashes are recorded in the model governance ledger.
