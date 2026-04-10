from app.db_connection import SessionLocal, Base, engine
from app.database import User
from app.utils.security.pwd import hash_pwd


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


if __name__ == "__main__":
    seed()
