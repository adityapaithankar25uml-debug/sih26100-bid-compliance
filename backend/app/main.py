import time
import uuid
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import settings
from app.core.logging import logger
from app.api.v1.router import api_router
from app.core.security import generate_ulid


def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="0.1.0",
        description="""
### SIH26100 — AI-Powered Integrated Bid Compliance Verification Platform
**Organization:** Ministry of Petroleum & Natural Gas / CPCL  
**Phase:** Phase 2 — Implementation Foundation & Core Platform  
**Core Axiom:** `AI INTERPRETS → AUTHORIZED SOURCES VERIFY → RULES EVALUATE → EVIDENCE PROVES → HUMAN APPROVES`
        """,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Configure CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Middleware: Request Correlation ID & Idempotency Key Propagation
    @app.middleware("http")
    async def add_correlation_and_idempotency_headers(request: Request, call_next):
        correlation_id = request.headers.get("X-Correlation-ID") or generate_ulid()
        idempotency_key = request.headers.get("X-Idempotency-Key")
        request.state.correlation_id = correlation_id
        request.state.idempotency_key = idempotency_key
        start_time = time.time()

        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000
        response.headers["X-Correlation-ID"] = correlation_id
        if idempotency_key:
            response.headers["X-Idempotency-Key"] = idempotency_key
        response.headers["X-Process-Time-MS"] = f"{process_time:.2f}"
        return response

    # RFC 7807 Problem Details Error Handler for HTTP Exceptions
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        correlation_id = getattr(request.state, "correlation_id", "unknown")
        problem_details = {
            "type": f"https://sih26100.cpcl.gov.in/errors/{exc.status_code}",
            "title": exc.detail if isinstance(exc.detail, str) else "HTTP Exception",
            "status": exc.status_code,
            "detail": exc.detail,
            "instance": request.url.path,
            "correlation_id": correlation_id,
        }
        return JSONResponse(
            status_code=exc.status_code,
            content=problem_details,
            headers={"Content-Type": "application/problem+json"},
        )

    # RFC 7807 Validation Exception Handler
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        correlation_id = getattr(request.state, "correlation_id", "unknown")
        problem_details = {
            "type": "https://sih26100.cpcl.gov.in/errors/validation-error",
            "title": "Unprocessable Entity / Validation Error",
            "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "detail": exc.errors(),
            "instance": request.url.path,
            "correlation_id": correlation_id,
        }
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=problem_details,
            headers={"Content-Type": "application/problem+json"},
        )

    # RFC 7807 Unhandled Server Exception Handler (prevents stack trace leakage)
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        correlation_id = getattr(request.state, "correlation_id", "unknown")
        logger.error(
            f"Unhandled exception on path '{request.url.path}'",
            exc_info=exc,
            extra={"correlation_id": correlation_id},
        )
        problem_details = {
            "type": "https://sih26100.cpcl.gov.in/errors/internal-server-error",
            "title": "Internal Server Error",
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "detail": "An internal server error occurred. Please contact system administrator.",
            "instance": request.url.path,
            "correlation_id": correlation_id,
        }
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=problem_details,
            headers={"Content-Type": "application/problem+json"},
        )

    # Include API Router
    app.include_router(api_router, prefix=settings.API_V1_STR)

    @app.on_event("startup")
    def startup_event():
        if settings.SEED_DEMO_DATA:
            try:
                from app.db.session import SessionLocal, Base, engine
                from app.db.seed import seed_database
                Base.metadata.create_all(bind=engine)
                db = SessionLocal()
                try:
                    seed_database(db)
                finally:
                    db.close()
            except Exception as e:
                logger.error(f"Database startup initialization error: {e}")

    return app


app = create_application()
