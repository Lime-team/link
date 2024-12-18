from aiogram import F, Router, types

from filters.chat_type import ChatTypeFilter
from filters.cmd import MessageFilter, ArgsMessageFilter

from database import set_user, get_user_by_telegram_id

from random import randint


router = Router()
router.message.filter(
    F.text,
    ChatTypeFilter(chat_type=['group', 'supergroup'])
)


@router.message(MessageFilter(['помощь', 'Помощь', 'помощ', 'Помощ', 'хелп', 'Хелп', '!help', '/help']))
async def cmd_help(message: types.Message):
    await message.answer("🧐 Помощь \nТы всегда можешь написать в чат @liinkyyhelp, если у тебя есть "
                         "вопрос \nДоступные команды находятся на <a href='https://docs.linkbot.run.place'>"
                         "сайте</a>", parse_mode="html")


@router.message(MessageFilter(['/random', '!rand', 'рандом', 'ранд', 'Рандом', 'Ранд']))
async def cmd_rand(message: types.Message):
    try:
        start = int(message.text.split()[1])
        end = int(message.text.split()[2])
        if start > end:
            await message.reply("Ошибка! Начальное число больше последнего!")
            return
    except IndexError:
        await message.reply("Ошибка! Недостаточно аргументов! \nПример: !rand 1 100")
        return
    await message.reply(f"Ваше случайное число... 😲\n{randint(start, end)}!")
