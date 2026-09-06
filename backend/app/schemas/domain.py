import datetime
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, EmailStr, Field


# --- USER & AUTH SCHEMAS ---
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str
    role: str
    full_name: str


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role: str = "ProcurementOfficer"
    organization_id: str = "CPCL"


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    role: str
    is_active: bool
    organization_id: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True


# --- TENDER & REQUIREMENT SCHEMAS ---
class RequirementCreate(BaseModel):
    requirement_code: str
    category: str
    requirement_text: str
    is_mandatory: bool = True
    metadata_json: Optional[Dict[str, Any]] = None


class RequirementResponse(BaseModel):
    id: str
    tender_version_id: str
    requirement_code: str
    category: str
    requirement_text: str
    is_mandatory: bool
    metadata_json: Optional[Dict[str, Any]] = None
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class TenderVersionCreate(BaseModel):
    version_number: int
    description: Optional[str] = None
    is_finalized: bool = False


class TenderVersionResponse(BaseModel):
    id: str
    tender_id: str
    version_number: int
    description: Optional[str] = None
    publish_date: datetime.datetime
    is_finalized: bool
    requirements: List[RequirementResponse] = []
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class TenderCreate(BaseModel):
    tender_number: str
    title: str
    organization: str = "CPCL"
    description: Optional[str] = None


class TenderResponse(BaseModel):
    id: str
    tender_number: str
    title: str
    organization: str
    status: str
    versions: List[TenderVersionResponse] = []
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True


# --- BIDDER SCHEMAS ---
class BidderCreate(BaseModel):
    bidder_name: str
    registration_number: str
    entity_type: str = "PRIVATE_LIMITED"
    organization_type: str = "MSE"
    pan: Optional[str] = None
    gstin: Optional[str] = None
    udyam: Optional[str] = None


class BidderResponse(BaseModel):
    id: str
    bidder_name: str
    registration_number: str
    entity_type: str
    organization_type: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True


# --- SUBMISSION SCHEMAS ---
class SubmissionCreate(BaseModel):
    bidder_id: str
    tender_id: str
    tender_version_id: str
    submission_reference: str
    cover_type: str = "TECHNICAL"


class SubmissionResponse(BaseModel):
    id: str
    bidder_id: str
    tender_id: str
    tender_version_id: str
    submission_reference: str
    submission_date: datetime.datetime
    status: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True


# --- DOCUMENT SCHEMAS ---
class DocumentRegisterRequest(BaseModel):
    bid_submission_id: str
    submission_cover_id: Optional[str] = None
    original_filename: str
    content_type: str
    file_size_bytes: int
    sha256_hash: str
    storage_ref: str


class DocumentResponse(BaseModel):
    id: str
    bid_submission_id: str
    original_filename: str
    content_type: str
    file_size_bytes: int
    sha256_hash: str
    storage_ref: str
    upload_status: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True


# --- AUDIT SCHEMAS ---
class AuditEventResponse(BaseModel):
    id: str
    actor_id: str
    actor_role: str
    action: str
    resource_type: str
    resource_id: str
    correlation_id: str
    payload_hash: str
    event_payload: Dict[str, Any]
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class AuditChainVerifyResponse(BaseModel):
    is_valid: bool
    total_blocks: int
    verified_blocks: int
    first_corrupted_block: Optional[int] = None
    message: str
