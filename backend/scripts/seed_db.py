# scripts/seed.py
from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.db.models.user import User
from app.db.models import Recommendation, Friendship  # noqa: F401 - needed for SQLAlchemy relationship resolution
from app.core.security import hash_pwd


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Users
    user1 = User(username="johnDoe", hashed_password=hash_pwd("admin1234"))
    user2 = User(username="janeDoe", hashed_password=hash_pwd("admin1234"))
    db.add_all([user1, user2])
    db.commit()
    db.refresh(user1)
    db.refresh(user2)

    print(f"Created users: {user1.username}, {user2.username}")
    db.close()


if __name__ == "__main__":
    seed()
