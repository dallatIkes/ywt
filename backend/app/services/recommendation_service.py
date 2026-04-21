from abc import ABC, abstractmethod
from app.repositories.recommendation_repository import RecommendationRepository
from app.repositories.user_repository import UserRepository
from app.schemas.recommendation import RecoCreate, RatingUpdate
from app.core.exceptions import ForbiddenError
from app.db.models.user import User
from app.db.models.recommendation import Recommendation
from app.core.decorators import log_service_call

# ── Strategy pattern ──────────────────────────────────────────────────────────


class VideoLinkNormalizer(ABC):
    """Strategy interface — all normalizers must implement normalize()."""

    @abstractmethod
    def normalize(self, url: str) -> str:
        pass


class YouTubeNormalizer(VideoLinkNormalizer):
    """Converts any YouTube URL format to an embeddable URL."""

    def normalize(self, url: str) -> str:
        from urllib.parse import urlparse, parse_qs, urlencode

        try:
            parsed = urlparse(url)
            params = parse_qs(parsed.query)
            video_id = None

            if parsed.hostname == "youtu.be":
                video_id = parsed.path[1:]
            elif parsed.hostname and "youtube.com" in parsed.hostname:
                video_id = params.get("v", [None])[0]

            if not video_id:
                return self._fallback()

            params.pop("v", None)
            query = f"?{urlencode(params, doseq=True)}" if params else ""
            return f"https://youtube.com/embed/{video_id}{query}"
        except Exception:
            return self._fallback()

    def _fallback(self) -> str:
        return "https://youtube.com/embed/dQw4w9WgXcQ"


class PassthroughNormalizer(VideoLinkNormalizer):
    """Fallback — returns the URL as-is for unsupported platforms."""

    def normalize(self, url: str) -> str:
        return url


# ── Observer pattern ──────────────────────────────────────────────────────────


class RecoObserver(ABC):
    """Observer interface — called after a recommendation is sent."""

    @abstractmethod
    def on_reco_sent(self, reco: Recommendation) -> None:
        pass


class LogObserver(RecoObserver):
    """Logs every new recommendation to stdout."""

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
        normalizer: VideoLinkNormalizer | None = None,
        observers: list[RecoObserver] | None = None,
    ):
        # Default to YouTube normalizer if none provided
        self.reco_repo = reco_repo
        self.user_repo = user_repo
        self.normalizer = normalizer or YouTubeNormalizer()
        self.observers = observers or [LogObserver()]

    @log_service_call("send_recommendation")
    def send_reco(self, data: RecoCreate, sender: User) -> Recommendation:
        # Business rule: cannot recommend to yourself
        if data.to_user_id == sender.id:
            raise ForbiddenError("Cannot send a recommendation to yourself")

        # Business rule: recipient must exist
        self.user_repo.get_or_404(data.to_user_id)

        normalized = self.normalizer.normalize(data.link)

        reco = self.reco_repo.create(
            link=normalized,
            description=data.description,
            from_user_id=sender.id,
            to_user_id=data.to_user_id,
        )

        # Notify all registered observers
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

        # Business rule: only the recipient can rate
        if reco.to_user_id != current_user.id:
            raise ForbiddenError("Only the recipient can rate a recommendation")

        return self.reco_repo.update_rating(reco, data.rating)
