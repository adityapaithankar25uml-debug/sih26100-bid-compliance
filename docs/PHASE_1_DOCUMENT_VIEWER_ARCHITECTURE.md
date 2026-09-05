# Phase 1 — Document Viewer Architecture Specification

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 11 Document Viewer Architecture Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Canvas Architecture

This specification defines the high-performance PDF rendering canvas, SVG bounding-box overlay system, page virtualization, and interactive text-selection hooks for document verification.

---

## 2. Document Viewer Interaction Layer

```
+-----------------------------------------------------------------------------------+
| TOOLBAR: Zoom: [ 100% ] | Fit: [ Width ] | Page: [ 3 / 18 ] | Overlays: [ ON/OFF ] |
+-----------------------------------------------------------------------------------+
| CANVAS CONTAINER                                                                  |
| +-------------------------------------------------------------------------------+ |
| | PDF Page Render Layer (Canvas / WebGL Rendering)                              | |
| |                                                                               | |
| | SVG Bounding Box Layer (Positioned absolute over canvas coordinates)          | |
| | +---------------------------------------------------------------------------+ | |
| | | SVG Rect: `x=120, y=340, w=220, h=40` (Color: `#0284C7`, Opacity: 0.2)     | | |
| | | Label Tag: `Extracted Field: Turnover = Rs. 62.4 Cr (Confidence: 96%)`    | | |
| | +---------------------------------------------------------------------------+ | |
| +-------------------------------------------------------------------------------+ |
+-----------------------------------------------------------------------------------+
```

---

## 3. Canvas Rendering & Performance Rules

1. **Page Virtualization:** Large multi-hundred-page documents use page virtualization, rendering only visible pages in DOM to prevent client memory bloat.
2. **Bounding Box Highlight Sync:** Hovering over an extracted field in the compliance matrix automatically scrolls the document viewer to the exact page and highlights the bounding box rectangle.
