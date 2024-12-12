from aiogram.enums.chat_member_status import ChatMemberStatus
from config_reader import config


async def is_admin(message, bo):
    member = await bo.get_chat_member(message.chat.id, message.from_user.id)
    b = await bo.get_chat_member(message.chat.id, bo.id)
    if message.from_user.id == config.admin_id.get_secret_value():
        return True
    if (member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR] or
            b.status != ChatMemberStatus.ADMINISTRATOR):
        return False
    return True
