from __future__ import annotations
from typing import TYPE_CHECKING
import datetime
from sqlalchemy import String, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.user import User


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(primary_key=True)
    link: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(String(280), nullable=False)
    from_user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    to_user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    # Nullable until the recipient rates the recommendation (1-5)
    rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Nullable until the recipient replies to the recommendation
    answer: Mapped[str | None] = mapped_column(String(280), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )

    from_user: Mapped["User"] = relationship(
        back_populates="sent_recommendations", foreign_keys=[from_user_id]
    )
    to_user: Mapped["User"] = relationship(
        back_populates="received_recommendations", foreign_keys=[to_user_id]
    )

    def __repr__(self) -> str:
        return (
            f"Recommendation(id={self.id}, from={self.from_user_id}, "
            f"to={self.to_user_id}, rating={self.rating})"
        )
