from aiogram import F, Router, types, Bot

from datetime import datetime, timedelta

from filters.chat_type import ChatTypeFilter
from filters.cmd import MessageFilter
from filters.is_admin import is_admin

router = Router()


@router.message(F.text, ChatTypeFilter(['group', 'supergroup']), MessageFilter(['мут', 'Мут', 'Замутить', 'замутить',
                                                                            '!mute', '/mute', '-голос']))
async def cmd_mute(message: types.Message, bot: Bot):
    name1 = message.from_user.mention_html()
    if not message.reply_to_message:
        await message.reply('Ошибка! Команда должна быть ответом на сообщение нарушителя!')
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


@router.message(F.text, ChatTypeFilter(['group', 'supergroup']), MessageFilter(['размут', 'Размут', 'Размутить',
                                                                            'размутить', '!unmute', '!Unmute',
                                                                            '/unmute', '+голос']))
async def cmd_unmute(message: types.Message, bot: Bot):
    if not message.reply_to_message:
        await message.reply('Ошибка! Команда должна быть ответом на сообщение нарушителя!')
        return
    await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id,
                                   types.ChatPermissions(can_send_messages=True))
    await message.reply("Пользователь был размучен! 😃")


@router.message(F.text, ChatTypeFilter(['group', 'supergroup']), MessageFilter(['Бан', 'бан', 'забанить',
                                                                            'Забанить', '!ban', '/ban', '-чел']))
async def cmd_ban(message: types.Message, bot: Bot):
    if not message.reply_to_message:
        await message.reply('Ошибка! Команда должна быть ответом на сообщение нарушителя!')
        return
    await bot.ban_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    await message.answer(f"Пользователь был забанен! ❌\nДля разбана обратись к администраторам группы 🤓")


@router.message(F.text, ChatTypeFilter(['group', 'supergroup']), MessageFilter(['написать', 'Написать',
                                                                            '!write', '!send', '/write',
                                                                            'Отправить', '!написать', 'отправить']))
async def cmd_write(message: types.Message, bot: Bot):
    if await is_admin(message, bot):
        if len(message.text.split()) > 1:
            mt = message.text
            for i in range(len(message.text)):
                if message.text[i] == ' ':
                    mt = message.text[i + 1:]
            await message.answer(mt)
        else:
            await message.reply("Ошибка! \nПустой текст!")
