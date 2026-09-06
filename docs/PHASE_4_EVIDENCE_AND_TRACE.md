# Phase 4 — Evidence Lineage & Calculation Trace

## 1. Traceability Invariant
Every compliance result is backed by a complete, traceable calculation lineage chain:
```
Requirement
  └── ComplianceRule
       └── ComplianceFact
            └── VerificationRecord / ExtractedField
                 └── Source Document / Government Source
```

## 2. Explanation Generation
- Primary explanations are deterministically rendered from AST traces and templates.
- Optional AI explanations may rephrase outputs for readability but are **strictly prohibited** from modifying evaluation results.
