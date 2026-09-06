import re
from typing import Dict, Any, List, Tuple


class PrivacyGatewayService:
    # Strict Phase 1 Security Classification Taxonomy ONLY
    CLASSIFICATIONS = {"PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED", "PII"}

    # PII Detection Patterns
    PAN_PATTERN = re.compile(r"[A-Z]{5}[0-9]{4}[A-Z]{1}")
    GSTIN_PATTERN = re.compile(r"[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}")
    AADHAAR_PATTERN = re.compile(r"\b[2-9]{1}[0-9]{3}\s?[0-9]{4}\s?[0-9]{4}\b")
    EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
    PHONE_PATTERN = re.compile(r"\b(?:\+91[\-\s]?)?[6-9]\d{9}\b")
    BANK_ACC_PATTERN = re.compile(r"\b[0-9]{9,18}\b")

    # Prompt Injection Suspicious Phrases
    PROMPT_INJECTION_PHRASES = [
        "ignore previous instructions",
        "ignore all previous instructions",
        "system prompt",
        "mark qualified",
        "mark compliant",
        "override status",
        "drop table",
        "call external api",
        "delete evidence",
        "bypass rule",
    ]

    def detect_pii(self, text: str) -> Dict[str, List[str]]:
        detected = {}
        pan_matches = self.PAN_PATTERN.findall(text)
        if pan_matches:
            detected["PAN"] = list(set(pan_matches))

        gst_matches = self.GSTIN_PATTERN.findall(text)
        if gst_matches:
            detected["GSTIN"] = list(set(gst_matches))

        aadhaar_matches = self.AADHAAR_PATTERN.findall(text)
        if aadhaar_matches:
            detected["AADHAAR"] = list(set(aadhaar_matches))

        email_matches = self.EMAIL_PATTERN.findall(text)
        if email_matches:
            detected["EMAIL"] = list(set(email_matches))

        phone_matches = self.PHONE_PATTERN.findall(text)
        if phone_matches:
            detected["PHONE"] = list(set(phone_matches))

        return detected

    def evaluate_sensitivity(self, doc_type: str, text: str) -> Tuple[str, bool, List[str], str]:
        """
        Evaluates security classification, PII presence, and cloud eligibility.
        Returns: (security_classification, pii_detected, pii_flags, cloud_eligibility)
        """
        pii_dict = self.detect_pii(text)
        pii_detected = len(pii_dict) > 0
        pii_flags = list(pii_dict.keys())

        # Determine security classification (PUBLIC | INTERNAL | CONFIDENTIAL | RESTRICTED | PII)
        if "AADHAAR" in pii_dict:
            classification = "PII"
            eligibility = "LOCAL_ONLY"
        elif doc_type in {"CA_TURNOVER_CERTIFICATE", "PAST_EXPERIENCE_ORDER"}:
            classification = "CONFIDENTIAL"
            eligibility = "SANITIZE_THEN_EXTERNAL_AI" if pii_detected else "ELIGIBLE_EXTERNAL_AI"
        elif doc_type in {"GST_REGISTRATION_CERTIFICATE", "UDYAM_REGISTRATION_CERTIFICATE", "PAN_CARD"}:
            classification = "RESTRICTED"
            eligibility = "ELIGIBLE_EXTERNAL_AI"
        elif doc_type == "TENDER_DOCUMENT":
            classification = "PUBLIC"
            eligibility = "ELIGIBLE_EXTERNAL_AI"
        else:
            classification = "INTERNAL"
            eligibility = "ELIGIBLE_EXTERNAL_AI"

        return classification, pii_detected, pii_flags, eligibility

    def sanitize_for_ai(self, text: str, eligibility: str) -> str:
        """
        Applies data minimization & prompt injection sandboxing delimiters.
        """
        sanitized = text

        # Mask Aadhaar numbers unconditionally
        sanitized = self.AADHAAR_PATTERN.sub("[REDACTED_AADHAAR]", sanitized)

        # Wrap in strict untrusted document delimiters
        sandboxed = (
            "<<<UNTRUSTED_DOC_CONTENT>>>\n"
            f"{sanitized}\n"
            "<<<END_UNTRUSTED_DOC_CONTENT>>>"
        )
        return sandboxed

    def inspect_prompt_injection(self, text: str) -> Tuple[bool, List[str]]:
        """Scans extracted text for malicious instruction attempts."""
        text_lower = text.lower()
        found_phrases = [phrase for phrase in self.PROMPT_INJECTION_PHRASES if phrase in text_lower]
        has_injection = len(found_phrases) > 0
        return has_injection, found_phrases


privacy_gateway = PrivacyGatewayService()
