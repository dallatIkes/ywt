import uuid
import datetime
from sqlalchemy import String, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20), nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(50), nullable=False)

    sent_recommendations: Mapped[list["Recommendation"]] = relationship(
        back_populates="from_user",
        foreign_keys="Recommendation.from_user_id"
    )
    received_recommendations: Mapped[list["Recommendation"]] = relationship(
        back_populates="to_user",
        foreign_keys="Recommendation.to_user_id"
    )
    
    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username}, hashed_password={self.hashed_password})"

class Recommendation(Base):
    __tablename__ = "recommendations"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    link: Mapped[str] = mapped_column(nullable=False)
    from_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    to_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),
        nullable=False
    )
    
    from_user: Mapped["User"] = relationship(
        back_populates="sent_recommendations",
        foreign_keys=[from_user_id]
    )
    to_user: Mapped["User"] = relationship(
        back_populates="received_recommendations",
        foreign_keys=[to_user_id]
    )
    
    def __repr__(self) -> str:
        return f"Recommendation(id={self.id}, link={self.link}, from_user_id={self.from_user_id}, to_user_id={self.to_user_id}, created_at={self.created_at})"