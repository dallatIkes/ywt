from __future__ import annotations
from typing import TYPE_CHECKING
import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.recommendation import Recommendation
    from app.db.models.friendship import Friendship


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    username: Mapped[str] = mapped_column(
        String(20), nullable=False, unique=True, index=True
    )
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)

    # Relationships defined with string refs to avoid circular imports
    sent_recommendations: Mapped[list["Recommendation"]] = relationship(
        back_populates="from_user", foreign_keys="Recommendation.from_user_id"
    )
    received_recommendations: Mapped[list["Recommendation"]] = relationship(
        back_populates="to_user", foreign_keys="Recommendation.to_user_id"
    )
    sent_friend_requests: Mapped[list["Friendship"]] = relationship(
        back_populates="requester", foreign_keys="Friendship.requester_id"
    )
    received_friend_requests: Mapped[list["Friendship"]] = relationship(
        back_populates="addressee", foreign_keys="Friendship.addressee_id"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username})"
