import pytest
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.core.exceptions import ConflictError, NotFoundError


@pytest.fixture
def user_service(db):
    return UserService(UserRepository(db))


def test_create_user(user_service):
    user = user_service.create_user(
        UserCreate(username="testuser", password="password123")
    )
    assert user.username == "testuser"
    assert user.id is not None


def test_created_user_password_is_hashed(user_service):
    user = user_service.create_user(
        UserCreate(username="testuser", password="password123")
    )
    assert user.hashed_password != "password123"


def test_create_duplicate_raises_conflict(user_service):
    user_service.create_user(UserCreate(username="testuser", password="password123"))
    with pytest.raises(ConflictError):
        user_service.create_user(
            UserCreate(username="testuser", password="password123")
        )


def test_get_by_username(user_service):
    user_service.create_user(UserCreate(username="testuser", password="password123"))
    user = user_service.get_by_username("testuser")
    assert user.username == "testuser"


def test_get_unknown_raises_not_found(user_service):
    with pytest.raises(NotFoundError):
        user_service.get_by_username("nobody")


def test_update_user(user_service):
    user_service.create_user(UserCreate(username="testuser", password="password123"))
    updated = user_service.update_user(
        "testuser", UserUpdate(username="newname", password="newpass123")
    )
    assert updated.username == "newname"


def test_update_to_existing_username_raises_conflict(user_service):
    user_service.create_user(UserCreate(username="user1", password="password123"))
    user_service.create_user(UserCreate(username="user2", password="password123"))
    with pytest.raises(ConflictError):
        user_service.update_user(
            "user1", UserUpdate(username="user2", password="password123")
        )


def test_delete_user(user_service):
    user_service.create_user(UserCreate(username="testuser", password="password123"))
    user_service.delete_user("testuser")
    with pytest.raises(NotFoundError):
        user_service.get_by_username("testuser")


def test_get_all(user_service):
    user_service.create_user(UserCreate(username="user1", password="password123"))
    user_service.create_user(UserCreate(username="user2", password="password123"))
    assert len(user_service.get_all()) == 2
