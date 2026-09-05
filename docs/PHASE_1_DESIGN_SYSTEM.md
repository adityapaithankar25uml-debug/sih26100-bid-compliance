# Phase 1 — Enterprise Design System Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 Design System Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Design Aesthetics Policy

This specification defines the visual tokens, typography, component library standards, and semantic status color palettes for the platform.

The visual direction mandates an **Enterprise / Government Procurement Aesthetic**:
- Primary palette: Deep Navy (`#0F172A`, `#1E293B`), Government Blue (`#0284C7`), Neutral Slate (`#F8FAFC`, `#E2E8F0`).
- Purple AI aesthetics, neon gradients, glassmorphism, chatbot bubbles, and decorative AI graphics are **STRICTLY PROHIBITED**.
- Color is **NEVER** the sole indicator of security, status, or authorization. All colored elements must be accompanied by explicit text labels or semantic icons.

---

## 2. Token & Palette Specifications

| Token Category | Token Name | Value / Specification | Usage Context |
|---|---|---|---|
| **Primary Brand** | `color-primary-navy` | `#0F172A` (Slate 900) | Shell background, primary headers |
| **Brand Accent** | `color-primary-blue` | `#0284C7` (Sky 600) | Primary buttons, active tabs, links |
| **Neutral Surface** | `color-surface-light` | `#F8FAFC` (Slate 50) | Main background surface |
| **Neutral Border** | `color-border-subtle` | `#E2E8F0` (Slate 200) | Table borders, card outlines |
| **Status Pass** | `color-status-pass` | `#16A34A` (Emerald 600) | Compliant / Verified status badges |
| **Status Review** | `color-status-review` | `#D97706` (Amber 600) | Pending review, unverified, human action |
| **Status Fail** | `color-status-fail` | `#DC2626` (Red 600) | Non-compliant status badges |
| **Status Technical**| `color-status-tech` | `#64748B` (Slate 500) | Technical integration failure / fallback |

---

## 3. Typography & Density Standards

- **Font Family:** Inter / Roboto / system-ui sans-serif. Monospace (`JetBrains Mono` / `Fira Code`) for SHA-256 hashes, ULIDs, and JSON AST rules.
- **Density:** Compact, high-density layout optimized for displaying multi-column compliance matrices and side-by-side document comparison viewers on desktop displays.
