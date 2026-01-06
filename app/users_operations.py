from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models import UserBody
from app.db_connection import get_db
from app.database import User
from app.utils.security import hash_pwd
from app.utils.check_db import get_user_or_404

users_crud_router = APIRouter()

@users_crud_router.post("/user")
def add_new_user(
    user: UserBody, db: Session = Depends(get_db)
):
    """Creating a new user.
    """
    
    new_user = User(
        username=user.username, 
        hashed_password=hash_pwd(user.password)
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@users_crud_router.get("/users")
def get_users(
    db: Session = Depends(get_db)
):
    """Reading all the users.
    """
    
    return db.query(User).all()

@users_crud_router.get("/user")
def get_user(
    user_id: str, db: Session = Depends(get_db)
):
    """Reading a specific user.
    """
    
    return get_user_or_404(user_id, db)

@users_crud_router.post("/user/{user_id}")
def update_user(
    user_id: str,
    user: UserBody,
    db: Session = Depends(get_db),
):
    """Updating a user.
    """
    
    db_user = get_user_or_404(user_id, db)
        
    db_user.username = user.username
    db_user.hashed_password = hash_pwd(user.password)
    
    db.commit()
    db.refresh(db_user)
    
    return db_user


@users_crud_router.delete("/user")
def delete_user(
    user_id: str, db: Session = Depends(get_db)
):
    """Deleting a user.
    """
    
    db_user = get_user_or_404(user_id, db)
        
    db.delete(db_user)
    db.commit()
    
    return {"detail": "User deleted"}