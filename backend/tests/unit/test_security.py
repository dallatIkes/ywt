from app.core.security import (
    hash_pwd,
    verify_pwd,
    create_access_token,
    decode_access_token,
)


def test_hash_is_not_plaintext():
    hashed = hash_pwd("secret123")
    assert hashed != "secret123"


def test_verify_correct_password():
    hashed = hash_pwd("secret123")
    assert verify_pwd("secret123", hashed) is True


def test_verify_wrong_password():
    hashed = hash_pwd("secret123")
    assert verify_pwd("wrong", hashed) is False


def test_two_hashes_of_same_pwd_differ():
    # bcrypt uses random salt — same input must never produce same hash
    assert hash_pwd("secret123") != hash_pwd("secret123")


def test_token_roundtrip():
    token = create_access_token({"sub": "johnDoe"})
    assert decode_access_token(token) == "johnDoe"


def test_invalid_token_returns_none():
    assert decode_access_token("not.a.valid.token") is None


def test_empty_token_returns_none():
    assert decode_access_token("") is None
