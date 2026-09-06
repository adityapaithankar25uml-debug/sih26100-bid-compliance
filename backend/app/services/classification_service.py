from typing import Dict, Any, Tuple, Optional
from app.core.config import settings


class DocumentClassificationService:
    TAXONOMY_KEYWORDS = {
        "CA_TURNOVER_CERTIFICATE": ["turnover", "chartered accountant", "ca certificate", "net worth", "annual turnover"],
        "GST_REGISTRATION_CERTIFICATE": ["gstin", "goods and services tax", "form gst reg-06", "registration certificate"],
        "UDYAM_REGISTRATION_CERTIFICATE": ["udyam", "msme", "micro, small & medium", "udyam registration"],
        "PAN_CARD": ["income tax department", "permanent account number", "pan card"],
        "EMD_PAYMENT_RECEIPT": ["emd", "earnest money deposit", "payment receipt", "bank guarantee"],
        "DEBARMENT_AFFIDAVIT": ["affidavit", "non-debarment", "blacklisting", "notary", "stamp paper"],
        "TECHNICAL_SPECIFICATION_SHEET": ["technical specification", "data sheet", "datasheet", "compliance sheet"],
        "PAST_EXPERIENCE_ORDER": ["purchase order", "work order", "completion certificate", "experience order"],
        "ISO_CERTIFICATE": ["iso 9001", "iso 14001", "iso 45001", "management system certificate"],
        "TENDER_DOCUMENT": ["notice inviting tender", "nit", "tender document", "request for proposal", "rfp", "cpcl"],
    }

    def classify_document(
        self,
        text: str,
        filename: str,
        threshold: float = None
    ) -> Tuple[str, float, bool, str]:
        """
        Classifies document text based on heuristic pattern matching.
        The human-review threshold is configurable per environment/task via settings.CLASSIFICATION_CONFIDENCE_THRESHOLD.
        Returns: (predicted_doc_type, confidence_score, requires_human_review, method)
        """
        if threshold is None:
            threshold = getattr(settings, "CLASSIFICATION_CONFIDENCE_THRESHOLD", 0.70)

        content_lower = (text + " " + filename).lower()

        scores: Dict[str, int] = {}
        for doc_type, keywords in self.TAXONOMY_KEYWORDS.items():
            matches = sum(1 for kw in keywords if kw in content_lower)
            if matches > 0:
                scores[doc_type] = matches

        if not scores:
            return "OTHER_UNCLASSIFIED", 0.40, True, "HEURISTIC"

        best_type = max(scores, key=scores.get)
        match_count = scores[best_type]
        
        # Calculate confidence
        confidence = min(0.50 + (match_count * 0.15), 0.98)
        requires_review = confidence < threshold

        return best_type, confidence, requires_review, "HEURISTIC"


classification_service = DocumentClassificationService()
