# Phase 1 — Responsive Layout Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 Responsive Layout Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Device Scope

This specification defines the responsive layout grid, viewport breakpoints, and desktop-first optimization strategy for complex compliance workspaces.

Primary procurement officer workflows involve dense evidence inspection, side-by-side PDF comparison, and multi-column rule matrices. Therefore, core evaluation workspaces are **desktop-optimized** ($1280\text{px}+$ viewports) to preserve security, readability, and data integrity.

---

## 2. Breakpoint Grid & Adaptability Matrix

| Viewport Tier | Resolution Range | Target Devices | Layout Behavior & Adaptation |
|---|---|---|---|
| **Desktop Ultra** | $\ge 1920\text{px}$ | Dual Monitors, 4K Displays | 3-Column Layout: Side Nav + Compliance Matrix + Side-by-Side PDF Viewer |
| **Desktop Standard**| $1280\text{px}\text{--}1919\text{px}$ | Standard Workstation Laptops | 2-Column Layout: Collapsible Nav + Split Screen Matrix/Document Viewer |
| **Tablet Landscape**| $1024\text{px}\text{--}1279\text{px}$ | iPad Pro / Tablets | Stacked Layout: Collapsible Drawer Nav + Full Matrix / View Document Modal |
| **Mobile / Compact**| $< 1024\text{px}$ | Mobile Devices | **Read-Only Dashboard & Alert Overview Only.** Dense matrix evaluation disabled. |

---

## 3. Responsive Safeguards

1. **No Mobile Matrix Distortion:** Dense compliance matrices will not force 20 columns into a 320px mobile screen. Mobile viewports display read-only summaries with prompts to switch to desktop for decision recording.
2. **Horizontal Table Scroll:** Data tables use explicit container overflow handling with fixed sticky columns for `Requirement ID` and `Status Badge`.
