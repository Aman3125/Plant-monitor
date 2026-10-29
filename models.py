from __future__ import annotations

from datetime import UTC, datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)

    readings: Mapped[list[Reading]] = relationship(back_populates="author",
                                                   cascade="all, delete-orphan")


class Reading(Base):
    __tablename__ = "reading"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # "temperature", "humidity" or "light"
    sensor: Mapped[str] = mapped_column(String(20), nullable=False)
    content: Mapped[float] = mapped_column(Float, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False, index=True)
    date_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                     default=lambda: datetime.now(UTC))
    author: Mapped[User] = relationship(back_populates="readings")
