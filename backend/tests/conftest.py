# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.db.base import Base
from app.db.models import User, Recommendation, Friendship  # noqa: F401
from app.db.session import get_db
from app.core.security import hash_pwd
from main import app


@pytest.fixture(scope="function")
def db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},  # allows cross-thread usage
        poolclass=StaticPool,  # reuses the same connection — critical for in-memory DB
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture
def user_john(db):
    user = User(username="johnDoe", hashed_password=hash_pwd("admin1234"))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def user_jane(db):
    user = User(username="janeDoe", hashed_password=hash_pwd("admin1234"))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def auth_client(db, user_john):
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as c:
        response = c.post(
            "/token", data={"username": "johnDoe", "password": "admin1234"}
        )
        c.headers.update({"Authorization": f"Bearer {response.json()['access_token']}"})
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def auth_client_jane(db, user_jane):
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as c:
        response = c.post(
            "/token", data={"username": "janeDoe", "password": "admin1234"}
        )
        c.headers.update({"Authorization": f"Bearer {response.json()['access_token']}"})
        yield c
    app.dependency_overrides.clear()
