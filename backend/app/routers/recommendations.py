from fastapi import APIRouter, Depends, status

from app.schemas.recommendation import (
    RecoCreate,
    RecoSentOut,
    RecoReceivedOut,
    RatingUpdate,
    RecoOut,
)
from app.services.recommendation_service import RecommendationService
from app.dependencies import get_reco_service, get_current_user
from app.db.models.user import User

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.post("/send", response_model=RecoOut, status_code=status.HTTP_201_CREATED)
def send_reco(
    data: RecoCreate,
    service: RecommendationService = Depends(get_reco_service),
    current_user: User = Depends(get_current_user),
):
    return service.send_reco(data, current_user)


@router.get("/sent", response_model=list[RecoSentOut])
def get_sent(
    service: RecommendationService = Depends(get_reco_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_sent(current_user)


@router.get("/received", response_model=list[RecoReceivedOut])
def get_received(
    service: RecommendationService = Depends(get_reco_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_received(current_user)


@router.patch("/{reco_id}/rating", response_model=RecoOut)
def rate_reco(
    reco_id: int,
    data: RatingUpdate,
    service: RecommendationService = Depends(get_reco_service),
    current_user: User = Depends(get_current_user),
):
    return service.rate_reco(reco_id, data, current_user)
