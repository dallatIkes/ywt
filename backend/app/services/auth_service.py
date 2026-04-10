from app.repositories.user_repository import UserRepository
from app.core.security import verify_pwd, decode_access_token, create_access_token
from app.core.exceptions import UnauthorizedError
from app.db.models.user import User


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def authenticate(self, username: str, password: str) -> User:
        user = self.repo.get_by_username(username)
        if not user or not verify_pwd(password, user.hashed_password):
            # Intentionally vague — don't reveal which field is wrong
            raise UnauthorizedError("Incorrect username or password")
        return user

    def get_current_user(self, token: str) -> User:
        username = decode_access_token(token)
        if not username:
            raise UnauthorizedError("Invalid or expired token")
        return self.repo.get_by_username_or_404(username)

    def create_token(self, user: User) -> str:
        return create_access_token({"sub": user.username})
