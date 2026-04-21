# scripts/seed.py
from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.db.models.user import User
from app.db.models import (  # noqa: F401 - needed for SQLAlchemy relationship resolution
    Recommendation,
    Friendship,
)
from app.core.security import hash_pwd
from app.db.models.friendship import FriendshipStatus


def seed():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Users
    user1 = User(username="johnDoe", hashed_password=hash_pwd("admin1234"))
    user2 = User(username="janeDoe", hashed_password=hash_pwd("admin1234"))
    db.add_all([user1, user2])
    db.commit()
    db.refresh(user1)
    db.refresh(user2)
    print(f"\nCreated users: {user1.username}, {user2.username}")

    # Friendships
    friendship = Friendship(requester_id=user1.id, addressee_id=user2.id)
    friendship.status = FriendshipStatus.ACCEPTED
    db.add(friendship)
    db.commit()
    print(f"\nCreated friendship: {friendship}")
    print(f"{user1.username} and {user2.username} are now friends!")

    # Recommendations
    reco1 = Recommendation(
        link="https://youtube.com/embed/dQw4w9WgXcQ",
        description="A classic music video.",
        from_user_id=user1.id,
        to_user_id=user2.id,
    )
    db.add(reco1)
    db.commit()
    print(f"\nCreated recommendation: {reco1}")
    print(f"{user1.username} recommended a video to {user2.username}!")

    db.close()


if __name__ == "__main__":
    seed()
