from fastapi import APIRouter, Depends, status

from app.schemas.friendship import (
    FriendRequestCreate,
    FriendRequestOut,
    FriendOut,
    FriendshipStatusUpdate,
)
from app.services.friendship_service import FriendshipService
from app.dependencies import get_friendship_service, get_current_user
from app.db.models.user import User

router = APIRouter(prefix="/friendships", tags=["friendships"])


@router.post(
    "/request", response_model=FriendRequestOut, status_code=status.HTTP_201_CREATED
)
def send_friend_request(
    data: FriendRequestCreate,
    service: FriendshipService = Depends(get_friendship_service),
    current_user: User = Depends(get_current_user),
):
    return service.send_request(current_user, data.addressee_id)


@router.patch("/{friendship_id}/respond", response_model=FriendRequestOut)
def respond_to_request(
    friendship_id: int,
    data: FriendshipStatusUpdate,
    service: FriendshipService = Depends(get_friendship_service),
    current_user: User = Depends(get_current_user),
):
    return service.respond_to_request(friendship_id, data.status, current_user)


@router.get("/friends", response_model=list[FriendOut])
def get_friends(
    service: FriendshipService = Depends(get_friendship_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_friends(current_user)


@router.get("/pending", response_model=list[FriendRequestOut])
def get_pending_requests(
    service: FriendshipService = Depends(get_friendship_service),
    current_user: User = Depends(get_current_user),
):
    return service.get_pending_requests(current_user)
