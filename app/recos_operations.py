from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import datetime

from app.models import RecoBody
from app.db_connection import get_db
from app.database import Recommendation, User
from app.utils.check_db import get_user_with_id_or_404, get_reco_or_404
from app.auth import get_current_user

recos_crud_router = APIRouter()

@recos_crud_router.post("/reco")
def add_new_reco(
    reco: RecoBody, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Creating a new recommendation.
    """
    
    to_user = get_user_with_id_or_404(reco.to_user_id, db)
    
    new_reco = Recommendation(
        link=reco.link, 
        from_user_id=current_user.id, 
        to_user_id=to_user.id, 
        created_at=datetime.datetime.now()
    )
    
    db.add(new_reco)
    db.commit()
    db.refresh(new_reco)
    
    return new_reco

@recos_crud_router.get("/recommendations/sent")
def get_recos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Reading all the recommendations sent.
    """
    
    return db.query(Recommendation).filter(Recommendation.from_user == current_user).all()

@recos_crud_router.get("/recommendations/received")
def get_recos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Reading all the recommendations received.
    """
    
    return db.query(Recommendation).filter(Recommendation.to_user == current_user).all()