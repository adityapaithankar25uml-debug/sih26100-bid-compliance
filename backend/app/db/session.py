from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.core.config import settings

# SQLAlchemy declarative base
Base = declarative_base()

db_url = settings.get_database_url()
connect_args = {"check_same_thread": False} if db_url.startswith("sqlite") else {}

# Create SQLAlchemy engine with connection pool settings
engine = create_engine(
    db_url,
    connect_args=connect_args,
    pool_pre_ping=True,
    future=True,
)


# Session local factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency for managing database session lifecycle per request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
