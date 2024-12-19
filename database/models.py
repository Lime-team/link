from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .database_ import Base


class BotUser(Base):
    __tablename__ = 'bot_user'

    tg_id: Mapped[str] = mapped_column(String(255), primary_key=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    medals: Mapped[str] = mapped_column(String(255), nullable=False)
