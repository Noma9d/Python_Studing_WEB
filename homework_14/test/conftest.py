import pytest
from fastapi.testclient import TestClient
from main import app
from src.database.models import Base
from src.database.db import get_db, SessionLocal
from src.database.db import engine as engine_connect

engine = engine_connect

TestingSessionLocal = SessionLocal


@pytest.fixture(scope="module")
def session():
    # Create the database

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client(session):
    # Dependency override

    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest.fixture(scope="module")
def user():
    return {"username": "woody", "email": "woody@example.com", "password": "123456789"}
