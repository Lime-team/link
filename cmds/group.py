from aiogram import F, Router

from filters.chat_type import ChatTypeFilter


router = Router()
router.message.filter(
    F.text,
    ChatTypeFilter(chat_type=['group', 'supergroup'])
)
