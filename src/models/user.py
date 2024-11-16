from database import Base
from sqlalchemy import BigInteger, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column



class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[BigInteger] = mapped_column(BigInteger, unique=True)
    rating: Mapped[int] = mapped_column(default=1000)
    wins: Mapped[int] = mapped_column(default=0)
    losses: Mapped[int] = mapped_column(default=0)
    games: Mapped[int] = mapped_column(default=0)
    draw: Mapped[int] = mapped_column(default=0)
    registered_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())