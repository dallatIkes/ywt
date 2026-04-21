import datetime
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.db.models.recommendation import Recommendation
from app.db.models.user import User


class RecommendationRepository(BaseRepository[Recommendation]):
    def __init__(self, db: Session):
        super().__init__(Recommendation, db)

    def create(
        self, link: str, description: str, from_user_id: str, to_user_id: str
    ) -> Recommendation:
        reco = Recommendation(
            link=link,
            description=description,
            from_user_id=from_user_id,
            to_user_id=to_user_id,
            created_at=datetime.datetime.now(),
        )
        return self.save(reco)

    def get_sent_by_user(self, user_id: str) -> list[dict]:
        rows = (
            self.db.query(Recommendation, User.username)
            .join(User, Recommendation.to_user_id == User.id)
            .filter(Recommendation.from_user_id == user_id)
            .all()
        )
        return [
            {
                "id": r.Recommendation.id,
                "link": r.Recommendation.link,
                "description": r.Recommendation.description,
                "to_user": r.username,
                "rating": r.Recommendation.rating,
                "answer": r.Recommendation.answer,
                "created_at": r.Recommendation.created_at,
            }
            for r in rows
        ]

    def get_received_by_user(self, user_id: str) -> list[dict]:
        rows = (
            self.db.query(Recommendation, User.username)
            .join(User, Recommendation.from_user_id == User.id)
            .filter(Recommendation.to_user_id == user_id)
            .all()
        )
        return [
            {
                "id": r.Recommendation.id,
                "link": r.Recommendation.link,
                "description": r.Recommendation.description,
                "from_user": r.username,
                "rating": r.Recommendation.rating,
                "answer": r.Recommendation.answer,
                "created_at": r.Recommendation.created_at,
            }
            for r in rows
        ]

    def update_rating(self, reco: Recommendation, rating: int) -> Recommendation:
        reco.rating = rating
        return self.save(reco)

    def update_answer(self, reco: Recommendation, answer: str) -> Recommendation:
        reco.answer = answer
        return self.save(reco)
