import asyncio

import logging
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, types, F
from filters.chat_type import ChatTypeFilter
from filters.cmd import MessageFilter

from config_reader import config

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
    try:
        mute_int = int(message.text.split()[1])
        mute_type = message.text.split()[2]
        reason = " ".join(message.text.split()[3:])
        repl = f'📢 🤐 Пользователь был лишён права голоса на {mute_int} {mute_type} ⏰. \n🙄 Наказал: {name1}. \n❓ Причина: {reason}'
    except IndexError:
        await message.reply('Не хватает аргументов!\nПример:\n`/мут 1 ч спам')
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


@dp.message(F.text, ChatTypeFilter(['group', 'supergroup']), MessageFilter(['размут', 'Размут', 'Размутить', 'размутить',
                                                                            '!unmute', '/unmute', '+голос']))
async def cmd_unmute(message: types.Message):
    if not message.reply_to_message:
        await message.reply('Ошибка! Команда должна быть ответом на сообщение нарушителя!')
        return
    await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id,
                                   types.ChatPermissions(can_send_messages=True))
    await message.reply("Пользователь был размучен! 😃")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
