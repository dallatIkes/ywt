from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.db.models.friendship import Friendship, FriendshipStatus
from app.db.models.user import User


class FriendshipRepository(BaseRepository[Friendship]):
    def __init__(self, db: Session):
        super().__init__(Friendship, db)

    def create(self, requester_id: str, addressee_id: str) -> Friendship:
        friendship = Friendship(
            requester_id=requester_id,
            addressee_id=addressee_id,
            status=FriendshipStatus.PENDING,
        )
        return self.save(friendship)

    def get_friendship(self, requester_id: str, addressee_id: str) -> Friendship | None:
        # Check both directions — friendship is bidirectional
        return (
            self.db.query(Friendship)
            .filter(
                (
                    (Friendship.requester_id == requester_id)
                    & (Friendship.addressee_id == addressee_id)
                )
                | (
                    (Friendship.requester_id == addressee_id)
                    & (Friendship.addressee_id == requester_id)
                )
            )
            .first()
        )

    def are_friends(self, user_id_a: str, user_id_b: str) -> bool:
        friendship = self.get_friendship(user_id_a, user_id_b)
        return friendship is not None and friendship.status == FriendshipStatus.ACCEPTED

    def get_friends(self, user_id: str) -> list[User]:
        # Collect accepted friendships in both directions
        sent = (
            self.db.query(User)
            .join(Friendship, Friendship.addressee_id == User.id)
            .filter(
                Friendship.requester_id == user_id,
                Friendship.status == FriendshipStatus.ACCEPTED,
            )
            .all()
        )
        received = (
            self.db.query(User)
            .join(Friendship, Friendship.requester_id == User.id)
            .filter(
                Friendship.addressee_id == user_id,
                Friendship.status == FriendshipStatus.ACCEPTED,
            )
            .all()
        )
        return sent + received

    def get_pending_received(self, user_id: str) -> list[Friendship]:
        # Friend requests waiting for this user's response
        return (
            self.db.query(Friendship)
            .filter(
                Friendship.addressee_id == user_id,
                Friendship.status == FriendshipStatus.PENDING,
            )
            .all()
        )

    def update_status(self, friendship: Friendship, status: str) -> Friendship:
        friendship.status = status
        return self.save(friendship)
