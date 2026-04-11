import pytest
from app.services.friendship_service import FriendshipService
from app.repositories.friendship_repository import FriendshipRepository
from app.repositories.user_repository import UserRepository
from app.db.models.friendship import FriendshipStatus
from app.core.exceptions import ConflictError, ForbiddenError, NotFoundError


@pytest.fixture
def friendship_service(db):
    return FriendshipService(FriendshipRepository(db), UserRepository(db))


def test_send_request(friendship_service, user_john, user_jane):
    req = friendship_service.send_request(user_john, user_jane.id)
    assert req.requester_id == user_john.id
    assert req.addressee_id == user_jane.id
    assert req.status == FriendshipStatus.PENDING


def test_send_request_to_self_raises_forbidden(friendship_service, user_john):
    with pytest.raises(ForbiddenError):
        friendship_service.send_request(user_john, user_john.id)


def test_send_duplicate_request_raises_conflict(
    friendship_service, user_john, user_jane
):
    friendship_service.send_request(user_john, user_jane.id)
    with pytest.raises(ConflictError):
        friendship_service.send_request(user_john, user_jane.id)


def test_send_request_to_unknown_raises_not_found(friendship_service, user_john):
    with pytest.raises(NotFoundError):
        friendship_service.send_request(user_john, "nonexistent-id")


def test_accept_request(friendship_service, user_john, user_jane):
    req = friendship_service.send_request(user_john, user_jane.id)
    accepted = friendship_service.respond_to_request(
        req.id, FriendshipStatus.ACCEPTED, user_jane
    )
    assert accepted.status == FriendshipStatus.ACCEPTED


def test_decline_request(friendship_service, user_john, user_jane):
    req = friendship_service.send_request(user_john, user_jane.id)
    declined = friendship_service.respond_to_request(
        req.id, FriendshipStatus.DECLINED, user_jane
    )
    assert declined.status == FriendshipStatus.DECLINED


def test_wrong_user_cannot_respond(friendship_service, user_john, user_jane):
    req = friendship_service.send_request(user_john, user_jane.id)
    with pytest.raises(ForbiddenError):
        friendship_service.respond_to_request(
            req.id, FriendshipStatus.ACCEPTED, user_john
        )


def test_cannot_accept_already_accepted(friendship_service, user_john, user_jane):
    req = friendship_service.send_request(user_john, user_jane.id)
    friendship_service.respond_to_request(req.id, FriendshipStatus.ACCEPTED, user_jane)
    with pytest.raises(ConflictError):
        friendship_service.respond_to_request(
            req.id, FriendshipStatus.ACCEPTED, user_jane
        )


def test_get_friends(friendship_service, user_john, user_jane):
    req = friendship_service.send_request(user_john, user_jane.id)
    friendship_service.respond_to_request(req.id, FriendshipStatus.ACCEPTED, user_jane)
    friends = friendship_service.get_friends(user_john)
    assert any(f.id == user_jane.id for f in friends)


def test_get_pending_requests(friendship_service, user_john, user_jane):
    friendship_service.send_request(user_john, user_jane.id)
    pending = friendship_service.get_pending_requests(user_jane)
    assert len(pending) == 1
    assert pending[0]["requester_id"] == user_john.id


def test_pending_requests_include_usernames(friendship_service, user_john, user_jane):
    friendship_service.send_request(user_john, user_jane.id)
    pending = friendship_service.get_pending_requests(user_jane)
    assert pending[0]["requester_username"] == "johnDoe"
    assert pending[0]["addressee_username"] == "janeDoe"


def test_sent_pending_include_usernames(friendship_service, user_john, user_jane):
    friendship_service.send_request(user_john, user_jane.id)
    sent = friendship_service.get_sent_pending_requests(user_john)
    assert sent[0]["requester_username"] == "johnDoe"
    assert sent[0]["addressee_username"] == "janeDoe"
