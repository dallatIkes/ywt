from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.recommendation_repository import RecommendationRepository
from app.repositories.friendship_repository import FriendshipRepository
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.services.recommendation_service import RecommendationService
from app.services.friendship_service import FriendshipService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# ── Repository factories ──────────────────────────────────────────────────────


def get_user_repo(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_reco_repo(db: Session = Depends(get_db)) -> RecommendationRepository:
    return RecommendationRepository(db)


def get_friendship_repo(db: Session = Depends(get_db)) -> FriendshipRepository:
    return FriendshipRepository(db)


# ── Service factories ─────────────────────────────────────────────────────────


def get_auth_service(repo: UserRepository = Depends(get_user_repo)) -> AuthService:
    return AuthService(repo)


def get_user_service(repo: UserRepository = Depends(get_user_repo)) -> UserService:
    return UserService(repo)


def get_reco_service(
    reco_repo: RecommendationRepository = Depends(get_reco_repo),
    user_repo: UserRepository = Depends(get_user_repo),
) -> RecommendationService:
    return RecommendationService(reco_repo, user_repo)


def get_friendship_service(
    friendship_repo: FriendshipRepository = Depends(get_friendship_repo),
    user_repo: UserRepository = Depends(get_user_repo),
) -> FriendshipService:
    return FriendshipService(friendship_repo, user_repo)


# ── Current user ─────────────────────────────────────────────────────────────


def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: AuthService = Depends(get_auth_service),
) -> User:
    return service.get_current_user(token)
