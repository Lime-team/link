from aiogram import F, Router, types

from filters.chat_type import ChatTypeFilter


router = Router()


@router.message(F.text, ChatTypeFilter('private'))
async def cmd_start(message: types.Message):
    await message.reply('Привет! Я работаю только в группах/супергруппах! Добавь меня туда '
                        'с правами администратора и напиши !помощь')
