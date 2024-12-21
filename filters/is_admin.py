from aiogram.enums.chat_member_status import ChatMemberStatus

from aiogram.filters import BaseFilter
from aiogram.types import Message

from app import bot_admins


async def is_group_admin(message, bo):
    member = await bo.get_chat_member(message.chat.id, message.from_user.id)
    b = await bo.get_chat_member(message.chat.id, bo.id)
    if message.from_user.id in bot_admins:
        return True
    if (member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR] or
            b.status != ChatMemberStatus.ADMINISTRATOR):
        return False
    return True


class IsBotAdmin(BaseFilter):
    def __init__(self):
        pass

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in bot_admins

