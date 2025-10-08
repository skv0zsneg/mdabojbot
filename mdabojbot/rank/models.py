from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from mdabojbot.common.models import BaseModel


class Rank(BaseModel):
    """Telegram chat ranks."""

    __tablename__ = "rank"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_chat_id: Mapped[int]
    name: Mapped[str]

    bs: Mapped[List["UsersRanks"]] = relationship()


class UsersRanks(BaseModel):
    """Ranks that sets to user in chat."""

    __tablename__ = "users_ranks"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_user_id: Mapped[int]
    rank_id: Mapped[int] = mapped_column(ForeignKey("rank.id"))
