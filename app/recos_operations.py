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

@recos_crud_router.get("/recos")
def get_recos(
    db: Session = Depends(get_db)
):
    """Reading all the recommendations.
    """
    
    return db.query(Recommendation).all()

@recos_crud_router.get("/reco")
def get_reco(
    reco_id: int, db: Session = Depends(get_db)
):
    """Reading a specific recommendations.
    """
    
    return get_reco_or_404(reco_id, db)

@recos_crud_router.post("/reco/{reco_id}")
def update_reco(
    reco_id: int,
    reco: RecoBody,
    db: Session = Depends(get_db),
):
    """Updating a recommenndation.
    """
    
    db_reco = get_reco_or_404(reco_id, db)
    
    from_user = get_user_with_id_or_404(reco.from_user_id, db)
    to_user = get_user_with_id_or_404(reco.to_user_id, db)
        
    db_reco.link = reco.link
    db_reco.from_user_id = from_user.id
    db_reco.to_user_id = to_user.id
    
    db.commit()
    db.refresh(db_reco)
    
    return db_reco


@recos_crud_router.delete("/reco")
def delete_reco(
    reco_id: int, db: Session = Depends(get_db)
):
    """Deleting a recommendation.
    """
    
    db_reco = get_reco_or_404(reco_id, db)
        
    db.delete(db_reco)
    db.commit()
    
    return {"detail": "Recommendation deleted"}