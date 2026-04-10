from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.db.models.user import User
from app.core.exceptions import NotFoundError


class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def get_by_username_or_404(self, username: str) -> User:
        user = self.get_by_username(username)
        if not user:
            raise NotFoundError("User", username)
        return user

    def create(self, username: str, hashed_password: str) -> User:
        user = User(username=username, hashed_password=hashed_password)
        return self.save(user)

    def update(self, user: User, username: str, hashed_password: str) -> User:
        user.username = username
        user.hashed_password = hashed_password
        return self.save(user)
