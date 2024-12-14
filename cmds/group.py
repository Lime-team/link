import asyncio

from aiogram import F, Router, types

from filters.chat_type import ChatTypeFilter
from filters.cmd import MessageFilter, Args2MessageFilter

from db import db

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


@router.message(Args2MessageFilter(['кто я', 'хто я', 'ктоя', 'хтоя', '!about_me', '/about_me', 'about',
                                    'who am i']))
async def cmd_about_me(message: types.Message):
    loop = asyncio.get_event_loop()
    d = await db.get('users', 'description', 'tg_id',
                                             message.from_user.id, loop)
    i = await db.get('users', 'icon', 'tg_id',
                                             message.from_user.id, loop)
    tg_id = await db.get('users', 'tg_id', 'tg_id',
                                             message.from_user.id, loop)
    id = await db.get('users', 'id', 'tg_id',
                                             message.from_user.id, loop)
    if not tg_id:
        await db.set_user('users', message.from_user.id, 'нет', 'нет', loop)
        return message.reply("Вы были успешно зарегистрированы в системе Линка! Напишите команду ещё раз")
    return message.reply(f"Вы - @{message.from_user.username}. Ваш id в системе линка: {id[0][0]}. "
                         f"Описание - {d[0][0]}. Значки - {i[0][0]}")
