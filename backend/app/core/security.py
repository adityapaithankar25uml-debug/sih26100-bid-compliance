import datetime
import re
from typing import Any, Dict, Optional
from ulid import ULID
import jwt
from passlib.context import CryptContext
from app.core.config import settings

# Crockford Base32 Alphabet: 0123456789ABCDEFGHJKMNPQRSTVWXYZ (excludes I, L, O, U)
CROCKFORD_BASE32_REGEX = re.compile(r"^[0123456789ABCDEFGHJKMNPQRSTVWXYZ]{26}$", re.IGNORECASE)

# Password Hashing Context using Argon2id with bcrypt fallback
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")



def generate_ulid() -> str:
    """
    Generates a 26-character Crockford Base32 ULID (time-ordered, 128-bit sortable ID).
    """
    return str(ULID())



def is_valid_ulid(ulid_str: str) -> bool:
    """
    Validates whether a string is a 26-character Crockford Base32 ULID.
    """
    if not ulid_str or len(ulid_str) != 26:
        return False
    return bool(CROCKFORD_BASE32_REGEX.match(ulid_str))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against an Argon2id/bcrypt hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hashes a password using Argon2id.
    """
    return pwd_context.hash(password)


def create_access_token(subject: str, role: str, expires_delta: Optional[datetime.timedelta] = None) -> str:
    """
    Creates a signed JWT access token containing subject (user_id) and role claims.
    """
    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode: Dict[str, Any] = {
        "exp": expire,
        "sub": str(subject),
        "role": str(role),
        "iat": datetime.datetime.now(datetime.timezone.utc),
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decodes and verifies a JWT access token.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None
