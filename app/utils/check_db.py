from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database import User, Recommendation

def get_user_or_404(user_id: str, db: Session) -> User:
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f"User {user_id} not found"
        )

    return user

def get_reco_or_404(reco_id: int, db: Session) -> Recommendation:
    reco = (
        db.query(Recommendation)
        .filter(Recommendation.id == reco_id)
        .first()
    )
    if reco is None:
        raise HTTPException(
            status_code=404, detail=f"Recommendation {reco_id} not found"
        )

    return reco