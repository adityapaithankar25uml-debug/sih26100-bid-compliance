from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.v1.deps import get_db, get_current_user, get_correlation_id
from app.schemas.domain import LoginRequest, TokenResponse, UserResponse
from app.services.auth_service import AuthService
from app.services.audit_service import AuditService
from app.core.security import create_access_token
from app.models.domain import User

router = APIRouter()


@router.post("/login", response_model=TokenResponse, summary="Development/Demo User Authentication")
def login(
    req: LoginRequest,
    db: Session = Depends(get_db),
    correlation_id: str = Depends(get_correlation_id),
):
    user = AuthService.authenticate_user(db, req.email, req.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
        )

    access_token = create_access_token(subject=user.id, role=user.role)

    # Log user authentication audit event
    AuditService.log_event(
        db=db,
        actor_id=user.id,
        actor_role=user.role,
        action="USER_AUTHENTICATED",
        resource_type="User",
        resource_id=user.id,
        correlation_id=correlation_id,
        payload={"email": user.email, "role": user.role},
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        email=user.email,
        role=user.role,
        full_name=user.full_name,
    )


@router.get("/me", response_model=UserResponse, summary="Get Current Authenticated User Profile")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
