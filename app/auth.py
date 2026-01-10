from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db_connection import get_db
from app.models import Token
from app.utils.security.pwd import authenticate_user
from app.utils.security.token import create_access_token, decode_access_token

def get_current_user(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="/token")), 
    session: Session = Depends(get_db)
):
    user = decode_access_token(token, session)
    if not user:
        raise HTTPException(status_code=401, detail="User not authorized")
    return user

auth_router = APIRouter()

@auth_router.post("/token")
def get_user_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token({"sub": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@auth_router.get("/users/me")
def read_user_me(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="/token")), 
    session: Session = Depends(get_db)
):
    user = get_current_user(token, session)

    return {
        "id": user.id,
        "username": user.username,
    }