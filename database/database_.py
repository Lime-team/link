from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy import String

from uuid import uuid4

from config_reader import config


DB_URL = f'mysql+aiomysql://{config.mysql_user.get_secret_value()}:{config.mysql_password.get_secret_value()}@{config.mysql_host.get_secret_value()}/{config.mysql_db_name.get_secret_value()}'

engine = create_async_engine(url=DB_URL)
async_session = async_sessionmaker(engine, class_=AsyncSession)


class Base(AsyncAttrs, DeclarativeBase):
    id_: Mapped[str] = mapped_column(String(255), default=str(uuid4()))
