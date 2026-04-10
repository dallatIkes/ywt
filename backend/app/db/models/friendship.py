from __future__ import annotations
from typing import TYPE_CHECKING
import datetime
from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.user import User


class FriendshipStatus:
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"


class Friendship(Base):
    __tablename__ = "friendships"

    id: Mapped[int] = mapped_column(primary_key=True)
    requester_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    addressee_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    # One of: pending, accepted, declined
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default=FriendshipStatus.PENDING
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )

    requester: Mapped["User"] = relationship(
        back_populates="sent_friend_requests", foreign_keys=[requester_id]
    )
    addressee: Mapped["User"] = relationship(
        back_populates="received_friend_requests", foreign_keys=[addressee_id]
    )

    def __repr__(self) -> str:
        return (
            f"Friendship(id={self.id}, from={self.requester_id}, "
            f"to={self.addressee_id}, status={self.status})"
        )
