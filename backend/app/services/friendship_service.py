from app.repositories.friendship_repository import FriendshipRepository
from app.repositories.user_repository import UserRepository
from app.db.models.friendship import Friendship, FriendshipStatus
from app.db.models.user import User
from app.core.exceptions import ConflictError, ForbiddenError

# ── State pattern ─────────────────────────────────────────────────────────────

# Valid transitions: pending -> accepted, pending -> declined
VALID_TRANSITIONS: dict[str, list[str]] = {
    FriendshipStatus.PENDING: [FriendshipStatus.ACCEPTED, FriendshipStatus.DECLINED],
    FriendshipStatus.ACCEPTED: [],
    FriendshipStatus.DECLINED: [],
}


def can_transition(current: str, target: str) -> bool:
    return target in VALID_TRANSITIONS.get(current, [])


# ── Service ───────────────────────────────────────────────────────────────────


class FriendshipService:
    def __init__(
        self, friendship_repo: FriendshipRepository, user_repo: UserRepository
    ):
        self.friendship_repo = friendship_repo
        self.user_repo = user_repo

    def send_request(self, requester: User, addressee_id: str) -> Friendship:
        # Business rule: cannot send a request to yourself
        if requester.id == addressee_id:
            raise ForbiddenError("Cannot send a friend request to yourself")

        # Business rule: addressee must exist
        self.user_repo.get_or_404(addressee_id)

        # Business rule: request must not already exist in any direction
        existing = self.friendship_repo.get_friendship(requester.id, addressee_id)
        if existing:
            raise ConflictError("A friend request already exists between these users")

        return self.friendship_repo.create(
            requester_id=requester.id, addressee_id=addressee_id
        )

    def respond_to_request(
        self, friendship_id: int, new_status: str, current_user: User
    ) -> Friendship:
        friendship = self.friendship_repo.get_or_404(friendship_id)

        # Business rule: only the addressee can respond
        if friendship.addressee_id != current_user.id:
            raise ForbiddenError("Only the recipient of the request can respond")

        # State pattern: validate the transition is legal
        if not can_transition(friendship.status, new_status):
            raise ConflictError(
                f"Cannot transition from '{friendship.status}' to '{new_status}'"
            )

        return self.friendship_repo.update_status(friendship, new_status)

    def get_friends(self, user: User) -> list[User]:
        return self.friendship_repo.get_friends(user.id)

    def get_pending_requests(self, user: User) -> list[Friendship]:
        return self.friendship_repo.get_pending_received(user.id)

    def get_sent_pending_requests(self, user: User) -> list[Friendship]:
        return self.friendship_repo.get_pending_sent(user.id)
