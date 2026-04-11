import pytest
from app.services.recommendation_service import RecommendationService
from app.repositories.recommendation_repository import RecommendationRepository
from app.repositories.user_repository import UserRepository
from app.schemas.recommendation import RecoCreate, RatingUpdate
from app.core.exceptions import ForbiddenError, NotFoundError


@pytest.fixture
def reco_service(db):
    return RecommendationService(RecommendationRepository(db), UserRepository(db))


def test_send_reco(reco_service, user_john, user_jane):
    data = RecoCreate(
        link="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        description="Great video",
        to_user_id=user_jane.id,
    )
    reco = reco_service.send_reco(data, user_john)
    assert reco.from_user_id == user_john.id
    assert reco.to_user_id == user_jane.id
    assert reco.rating is None


def test_send_reco_normalizes_link(reco_service, user_john, user_jane):
    data = RecoCreate(
        link="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        description="Great video",
        to_user_id=user_jane.id,
    )
    reco = reco_service.send_reco(data, user_john)
    assert "embed" in reco.link


def test_send_reco_to_self_raises_forbidden(reco_service, user_john):
    data = RecoCreate(
        link="https://youtu.be/dQw4w9WgXcQ",
        description="Great video",
        to_user_id=user_john.id,
    )
    with pytest.raises(ForbiddenError):
        reco_service.send_reco(data, user_john)


def test_send_reco_to_unknown_user_raises_not_found(reco_service, user_john):
    data = RecoCreate(
        link="https://youtu.be/dQw4w9WgXcQ",
        description="Great video",
        to_user_id="nonexistent-id",
    )
    with pytest.raises(NotFoundError):
        reco_service.send_reco(data, user_john)


def test_get_sent(reco_service, user_john, user_jane):
    data = RecoCreate(
        link="https://youtu.be/dQw4w9WgXcQ",
        description="Watch this",
        to_user_id=user_jane.id,
    )
    reco_service.send_reco(data, user_john)
    sent = reco_service.get_sent(user_john)
    assert len(sent) == 1
    assert sent[0]["to_user"] == user_jane.username


def test_get_received(reco_service, user_john, user_jane):
    data = RecoCreate(
        link="https://youtu.be/dQw4w9WgXcQ",
        description="Watch this",
        to_user_id=user_jane.id,
    )
    reco_service.send_reco(data, user_john)
    received = reco_service.get_received(user_jane)
    assert len(received) == 1
    assert received[0]["from_user"] == user_john.username


def test_rate_reco(reco_service, user_john, user_jane):
    data = RecoCreate(
        link="https://youtu.be/dQw4w9WgXcQ",
        description="Watch this",
        to_user_id=user_jane.id,
    )
    reco = reco_service.send_reco(data, user_john)
    rated = reco_service.rate_reco(reco.id, RatingUpdate(rating=5), user_jane)
    assert rated.rating == 5


def test_rate_reco_wrong_user_raises_forbidden(reco_service, user_john, user_jane):
    data = RecoCreate(
        link="https://youtu.be/dQw4w9WgXcQ",
        description="Watch this",
        to_user_id=user_jane.id,
    )
    reco = reco_service.send_reco(data, user_john)
    with pytest.raises(ForbiddenError):
        reco_service.rate_reco(reco.id, RatingUpdate(rating=5), user_john)
