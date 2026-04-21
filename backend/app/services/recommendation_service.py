from abc import ABC, abstractmethod
from app.repositories.recommendation_repository import RecommendationRepository
from app.repositories.user_repository import UserRepository
from app.schemas.recommendation import RecoCreate, RatingUpdate, AnswerUpdate
from app.core.exceptions import ForbiddenError, ConflictError
from app.core.decorators import log_service_call
from app.db.models.user import User
from app.db.models.recommendation import Recommendation
from app.utils.url import normalize_link

# ── Observer pattern ──────────────────────────────────────────────────────────


class RecoObserver(ABC):
    @abstractmethod
    def on_reco_sent(self, reco: Recommendation) -> None:
        pass


class LogObserver(RecoObserver):
    def on_reco_sent(self, reco: Recommendation) -> None:
        print(
            f"[LOG] New reco #{reco.id} from {reco.from_user_id} to {reco.to_user_id}"
        )


# ── Service ───────────────────────────────────────────────────────────────────


class RecommendationService:
    def __init__(
        self,
        reco_repo: RecommendationRepository,
        user_repo: UserRepository,
        observers: list[RecoObserver] | None = None,
    ):
        self.reco_repo = reco_repo
        self.user_repo = user_repo
        self.observers = observers or [LogObserver()]

    @log_service_call("send_recommendation")
    def send_reco(self, data: RecoCreate, sender: User) -> Recommendation:
        if data.to_user_id == sender.id:
            raise ForbiddenError("Cannot send a recommendation to yourself")

        self.user_repo.get_or_404(data.to_user_id)

        # Factory picks the right normalizer automatically
        normalized = normalize_link(data.link)

        reco = self.reco_repo.create(
            link=normalized,
            description=data.description,
            from_user_id=sender.id,
            to_user_id=data.to_user_id,
        )

        for observer in self.observers:
            observer.on_reco_sent(reco)

        return reco

    def get_sent(self, user: User) -> list[dict]:
        return self.reco_repo.get_sent_by_user(user.id)

    def get_received(self, user: User) -> list[dict]:
        return self.reco_repo.get_received_by_user(user.id)

    @log_service_call("rate_recommendation")
    def rate_reco(
        self, reco_id: int, data: RatingUpdate, current_user: User
    ) -> Recommendation:
        reco = self.reco_repo.get_or_404(reco_id)
        if reco.to_user_id != current_user.id:
            raise ForbiddenError("Only the recipient can rate a recommendation")
        return self.reco_repo.update_rating(reco, data.rating)

    @log_service_call("answer_recommendation")
    def answer_reco(
        self, reco_id: int, data: AnswerUpdate, current_user: User
    ) -> Recommendation:
        reco = self.reco_repo.get_or_404(reco_id)
        if reco.to_user_id != current_user.id:
            raise ForbiddenError("Only the recipient can answer a recommendation")
        if reco.answer is not None:
            raise ConflictError("This recommendation already has an answer")
        return self.reco_repo.update_answer(reco, data.answer)
