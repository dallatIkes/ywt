from app.core.exceptions import (
    NotFoundError,
    ConflictError,
    ForbiddenError,
    UnauthorizedError,
)


def test_not_found_message():
    err = NotFoundError("User", "samy")
    assert str(err) == "User 'samy' not found"
    assert err.resource == "User"
    assert err.identifier == "samy"


def test_conflict_message():
    err = ConflictError("Username already exists")
    assert str(err) == "Username already exists"


def test_forbidden_default_message():
    err = ForbiddenError()
    assert str(err) == "Action not allowed"


def test_forbidden_custom_message():
    err = ForbiddenError("Cannot rate your own recommendation")
    assert str(err) == "Cannot rate your own recommendation"


def test_unauthorized_default_message():
    err = UnauthorizedError()
    assert str(err) == "Not authenticated"
