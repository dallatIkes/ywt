from sqlalchemy.orm import Session, aliased
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

    def get_pending_received(self, user_id: str) -> list[dict]:
        # Join both requester and addressee usernames in one query
        Requester = aliased(User)
        Addressee = aliased(User)
        rows = (
            self.db.query(Friendship, Requester.username, Addressee.username)
            .join(Requester, Friendship.requester_id == Requester.id)
            .join(Addressee, Friendship.addressee_id == Addressee.id)
            .filter(
                Friendship.addressee_id == user_id,
                Friendship.status == FriendshipStatus.PENDING,
            )
            .all()
        )
        return [
            {
                "id": r.Friendship.id,
                "requester_id": r.Friendship.requester_id,
                "requester_username": r[1],
                "addressee_id": r.Friendship.addressee_id,
                "addressee_username": r[2],
                "status": r.Friendship.status,
                "created_at": r.Friendship.created_at,
            }
            for r in rows
        ]

    def get_pending_sent(self, user_id: str) -> list[dict]:
        Requester = aliased(User)
        Addressee = aliased(User)
        rows = (
            self.db.query(Friendship, Requester.username, Addressee.username)
            .join(Requester, Friendship.requester_id == Requester.id)
            .join(Addressee, Friendship.addressee_id == Addressee.id)
            .filter(
                Friendship.requester_id == user_id,
                Friendship.status == FriendshipStatus.PENDING,
            )
            .all()
        )
        return [
            {
                "id": r.Friendship.id,
                "requester_id": r.Friendship.requester_id,
                "requester_username": r[1],
                "addressee_id": r.Friendship.addressee_id,
                "addressee_username": r[2],
                "status": r.Friendship.status,
                "created_at": r.Friendship.created_at,
            }
            for r in rows
        ]

    def update_status(self, friendship: Friendship, status: str) -> Friendship:
        friendship.status = status
        return self.save(friendship)
