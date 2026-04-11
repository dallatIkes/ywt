from app.services.friendship_service import can_transition
from app.db.models.friendship import FriendshipStatus


def test_pending_to_accepted():
    assert can_transition(FriendshipStatus.PENDING, FriendshipStatus.ACCEPTED) is True


def test_pending_to_declined():
    assert can_transition(FriendshipStatus.PENDING, FriendshipStatus.DECLINED) is True


def test_accepted_to_declined_invalid():
    assert can_transition(FriendshipStatus.ACCEPTED, FriendshipStatus.DECLINED) is False


def test_declined_to_accepted_invalid():
    assert can_transition(FriendshipStatus.DECLINED, FriendshipStatus.ACCEPTED) is False


def test_accepted_to_pending_invalid():
    assert can_transition(FriendshipStatus.ACCEPTED, FriendshipStatus.PENDING) is False


def test_unknown_status_returns_false():
    assert can_transition("unknown", FriendshipStatus.ACCEPTED) is False
