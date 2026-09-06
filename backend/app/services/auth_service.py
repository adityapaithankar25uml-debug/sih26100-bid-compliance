from typing import Optional
from sqlalchemy.orm import Session
from app.models.domain import User
from app.schemas.domain import UserCreate
from app.core.security import verify_password, get_password_hash, create_access_token


class AuthService:

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    @classmethod
    def create_user(cls, db: Session, user_in: UserCreate) -> User:
        hashed_password = get_password_hash(user_in.password)
        user = User(
            email=user_in.email,
            full_name=user_in.full_name,
            hashed_password=hashed_password,
            role=user_in.role,
            organization_id=user_in.organization_id,
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @classmethod
    def authenticate_user(cls, db: Session, email: str, password: str) -> Optional[User]:
        user = cls.get_user_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
