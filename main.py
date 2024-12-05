import asyncio

import logging
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, types, F
from filters.chat_type import ChatTypeFilter
from filters.cmd import MessageFilter
from aiogram.enums.chat_member_status import ChatMemberStatus

from config_reader import config


async def is_admin(message, bo):
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    b = await bo.get_chat_member(message.chat.id, bot.id)
    if message.from_user.id == 969043918:
        return True
    if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR] or b.status != ChatMemberStatus.ADMINISTRATOR:
        return False
    return True


logging.basicConfig(level=logging.ERROR)

bot = Bot(token=config.bot_token.get_secret_value())

dp = Dispatcher()


@dp.message(F.text, ChatTypeFilter('private'))
async def cmd_start(message: types.Message):
    await message.reply('Привет! Я работаю только в группах/супергруппах! Добавь меня туда '
                        'с правами администратора и напиши !помощь')


# @dp.message_text(F.text, ChatTypeFilter(['group', 'supergroup']))
# async def cmd_help(message_text: types.Message):
#     await message_text.reply()


@dp.message(F.text, ChatTypeFilter(['group', 'supergroup']), MessageFilter(['написать', 'Написать',
                                                                            '!write', '!send', '/write',
                                                                            'Отправить', '!написать', '!Написать']))
async def cmd_write(message: types.Message):
    if await is_admin(message, bot):
        if len(message.text.split()) > 1:
            await message.answer(" ".join(message.text.split()[1:]))
        else:
            await message.reply("Ошибка! \nПустой текст!")


@dp.message(F.text, ChatTypeFilter(['group', 'supergroup']), MessageFilter(['мут', 'Мут', 'Замутить', 'замутить',
                                                                            '!mute', '/mute', '-голос']))
async def cmd_mute(message: types.Message):
    name1 = message.from_user.mention_html()
    if not message.reply_to_message:
        await message.reply('Ошибка! Команда должна быть ответом на сообщение нарушителя!')
        return
    elif not await is_admin(message, bot):
        await message.reply('Ошибка! Вы не администратор группы!')
        return
    elif message.reply_to_message.from_user.id == 969043918:
        await message.reply('Произошла ошибка! Напишите в чат @liinkyyhelp')
        return
    try:
        mute_int = int(message.text.split()[1])
        mute_type = message.text.split()[2]
        reason = " ".join(message.text.split()[3:])
        repl = f'📢 🤐 Пользователь был лишён права голоса на {mute_int} {mute_type} ⏰. \n🙄 Наказал: {name1}. \n❓ Причина: {reason}'
    except IndexError:
        await message.reply('Не хватает аргументов!\nПример:\n`/mute 1 ч спам')
        return
    if mute_type == "ч" or mute_type == "часов" or mute_type == "час" or mute_type == "часа":
        dt = datetime.now() + timedelta(hours=mute_int)
        timestamp = dt.timestamp()
        await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id,
                                       types.ChatPermissions(can_send_messages=False), until_date=timestamp)
        await message.reply(repl, parse_mode='html')
    elif mute_type == "м" or mute_type == "мин" or mute_type == "минут" or mute_type == "минуты":
        dt = datetime.now() + timedelta(minutes=mute_int)
        timestamp = dt.timestamp()
        await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id,
                                       types.ChatPermissions(can_send_messages=False), until_date=timestamp)
        await message.reply(repl, parse_mode='html')
    elif mute_type == "д" or mute_type == "дней" or mute_type == "день" or mute_type == "дня":
        dt = datetime.now() + timedelta(days=mute_int)
        timestamp = dt.timestamp()
        await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id,
                                       types.ChatPermissions(can_send_messages=False), until_date=timestamp)
        await message.reply(repl, parse_mode='html')
    elif mute_type == "н" or mute_type == "нед" or mute_type == "неделя" or mute_type == "недели" or mute_type == "недель":
        dt = datetime.now() + timedelta(weeks=mute_int)
        timestamp = dt.timestamp()
        await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id,
                                       types.ChatPermissions(can_send_messages=False), until_date=timestamp)
        await message.reply(repl, parse_mode='html')


@dp.message(F.text, ChatTypeFilter(['group', 'supergroup']), MessageFilter(['размут', 'Размут', 'Размутить',
                                                                            'размутить', '!unmute', '!Unmute',
                                                                            '/unmute', '+голос']))
async def cmd_unmute(message: types.Message):
    if not message.reply_to_message or not await is_admin(message, bot):
        await message.reply('Ошибка! Команда должна быть ответом на сообщение нарушителя!')
        return
    await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id,
                                   types.ChatPermissions(can_send_messages=True))
    await message.reply("Пользователь был размучен! 😃")


@dp.message(F.text, ChatTypeFilter(['group', 'supergroup']), MessageFilter(['Бан', 'бан', 'забанить',
                                                                            'Забанить', '!ban', '/ban', '-чел']))
async def cmd_ban(message: types.Message):
    if not message.reply_to_message or not await is_admin(message, bot):
        await message.reply('Ошибка! Команда должна быть ответом на сообщение нарушителя!')
        return
    await bot.ban_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    await message.answer(f"Пользователь был забанен! ❌\nДля разбана обратись к администраторам группы 🤓")


@dp.message(F.text, ChatTypeFilter(['group', 'supergroup']), MessageFilter(['помощь', 'Помощь', 'помощ',
                                                                            'Помощ', 'хелп', 'Хелп', '!help',
                                                                            '/help']))
async def cmd_help(message: types.Message):
    await message.answer("🧐 Помощь \nТы всегда можешь написать в чат @liinkyyhelp, если у тебя есть "
                         "вопрос \nДоступные команды находятся на <a href='https://limeteam.gitbook.io/link'>"
                         "сайте</a>",
                         parse_mode='html')


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
