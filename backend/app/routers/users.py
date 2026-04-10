from fastapi import APIRouter, Depends, status

from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.services.user_service import UserService
from app.dependencies import get_user_service, get_current_user
from app.db.models.user import User

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate, service: UserService = Depends(get_user_service)):
    return service.create_user(data)


@router.get("", response_model=list[UserOut])
def get_all_users(service: UserService = Depends(get_user_service)):
    return service.get_all()


@router.get("/{username}", response_model=UserOut)
def get_user(username: str, service: UserService = Depends(get_user_service)):
    return service.get_by_username(username)


@router.put("/{username}", response_model=UserOut)
def update_user(
    username: str,
    data: UserUpdate,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    return service.update_user(username, data)


@router.delete("/{username}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    username: str,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    service.delete_user(username)
