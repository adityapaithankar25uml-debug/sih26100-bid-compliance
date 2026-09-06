import pytest
from fastapi.testclient import TestClient
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

TEST_DB_FILE = "./test_runner.db"
SQLALCHEMY_TEST_DATABASE_URL = f"sqlite:///{TEST_DB_FILE}"

# Force file-backed SQLite database URL for pytest runner
settings.DATABASE_URL = SQLALCHEMY_TEST_DATABASE_URL


import app.db.session as db_session
from app.db.session import Base, get_db
from app.main import app
from app.models.domain import User
from app.core.security import get_password_hash, create_access_token

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override main application engine and SessionLocal for test suite
db_session.engine = engine
db_session.SessionLocal = TestingSessionLocal





@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    def _override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_officer_user(db):
    user = User(
        email="officer_test@cpcl.gov.in",
        full_name="Test Procurement Officer",
        hashed_password=get_password_hash("TestPass123!"),
        role="ProcurementOfficer",
        organization_id="CPCL",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture(scope="function")
def test_auditor_user(db):
    user = User(
        email="auditor_test@cpcl.gov.in",
        full_name="Test Auditor",
        hashed_password=get_password_hash("TestPass123!"),
        role="Auditor",
        organization_id="CPCL",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture(scope="function")
def officer_headers(test_officer_user):
    token = create_access_token(subject=test_officer_user.id, role=test_officer_user.role)
    return {"Authorization": f"Bearer {token}", "X-Correlation-ID": "TEST-CORRELATION-001"}


@pytest.fixture(scope="function")
def auditor_headers(test_auditor_user):
    token = create_access_token(subject=test_auditor_user.id, role=test_auditor_user.role)
    return {"Authorization": f"Bearer {token}", "X-Correlation-ID": "TEST-CORRELATION-AUDIT"}
