import abc
import datetime
import hashlib
import uuid
from typing import Dict, Any, Tuple, Optional, List


class GovernmentVerificationAdapter(abc.ABC):
    """Abstract contract for all government verification adapters."""

    @property
    @abc.abstractmethod
    def source_code(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def authority_type(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def default_integration_mode(self) -> str:
        pass

    @abc.abstractmethod
    def verify(
        self,
        identifier_value: str,
        bidder_context: Optional[Dict[str, Any]] = None,
        integration_mode: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes verification against external or mock adapter.
        Returns normalized dictionary with technical_status, business_status, identity_match_status, normalized_facts, raw_response_hash.
        """
        pass


class GSTAdapter(GovernmentVerificationAdapter):
    source_code = "GST"
    authority_type = "GSTN_TAX_AUTHORITY"
    default_integration_mode = "MOCK"

    def verify(
        self,
        identifier_value: str,
        bidder_context: Optional[Dict[str, Any]] = None,
        integration_mode: Optional[str] = None
    ) -> Dict[str, Any]:
        mode = integration_mode or self.default_integration_mode
        gstin = identifier_value.strip().upper()

        # Simulated synthetic mock records
        if "TIMEOUT" in gstin:
            return {
                "source_code": self.source_code,
                "adapter_name": "GSTAdapter",
                "integration_mode": mode,
                "technical_status": "TIMEOUT",
                "business_status": "UNKNOWN",
                "source_authority_type": self.authority_type,
                "identity_match_status": "NOT_VERIFIED",
                "raw_response_hash": None,
                "normalized_facts": {}
            }
        elif "INACTIVE" in gstin or gstin.endswith("9Z9"):
            bus_status = "INACTIVE"

            legal_name = "DEMO INACTIVE SUPPLIERS PRIVATE LIMITED"
            active_flag = False
        elif "CANCELLED" in gstin or gstin.endswith("8Z8"):
            bus_status = "CANCELLED"
            legal_name = "DEMO CANCELLED ENTITY PVT LTD"
            active_flag = False
        else:
            bus_status = "VERIFIED"
            legal_name = (bidder_context or {}).get("legal_name", "ACME INDUSTRIAL SYSTEMS PRIVATE LIMITED")
            active_flag = True

        # Identity matching against bidder_context
        match_status = "MATCHED"
        if bidder_context and bidder_context.get("legal_name"):
            expected = bidder_context["legal_name"].lower()
            actual = legal_name.lower()
            if expected != actual and not (expected in actual or actual in expected):
                match_status = "MISMATCH"

        raw_payload = f"GSTIN:{gstin}|LEGAL:{legal_name}|STATUS:{bus_status}|MODE:{mode}"
        raw_hash = hashlib.sha256(raw_payload.encode()).hexdigest()

        return {
            "source_code": self.source_code,
            "adapter_name": "GSTAdapter",
            "integration_mode": mode,
            "technical_status": "SUCCESS",
            "business_status": bus_status,
            "source_authority_type": self.authority_type,
            "identity_match_status": match_status,
            "raw_response_hash": raw_hash,
            "normalized_facts": {
                "gstin": gstin,
                "legal_name": legal_name,
                "gst_status": "ACTIVE" if active_flag else "INACTIVE",
                "registration_date": "2018-07-01",
                "taxpayer_type": "REGULAR",
                "state_code": gstin[:2] if len(gstin) >= 2 else "33",
                "returns_filed_up_to_date": True
            }
        }


class UdyamAdapter(GovernmentVerificationAdapter):
    source_code = "UDYAM"
    authority_type = "MSME_MINISTRY"
    default_integration_mode = "MOCK"

    def verify(
        self,
        identifier_value: str,
        bidder_context: Optional[Dict[str, Any]] = None,
        integration_mode: Optional[str] = None
    ) -> Dict[str, Any]:
        mode = integration_mode or self.default_integration_mode
        udyam_no = identifier_value.strip().upper()

        if "EXPIRED" in udyam_no or udyam_no.endswith("000"):
            bus_status = "INACTIVE"
            category = "MICRO"
            active_flag = False
        else:
            bus_status = "VERIFIED"
            category = "SMALL"
            active_flag = True

        raw_payload = f"UDYAM:{udyam_no}|STATUS:{bus_status}|MODE:{mode}"
        raw_hash = hashlib.sha256(raw_payload.encode()).hexdigest()

        return {
            "source_code": self.source_code,
            "adapter_name": "UdyamAdapter",
            "integration_mode": mode,
            "technical_status": "SUCCESS",
            "business_status": bus_status,
            "source_authority_type": self.authority_type,
            "identity_match_status": "MATCHED",
            "raw_response_hash": raw_hash,
            "normalized_facts": {
                "udyam_number": udyam_no,
                "enterprise_name": (bidder_context or {}).get("legal_name", "ACME INDUSTRIAL SYSTEMS PRIVATE LIMITED"),
                "enterprise_category": category,
                "msme_status": "ACTIVE" if active_flag else "INACTIVE",
                "major_activity": "MANUFACTURING",
                "date_of_commencement": "2019-04-01"
            }
        }


class PANAdapter(GovernmentVerificationAdapter):
    source_code = "PAN"
    authority_type = "INCOME_TAX_DEPARTMENT"
    default_integration_mode = "MOCK"

    def verify(
        self,
        identifier_value: str,
        bidder_context: Optional[Dict[str, Any]] = None,
        integration_mode: Optional[str] = None
    ) -> Dict[str, Any]:
        mode = integration_mode or self.default_integration_mode
        pan = identifier_value.strip().upper()

        bus_status = "VERIFIED" if len(pan) == 10 and pan[:5].isalpha() else "NOT_FOUND"

        raw_payload = f"PAN:{pan}|STATUS:{bus_status}|MODE:{mode}"
        raw_hash = hashlib.sha256(raw_payload.encode()).hexdigest()

        return {
            "source_code": self.source_code,
            "adapter_name": "PANAdapter",
            "integration_mode": mode,
            "technical_status": "SUCCESS",
            "business_status": bus_status,
            "source_authority_type": self.authority_type,
            "identity_match_status": "MATCHED" if bus_status == "VERIFIED" else "MISMATCH",
            "raw_response_hash": raw_hash,
            "normalized_facts": {
                "pan_number": pan,
                "name_on_pan": (bidder_context or {}).get("legal_name", "ACME INDUSTRIAL SYSTEMS PRIVATE LIMITED"),
                "pan_status": "VALID" if bus_status == "VERIFIED" else "INVALID",
                "category": "COMPANY"
            }
        }


class MCAAdapter(GovernmentVerificationAdapter):
    source_code = "MCA"
    authority_type = "MINISTRY_OF_CORPORATE_AFFAIRS"
    default_integration_mode = "MOCK"

    def verify(
        self,
        identifier_value: str,
        bidder_context: Optional[Dict[str, Any]] = None,
        integration_mode: Optional[str] = None
    ) -> Dict[str, Any]:
        mode = integration_mode or self.default_integration_mode
        cin = identifier_value.strip().upper()

        bus_status = "VERIFIED" if len(cin) >= 5 else "NOT_FOUND"

        raw_payload = f"CIN:{cin}|STATUS:{bus_status}|MODE:{mode}"
        raw_hash = hashlib.sha256(raw_payload.encode()).hexdigest()

        return {
            "source_code": self.source_code,
            "adapter_name": "MCAAdapter",
            "integration_mode": mode,
            "technical_status": "SUCCESS",
            "business_status": bus_status,
            "source_authority_type": self.authority_type,
            "identity_match_status": "MATCHED",
            "raw_response_hash": raw_hash,
            "normalized_facts": {
                "cin_number": cin,
                "company_name": (bidder_context or {}).get("legal_name", "ACME INDUSTRIAL SYSTEMS PRIVATE LIMITED"),
                "company_status": "ACTIVE",
                "class_of_company": "PRIVATE",
                "date_of_incorporation": "2015-06-15"
            }
        }


class EPFOAdapter(GovernmentVerificationAdapter):
    source_code = "EPFO"
    authority_type = "EPFO_LABOUR_MINISTRY"
    default_integration_mode = "MOCK"

    def verify(self, identifier_value: str, bidder_context: Optional[Dict[str, Any]] = None, integration_mode: Optional[str] = None) -> Dict[str, Any]:
        return {
            "source_code": self.source_code,
            "adapter_name": "EPFOAdapter",
            "integration_mode": integration_mode or self.default_integration_mode,
            "technical_status": "SUCCESS",
            "business_status": "VERIFIED",
            "source_authority_type": self.authority_type,
            "identity_match_status": "MATCHED",
            "raw_response_hash": hashlib.sha256(identifier_value.encode()).hexdigest(),
            "normalized_facts": {
                "epfo_establishment_code": identifier_value,
                "epfo_registration_status": "ACTIVE",
                "active_subscribers_count": 45
            }
        }


class ESICAdapter(GovernmentVerificationAdapter):
    source_code = "ESIC"
    authority_type = "ESIC_LABOUR_MINISTRY"
    default_integration_mode = "MOCK"

    def verify(self, identifier_value: str, bidder_context: Optional[Dict[str, Any]] = None, integration_mode: Optional[str] = None) -> Dict[str, Any]:
        return {
            "source_code": self.source_code,
            "adapter_name": "ESICAdapter",
            "integration_mode": integration_mode or self.default_integration_mode,
            "technical_status": "SUCCESS",
            "business_status": "VERIFIED",
            "source_authority_type": self.authority_type,
            "identity_match_status": "MATCHED",
            "raw_response_hash": hashlib.sha256(identifier_value.encode()).hexdigest(),
            "normalized_facts": {
                "esic_code": identifier_value,
                "esic_registration_status": "ACTIVE"
            }
        }


class StartupIndiaAdapter(GovernmentVerificationAdapter):
    source_code = "STARTUP_INDIA"
    authority_type = "DPIIT_COMMERCE_MINISTRY"
    default_integration_mode = "MOCK"

    def verify(self, identifier_value: str, bidder_context: Optional[Dict[str, Any]] = None, integration_mode: Optional[str] = None) -> Dict[str, Any]:
        return {
            "source_code": self.source_code,
            "adapter_name": "StartupIndiaAdapter",
            "integration_mode": integration_mode or self.default_integration_mode,
            "technical_status": "SUCCESS",
            "business_status": "VERIFIED",
            "source_authority_type": self.authority_type,
            "identity_match_status": "MATCHED",
            "raw_response_hash": hashlib.sha256(identifier_value.encode()).hexdigest(),
            "normalized_facts": {
                "dpiit_recognition_number": identifier_value,
                "startup_status": "RECOGNIZED",
                "recognition_date": "2021-03-10"
            }
        }


class NSICAdapter(GovernmentVerificationAdapter):
    source_code = "NSIC"
    authority_type = "NATIONAL_SMALL_INDUSTRIES_CORP"
    default_integration_mode = "MOCK"

    def verify(self, identifier_value: str, bidder_context: Optional[Dict[str, Any]] = None, integration_mode: Optional[str] = None) -> Dict[str, Any]:
        return {
            "source_code": self.source_code,
            "adapter_name": "NSICAdapter",
            "integration_mode": integration_mode or self.default_integration_mode,
            "technical_status": "SUCCESS",
            "business_status": "VERIFIED",
            "source_authority_type": self.authority_type,
            "identity_match_status": "MATCHED",
            "raw_response_hash": hashlib.sha256(identifier_value.encode()).hexdigest(),
            "normalized_facts": {
                "nsic_certificate_number": identifier_value,
                "nsic_status": "VALID",
                "monetary_limit_lakhs": 500
            }
        }


class OEMAuthorizationAdapter(GovernmentVerificationAdapter):
    source_code = "OEM_AUTH"
    authority_type = "OEM_VENDOR_REGISTRY"
    default_integration_mode = "MOCK"

    def verify(self, identifier_value: str, bidder_context: Optional[Dict[str, Any]] = None, integration_mode: Optional[str] = None) -> Dict[str, Any]:
        return {
            "source_code": self.source_code,
            "adapter_name": "OEMAuthorizationAdapter",
            "integration_mode": integration_mode or self.default_integration_mode,
            "technical_status": "SUCCESS",
            "business_status": "VERIFIED",
            "source_authority_type": self.authority_type,
            "identity_match_status": "MATCHED",
            "raw_response_hash": hashlib.sha256(identifier_value.encode()).hexdigest(),
            "normalized_facts": {
                "oem_name": "GLOBAL TECH INSTRUMENTS INC",
                "authorization_code": identifier_value,
                "authorization_status": "VALID",
                "valid_until": "2027-12-31"
            }
        }


class DebarmentAdapter(GovernmentVerificationAdapter):
    source_code = "DEBARMENT"
    authority_type = "GEM_CPPP_ADMINISTRATIVE_AUTHORITY"
    default_integration_mode = "MOCK"

    def verify(
        self,
        identifier_value: str,
        bidder_context: Optional[Dict[str, Any]] = None,
        integration_mode: Optional[str] = None
    ) -> Dict[str, Any]:
        mode = integration_mode or self.default_integration_mode
        vendor_id = identifier_value.strip().upper()

        if "DEBARRED" in vendor_id or vendor_id.endswith("BLACK"):
            bus_status = "DEBARRED"
            debarred_flag = True
        else:
            bus_status = "NOT_DEBARRED"
            debarred_flag = False

        raw_payload = f"DEBARMENT:{vendor_id}|STATUS:{bus_status}|MODE:{mode}"
        raw_hash = hashlib.sha256(raw_payload.encode()).hexdigest()

        return {
            "source_code": self.source_code,
            "adapter_name": "DebarmentAdapter",
            "integration_mode": mode,
            "technical_status": "SUCCESS",
            "business_status": bus_status,
            "source_authority_type": self.authority_type,
            "identity_match_status": "MATCHED",
            "raw_response_hash": raw_hash,
            "normalized_facts": {
                "vendor_id": vendor_id,
                "debarment_status": "DEBARRED" if debarred_flag else "NOT_DEBARRED",
                "debarment_reason": "Non-performance on CPCL Order" if debarred_flag else None,
                "debarment_end_date": "2027-06-30" if debarred_flag else None
            }
        }


class GeMProfileAdapter(GovernmentVerificationAdapter):
    source_code = "GEM_PROFILE"
    authority_type = "GEM_PROCUREMENT_PORTAL"
    default_integration_mode = "MOCK"

    def verify(self, identifier_value: str, bidder_context: Optional[Dict[str, Any]] = None, integration_mode: Optional[str] = None) -> Dict[str, Any]:
        return {
            "source_code": self.source_code,
            "adapter_name": "GeMProfileAdapter",
            "integration_mode": integration_mode or self.default_integration_mode,
            "technical_status": "SUCCESS",
            "business_status": "VERIFIED",
            "source_authority_type": self.authority_type,
            "identity_match_status": "MATCHED",
            "raw_response_hash": hashlib.sha256(identifier_value.encode()).hexdigest(),
            "normalized_facts": {
                "gem_seller_id": identifier_value,
                "verification_status": "VERIFIED_SELLER",
                "vendor_assessment_status": "COMPLETED"
            }
        }


class DigiLockerAdapter(GovernmentVerificationAdapter):
    source_code = "DIGILOCKER"
    authority_type = "MEITY_DIGILOCKER_ISSUER"
    default_integration_mode = "MOCK"

    def verify(self, identifier_value: str, bidder_context: Optional[Dict[str, Any]] = None, integration_mode: Optional[str] = None) -> Dict[str, Any]:
        return {
            "source_code": self.source_code,
            "adapter_name": "DigiLockerAdapter",
            "integration_mode": integration_mode or self.default_integration_mode,
            "technical_status": "SUCCESS",
            "business_status": "VERIFIED",
            "source_authority_type": self.authority_type,
            "identity_match_status": "MATCHED",
            "raw_response_hash": hashlib.sha256(identifier_value.encode()).hexdigest(),
            "normalized_facts": {
                "digilocker_uri": identifier_value,
                "issuer_name": "Income Tax Department / GSTN",
                "doc_verification_status": "DIGITALLY_VERIFIED"
            }
        }


class GovernmentAdapterRegistry:
    def __init__(self):
        self._adapters: Dict[str, GovernmentVerificationAdapter] = {
            "GST": GSTAdapter(),
            "UDYAM": UdyamAdapter(),
            "PAN": PANAdapter(),
            "MCA": MCAAdapter(),
            "EPFO": EPFOAdapter(),
            "ESIC": ESICAdapter(),
            "STARTUP_INDIA": StartupIndiaAdapter(),
            "NSIC": NSICAdapter(),
            "OEM_AUTH": OEMAuthorizationAdapter(),
            "DEBARMENT": DebarmentAdapter(),
            "GEM_PROFILE": GeMProfileAdapter(),
            "DIGILOCKER": DigiLockerAdapter(),
        }

    def get_adapter(self, source_code: str) -> Optional[GovernmentVerificationAdapter]:
        return self._adapters.get(source_code.upper())

    def list_sources(self) -> List[Dict[str, Any]]:
        return [
            {
                "source_code": code,
                "adapter_name": adapter.__class__.__name__,
                "authority_type": adapter.authority_type,
                "default_mode": adapter.default_integration_mode
            }
            for code, adapter in self._adapters.items()
        ]


adapter_registry = GovernmentAdapterRegistry()

# Alias for backward compatibility
OEMAuthAdapter = OEMAuthorizationAdapter

