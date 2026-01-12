from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import datetime

from app.models import RecoBody
from app.db_connection import get_db
from app.database import Recommendation, User
from app.utils.check_db import get_user_with_id_or_404, get_reco_or_404
from app.auth import get_current_user
from app.utils.url import normalize_youtube_link

recos_crud_router = APIRouter()

@recos_crud_router.post("/recommendations/send")
def add_new_reco(
    reco: RecoBody, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Creating a new recommendation.
    """
    
    to_user = get_user_with_id_or_404(reco.to_user_id, db)
    
    new_reco = Recommendation(
        link=normalize_youtube_link(reco.link), 
        description= reco.description,
        from_user_id=current_user.id, 
        to_user_id=to_user.id, 
        created_at=datetime.datetime.now()
    )
    
    db.add(new_reco)
    db.commit()
    db.refresh(new_reco)
    
    return new_reco

@recos_crud_router.get("/recommendations/sent")
def get_sent_recos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Reading all the recommendations sent.
    """
    
    recos = (
        db.query(Recommendation, User.username)
        .join(User, Recommendation.to_user_id == User.id)
        .filter(Recommendation.from_user_id == current_user.id)
        .all()
    )
    
    return [
        {
            "link": r.Recommendation.link,
            "description": r.Recommendation.description,
            "to_user": r.username
        }
        for r in recos
    ]

@recos_crud_router.get("/recommendations/received")
def get_reeceived_recos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Reading all the recommendations received.
    """
    
    recos = (
        db.query(Recommendation, User.username)
        .join(User, Recommendation.from_user_id == User.id)
        .filter(Recommendation.to_user_id == current_user.id)
        .all()
    )
    
    return [
        {
            "link": r.Recommendation.link,
            "description": r.Recommendation.description,
            "from_user": r.username
        }
        for r in recos
    ]