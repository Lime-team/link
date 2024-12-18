from aiogram import F, Router  # , types

from filters.chat_type import ChatTypeFilter


router = Router()
router.message.filter(
    F.text,
    ChatTypeFilter('private')
)


# bot has giveaway part, if not uncomment all under this line
# @router.message()
# async def cmd_direct_response(message: types.Message):
#     await message.reply('Привет! Я работаю только в группах/супергруппах! Добавь меня туда '
#                         'с правами администратора и напиши !помощь')
