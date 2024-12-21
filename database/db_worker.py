import logging
from .wrappers import connection
from .models import BotUser
from sqlalchemy import select
from typing import Optional, Dict, Any
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


@connection
async def set_user(session, tg_id: int, description: str = 'нет', medals: str = 'нет') -> Optional[BotUser]:
    try:
        user = await session.scalar(select(BotUser).filter_by(tg_id=tg_id))

        if not user:
            new_user = BotUser(tg_id=tg_id, description=description, medals=medals)
            session.add(new_user)
            await session.commit()
            logger.info(f"Registered user with ltelegram id - {tg_id}.")
            return None
        else:
            logger.info(f"User with telegram id - {tg_id} already exists.")
            return user
    except SQLAlchemyError as e:
        logger.error(f"Error while adding user with telegram id - {tg_id}: {e}.")
        await session.rollback()


@connection
async def remove_user(session, tg_id: str) -> Optional[BotUser]:
    try:
        user = await session.get(BotUser, tg_id)
        if not user:
            logger.error(f"User with id - {tg_id} has not found.")
            return None
        await session.delete(user)
        await session.commit()
        logger.info(f"User with id - {tg_id} removed.")
        return user
    except SQLAlchemyError as e:
        logger.error(f"Error while removing user with telegram id - {tg_id}: {e}.")
        await session.rollback()
        return None


@connection
async def update_user(session, tg_id: str, id_: str = None, description: str = None, medals: str = None) \
        -> Optional[BotUser]:
    try:
        user = await session.scalar(select(BotUser).filter_by(tg_id=tg_id))
        if not user:
            logger.error(f"User with telegram id - {tg_id} had not found.")
            return None

        if id_ is not None:
            user.id_ = id_
        if description is not None:
            user.description = description
        if medals is not None:
            user.medals = medals

        await session.commit()
        logger.info(f"User with telegram id {tg_id} updated.")
        return user
    except SQLAlchemyError as e:
        logger.error(f"Error while updating user with telegram id - {tg_id}: {e}")
        await session.rollback()


@connection
async def get_user_by_telegram_id(session, tg_id: str) -> Optional[Dict[str, Any]]:
    try:
        user = await session.get(BotUser, tg_id)
        if not user:
            logger.info(f"User with telegram id - {tg_id} had not found.")
            return None

        return {
            'tg_id': user.tg_id,
            'id_': user.id_,
            'description': user.description,
            'medals': user.medals
        }
    except SQLAlchemyError as e:
        logger.error(f"Error while getting user information by telegram id - {tg_id}: {e}")
        return None
