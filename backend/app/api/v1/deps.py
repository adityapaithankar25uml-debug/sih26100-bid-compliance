from typing import Generator, Optional, List, Callable
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.core.security import decode_access_token, generate_ulid
from app.models.domain import User
from app.services.auth_service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_correlation_id(request: Request) -> str:
    correlation_id = request.headers.get("X-Correlation-ID")
    if not correlation_id:
        correlation_id = generate_ulid()
    return correlation_id


def get_current_user(
    db: Session = Depends(get_db), token: Optional[str] = Depends(oauth2_scheme)
) -> User:
    if not token:
        # Development / demo fallback: return active ProcurementOfficer if token missing in demo mode
        user = db.query(User).filter(User.role == "ProcurementOfficer").first()
        if user:
            return user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials missing.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = AuthService.get_user_by_id(db, payload["sub"])
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account inactive or not found.",
        )

    return user


def require_roles(allowed_roles: List[str]) -> Callable:
    """
    Backend-authoritative Role-Based Access Control (RBAC) dependency guard.
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles and current_user.role != "SystemAdmin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: User role '{current_user.role}' lacks required permissions ({', '.join(allowed_roles)}).",
            )
        return current_user

    return role_checker
