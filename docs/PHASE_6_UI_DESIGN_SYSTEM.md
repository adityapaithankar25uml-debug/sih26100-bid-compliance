# Phase 6 — GeM-Inspired Enterprise UI Design System

## 1. Design Direction & Visual Tokens
Inspired by the Government e-Marketplace (GeM) visual hierarchy, the interface presents a structured, high-density, professional government procurement experience:

- **Deep Navy (`#0a192f`, `#0a101d`):** Command header, primary sidebar, and authoritative banners.
- **Government Blue (`#1e40af`, `#2563eb`):** Primary action buttons, active navigation indicators, link highlights.
- **Slate Neutrals (`#f8fafc`, `#f1f5f9`, `#cbd5e1`, `#0f172a`):** Crisp content card backgrounds, subtle borders, high-contrast text typography.
- **Status Color Coding:**
  - **PASS / QUALIFIED / VERIFIED:** Restrained Emerald (`#059669`, `#ecfdf5`)
  - **REVIEW REQUIRED / PENDING / MISSING EVIDENCE:** Restrained Amber (`#d97706`, `#fffbe6`)
  - **FAIL / DISQUALIFIED / TAMPERED:** Restrained Rose (`#e11d48`, `#fff1f2`)
  - **AI EXTRACTED (ADVISORY):** Deep Purple (`#7c3aed`, `#faf5ff`)
  - **MOCK / DEMO INTEGRATION:** Warm Orange (`#ea580c`, `#fff7ed`)

---

## 2. Status Badge Taxonomy & Rules
1. `GOVERNMENT VERIFIED` — Derived from authoritative government registry verification.
2. `AI EXTRACTED (ADVISORY)` — Derived from AI OCR / document extraction; requires human or rule confirmation.
3. `PASS` — Rule requirement satisfied by deterministic evaluation.
4. `FAIL` — Rule requirement failing policy threshold.
5. `MISSING EVIDENCE (NON-FATAL)` — Evidence incomplete; non-fatal evaluation status.
6. `HUMAN REVIEW REQUIRED` — Flagged for officer review and manual resolution.
7. `MOCK / DEMO` — Explicit label indicating mock gateway integration mode.
