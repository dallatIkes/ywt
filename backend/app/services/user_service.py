from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_pwd
from app.core.exceptions import ConflictError
from app.db.models.user import User


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def create_user(self, data: UserCreate) -> User:
        if self.repo.get_by_username(data.username):
            raise ConflictError("Username already exists")
        return self.repo.create(
            username=data.username, hashed_password=hash_pwd(data.password)
        )

    def get_all(self) -> list[User]:
        return self.repo.get_all()

    def get_by_username(self, username: str) -> User:
        return self.repo.get_by_username_or_404(username)

    def update_user(self, username: str, data: UserUpdate) -> User:
        user = self.repo.get_by_username_or_404(username)

        # Only check for conflict if the username is actually changing
        if data.username != user.username:
            if self.repo.get_by_username(data.username):
                raise ConflictError("Username already exists")

        return self.repo.update(
            user=user, username=data.username, hashed_password=hash_pwd(data.password)
        )

    def delete_user(self, username: str) -> None:
        user = self.repo.get_by_username_or_404(username)
        self.repo.delete(user)
