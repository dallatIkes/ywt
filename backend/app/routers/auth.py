from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.token import Token
from app.schemas.user import UserOut
from app.services.auth_service import AuthService
from app.dependencies import get_auth_service, get_current_user
from app.db.models.user import User

router = APIRouter(tags=["auth"])


@router.post("/token", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service),
):
    user = service.authenticate(form_data.username, form_data.password)
    return Token(access_token=service.create_token(user), token_type="bearer")


@router.get("/users/me", response_model=UserOut)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user
