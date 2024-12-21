from aiogram import F, Router, types

from filters.chat_type import ChatTypeFilter
from filters.is_admin import IsBotAdmin
from filters.cmd import MessageFilter, ArgsMessageFilter

from random import randint

from database import set_user, get_user_by_telegram_id, update_user

router = Router()
router.message.filter(
    F.text,
    ChatTypeFilter(chat_type=['group', 'supergroup', 'private'])
)


@router.message(ArgsMessageFilter(['кто я', 'хто я', 'ктоя', 'хтоя', '!about_me', '/about_me', 'about',
                                   'who am i']))
async def cmd_about_me(message: types.Message):
    user = await set_user(tg_id=message.from_user.id)
    if user is None:
        await message.reply("👋 Вы были успешно зарегистрированы в системе Линка, так как до этого не"
                            " использовали бота!")
    user_info = await get_user_by_telegram_id(tg_id=message.from_user.id)
    if user_info is None:
        await message.reply("Произошла ошибка! Пользователь не найден! Напиши в чат @liinkyyhelp")
        return
    await message.reply(f"😜 Вы - {message.from_user.first_name} {message.from_user.last_name},"
                        f" @{message.from_user.username}."
                        f"\n🧐 Ваш id в системе линка: {user_info['id_']}."
                        f" \n👀 Описание - {user_info['description']}."
                        f" \n🦾 Награды (медали) - {user_info['medals']}")


@router.message(MessageFilter(['+описание', 'описание', '!description', '/description']),
                ChatTypeFilter(chat_type=['group', 'supergroup', 'private']))
async def cmd_update_description(message: types.Message):
    description = " ".join(message.text.split()[1:])
    await update_user(tg_id=message.from_user.id, description=description)
    await message.reply("Описание изменено!")


@router.message(MessageFilter(['+медаль', '+награда', 'наградить', '!medal', '/medal']),
                ChatTypeFilter(chat_type=['group', 'supergroup', 'private']), IsBotAdmin())
async def cmd_update_medals(message: types.Message):
    tg_id = message.text.split()[1]
    medals = " ".join(message.text.split()[2:])
    user_info = await update_user(tg_id=tg_id, medals=medals)
    if user_info is None:
        await message.reply("Такого пользователя нет!")
    else:
        await message.reply("Всё успешно обновлено!")


@router.message(MessageFilter(['+айди', '!id', '/id']), ChatTypeFilter(chat_type=['group', 'supergroup', 'private']),
                IsBotAdmin())
async def cmd_update_id(message: types.Message):
    tg_id = message.text.split()[1]
    id_ = message.text.split()[2]
    user_info = await update_user(tg_id=tg_id, id_=id_)
    if user_info is None:
        await message.reply("Такого пользователя нет!")
    else:
        await message.reply("Всё успешно обновлено!")


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
