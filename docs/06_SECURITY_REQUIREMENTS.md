# 06 — Security Requirements

## SIH 26100: AI-Powered Integrated Bid Compliance Verification Platform

**Version:** 0.1 (Phase 0)  
**Date:** 2026-09-05

---

## 1. Threat Model

### 1.1 Assets to Protect

| Asset | Classification | Impact if Compromised |
|-------|---------------|----------------------|
| Tender documents (pre-publication) | CONFIDENTIAL | Unfair advantage; bid rigging |
| Bidder financial data | SENSITIVE | Business intelligence theft |
| PAN/GSTIN/CIN identifiers | PII / BUSINESS | Identity theft; impersonation |
| Government API credentials | SECRET | Unauthorized access to government systems |
| Compliance evaluation results | CONFIDENTIAL | Manipulation of procurement decisions |
| Audit logs | INTEGRITY-CRITICAL | Destruction of evidence; cover-up |
| Procurement officer decisions | INTEGRITY-CRITICAL | Decision tampering |
| AI model prompts/weights | PROPRIETARY | Prompt injection; model manipulation |

### 1.2 Threat Actors

| Actor | Motivation | Capability |
|-------|-----------|-----------|
| Malicious bidder | Win contract unfairly | Forged documents, identity manipulation |
| Insider threat (corrupt officer) | Favor specific bidder | System access, decision tampering |
| External attacker | Data theft, disruption | Network attacks, injection, credential theft |
| Competitor (bidder) | Access rival's bid data | Social engineering, insider cooperation |
| Nation-state actor | Strategic disruption | Advanced persistent threats |

### 1.3 Attack Vectors

| Vector | Target | Mitigation |
|--------|--------|-----------|
| Forged documents | Document processing | AI fraud detection + human review |
| Prompt injection | AI extraction/recommendation | Input sanitization; output validation; sandboxing |
| SQL/NoSQL injection | Database | Parameterized queries; ORM |
| XSS/CSRF | Web interface | CSP headers; CSRF tokens; input sanitization |
| API credential theft | Government integrations | Secrets vault; key rotation; audit logging |
| Malicious file upload | Document processing | Malware scanning; file type whitelist; sandboxed processing |
| Session hijacking | User sessions | Secure cookies; MFA; session timeout |
| Audit log tampering | Evidence integrity | Append-only storage; hash chaining; separate access control |
| Man-in-the-middle | Data in transit | TLS 1.2+; certificate pinning for government APIs |

---

## 2. Authentication & Authorization

### 2.1 Authentication
- Multi-factor authentication (MFA) for all users
- Password policy: minimum 12 characters, complexity requirements, rotation every 90 days
- Account lockout after 5 failed attempts
- Session timeout: 30 minutes inactivity
- No shared accounts; every action attributed to an individual

### 2.2 Role-Based Access Control (RBAC)

| Role | Permissions |
|------|------------|
| **Procurement Officer** | Create/manage tenders; add bidders; upload documents; review evaluations; make decisions; view reports |
| **Senior Officer / Approver** | All officer permissions + approve decisions; view all tenders |
| **Auditor** | Read-only access to all evaluations, audit logs, and reports; cannot make decisions |
| **System Administrator** | User management; system configuration; integration management; NO access to tender evaluations |
| **AI System (service account)** | Document processing; field extraction; recommendation generation; NO decision authority |
| **Integration Service** | Government API calls; data retrieval; NO decision authority |

### 2.3 Principle of Least Privilege
- Each role gets minimum permissions needed
- Separation of duties: admin cannot evaluate tenders; officer cannot modify system config
- Temporal access: time-bound access for auditors

---

## 3. Data Protection

### 3.1 Encryption
- **At rest:** AES-256 encryption for all stored data
- **In transit:** TLS 1.2+ for all communications
- **Government API credentials:** Stored in secrets vault (HashiCorp Vault or equivalent)
- **Database encryption:** Transparent Data Encryption (TDE) for database files
- **Document storage:** Encrypted file storage with per-document keys

### 3.2 Data Classification & Handling

| Classification | Examples | Handling |
|---------------|----------|---------|
| PUBLIC | Published tender documents | Standard protection |
| INTERNAL | Evaluation progress, system logs | Access-controlled; encrypted |
| CONFIDENTIAL | Bidder documents, evaluation results | Encrypted; role-based access; audit logged |
| SECRET | Government API keys, admin credentials | Vault-stored; MFA access; rotation policy |

### 3.3 DPDP Act 2023 Compliance
- **Consent:** Obtain bidder consent before processing personal data
- **Purpose limitation:** Data used only for bid compliance evaluation
- **Data minimization:** Collect only data necessary for evaluation
- **Retention policy:** Define and enforce data retention periods
- **Right to erasure:** Support data deletion upon valid request (subject to audit retention requirements)
- **Data breach notification:** Incident response plan with notification procedures

---

## 4. Application Security

### 4.1 Input Validation
- All user inputs validated and sanitized
- File uploads: type validation (magic bytes, not just extension), size limits, malware scanning
- API inputs: schema validation; parameter type checking
- AI inputs: prompt sanitization; injection-resistant prompt engineering

### 4.2 Output Security
- AI outputs validated against expected schemas
- No raw error messages exposed to users
- Content Security Policy (CSP) headers
- X-Frame-Options, X-Content-Type-Options headers

### 4.3 API Security
- Rate limiting on all endpoints
- API key authentication for service-to-service calls
- Request/response logging for audit trail
- Input size limits to prevent denial of service

---

## 5. Audit & Evidence Integrity

### 5.1 Audit Log Architecture
- Append-only log storage (no UPDATE or DELETE operations)
- Hash chaining: each log entry includes hash of previous entry
- Separate access control from application data (auditors can read; no one can modify)
- Timestamp from trusted time source (NTP-synchronized)

### 5.2 Evidence Integrity
- Every uploaded document hashed (SHA-256) upon receipt
- Hash stored separately from document
- Evidence chain: every decision links to its supporting evidence
- Document tampering detection via hash verification

### 5.3 Audit Log Contents
Every log entry includes:
- Timestamp (UTC)
- Actor (user ID or system component)
- Action type
- Target (document/bidder/tender/rule)
- Before state (for modifications)
- After state (for modifications)
- IP address
- Session ID
- Request ID (for traceability)

---

## 6. Infrastructure Security

### 6.1 Network
- Network segmentation: separate application, database, and AI service networks
- Firewall rules: allow only necessary traffic
- Government API calls from dedicated egress IP
- No direct database access from internet

### 6.2 Container Security
- Minimal base images (Alpine/Distroless)
- No root processes in containers
- Read-only file systems where possible
- Regular vulnerability scanning

### 6.3 Secrets Management
- No secrets in code, environment variables (for production), or config files
- Secrets vault with access auditing
- Key rotation policy
- Separate secrets per environment (dev/staging/production)

---

## 7. SIH Demo Security Considerations

For the hackathon demonstration:
- Use synthetic/mock data only — no real PAN, GSTIN, or personal data
- Demo credentials clearly marked as non-production
- Mock government APIs clearly labelled
- No real government API calls during demo
- Focus security demo on: RBAC, audit trail, evidence chain, AI transparency
