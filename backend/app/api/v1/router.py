from fastapi import APIRouter
from app.api.v1.endpoints import health, auth, tenders, bidders, submissions, documents, audit

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health & Readiness"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication & Profile"])
api_router.include_router(tenders.router, prefix="/tenders", tags=["Tenders & Requirements"])
api_router.include_router(bidders.router, prefix="/bidders", tags=["Bidders & Identities"])
api_router.include_router(submissions.router, prefix="/submissions", tags=["Bid Submissions"])
api_router.include_router(documents.router, prefix="/documents", tags=["Source Documents"])
api_router.include_router(audit.router, prefix="/audit", tags=["Tamper-Evident Audit Chain"])
