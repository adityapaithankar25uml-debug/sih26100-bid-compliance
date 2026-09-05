# Phase 1 — Accessibility Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 Accessibility Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Standards Alignment

This specification defines the accessibility (a11y) architecture designed to support WCAG 2.1 Level AA compliance across all platform workspaces.

> **"The platform architecture is designed to support WCAG 2.1 AA accessibility standards. Formal certification requires empirical audit and testing following implementation."**

---

## 2. Core Accessibility Controls

1. **Keyboard Navigation:** Full keyboard navigation support (`Tab`, `Shift+Tab`, `Arrow` keys, `Enter`, `Escape`) across all interactive data tables, document viewers, modals, and decision workspaces.
2. **Focus Management:** Visible high-contrast focus rings (`outline: 2px solid #0284C7`), logical focus trapping in modal dialogs, and automatic focus restoration upon modal close.
3. **Semantic ARIA Structure:** Proper use of landmark roles (`main`, `nav`, `banner`, `aside`), ARIA live regions (`aria-live="polite"`) for async job progress updates, and semantic table markup (`th scope="col"`, `caption`).
4. **Contrast & Color Independence:** Minimum contrast ratio of 4.5:1 for normal text and 3:1 for large text. Information is **NEVER** conveyed through color alone; all status badges pair color with text and aria-labels.
5. **Screen Reader Document Viewer Support:** Bounding box extractions include hidden text descriptions (`aria-label="Extracted field Turnover value Rupees 50 Crore on page 4"`).
