# Phase 1 — Vendor-Neutral Observability Tooling & Abstraction Architecture

**Document Control Information**
- **Project Name:** SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform for GeM Procurement
- **Organization:** Ministry of Petroleum & Natural Gas / CPCL
- **Document Version:** 1.0.0 (Phase 1 — Task 9 Observability Tooling Specification)
- **Status:** DESIGN DRAFT / PENDING REVIEW
- **Security Classification:** INTERNAL
- **Mode:** DESIGN ONLY — ZERO CODE IMPLEMENTATION

---

## 1. Executive Summary & Purpose

This specification defines the vendor-neutral telemetry abstraction layer and conceptual observability tooling architecture for the SIH26100 platform. The architecture evaluates conceptual compatibility with open standards (OpenTelemetry, Prometheus, Grafana, OpenSearch) without installing packages, writing integration code, or locking the platform to specific cloud vendors.

The foundational tooling principle is:
> **"Observability tooling uses open, vendor-neutral telemetry abstractions (`TelemetryProviderInterface`). The application core emits standardized telemetry formats compatible with on-premise open-source stacks as well as government cloud infrastructures."**

---

## 2. Vendor-Neutral Telemetry Abstraction Architecture

```mermaid
graph TD
    subgraph App_Core ["Application Subsystems"]
        FastAPI_App["API Service"]
        Celery_App["Celery Worker"]
        Rule_App["AST Rule Engine"]
    end

    subgraph Telemetry_Abstraction ["Vendor-Neutral Telemetry Interface"]
        TelemetryInterface["TelemetryProviderInterface (Logs, Metrics, Traces)"]
    end

    subgraph Monitoring_Stack ["Conceptual Observability Infrastructure (Design Only)"]
        LogCollector["Structured Log Collector (OpenSearch / FluentBit)"]
        TSDB["Time Series DB (Prometheus / VictoriaMetrics)"]
        TraceCollector["Distributed Trace Collector (OpenTelemetry / Jaeger)"]
    end

    FastAPI_App --> TelemetryInterface
    Celery_App --> TelemetryInterface
    Rule_App --> TelemetryInterface

    TelemetryInterface -.->|OpenTelemetry Protocol (OTLP)| LogCollector
    TelemetryInterface -.->|Prometheus Scraping / OTLP| TSDB
    TelemetryInterface -.->|OTLP Trace Spans| TraceCollector
```

---

## 3. Conceptual Compatibility Evaluation Matrix

The platform evaluates conceptual compatibility across four core observability tooling domains:

| Observability Domain | Open-Source / Standard Option | Cloud-Native / Enterprise Option | Architectural Compatibility Evaluation |
|---|---|---|---|
| **Log Aggregation** | OpenSearch / FluentBit | AWS CloudWatch Logs / Azure Monitor | Compatible. Application emits structured JSON logs over stdout/OTLP; log collectors ingest without application code modifications. |
| **Metrics Collection** | Prometheus / VictoriaMetrics | Amazon Managed Prometheus | Compatible. Application exposes standardized `/metrics` endpoints or exports OTLP metrics. |
| **Distributed Tracing** | OpenTelemetry Collector / Jaeger | AWS X-Ray / Azure Application Insights | Compatible. Context propagation uses standard W3C `traceparent` headers. |
| **Visualization & Dashboards** | Grafana | Amazon Managed Grafana | Compatible. Dashboard definitions (`DashboardDefinition`) export to standard JSON format. |

---

## 4. Vendor Lock-In Prevention Principles

1. **Zero Proprietary SDKs:** Application specifications mandate OpenTelemetry standard APIs. Proprietary vendor SDKs (e.g., AWS CloudWatch SDK or Datadog SDK) are strictly excluded from core application code.
2. **OTLP Standard Exporter:** Telemetry data exports utilize OpenTelemetry Protocol (OTLP) over gRPC/HTTP, allowing switching between on-premise Grafana stacks and cloud-hosted monitoring platforms by modifying collector endpoint configurations.
3. **Zero Package Installations in Task 9:** Zero monitoring packages (`opentelemetry-api`, `prometheus-client`, `grafana-api`) are installed or configured in Task 9. All tooling specifications remain conceptual documentation.
