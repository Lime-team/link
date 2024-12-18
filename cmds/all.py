from aiogram import F, Router, types

from filters.chat_type import ChatTypeFilter
from filters.cmd import MessageFilter, ArgsMessageFilter
from filters.is_admin import IsBotAdmin

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
    await message.reply(f"😜 Вы - @{message.from_user.username}. \n🧐 Ваш id в системе линка: {user_info['id_']}."
                        f" \n👀 Описание - {user_info['description']}."
                        f" \n🦾 Награды (медали) - {user_info['medals']}")


@router.message(MessageFilter(['+описание', 'описание', '!description', '/description']),
                ChatTypeFilter(chat_type=['group', 'supergroup', 'private']))
async def cmd_update_description(message: types.Message):
    description = message.text.split()[1:]
    await update_user(tg_id=message.from_user.id, description=description)
    await message.reply("Описание изменено!")


@router.message(MessageFilter(['+медаль', '+награда', 'наградить', '!medal', '/medal']),
                ChatTypeFilter(chat_type=['group', 'supergroup', 'private']), IsBotAdmin())
async def cmd_update_medals(message: types.Message):
    id_ = message.text.split()[1]
    medals = message.text.split()[2:]
    user_info = await update_user(tg_id=id_, medals=medals)
    if user_info is None:
        await message.reply("Такого пользователя нет!")
    else:
        await message.reply("Всё успешно обновлено!")


@router.message(MessageFilter(['+айди', '!id', '/id']), ChatTypeFilter(chat_type=['group', 'supergroup', 'private']),
                IsBotAdmin())
async def cmd_update_id(message: types.Message):
    id_ = message.text.split()[1]
    id = message.text.split()[2]
    user_info = await update_user(tg_id=id_, id_=id)
    if user_info is None:
        await message.reply("Такого пользователя нет!")
    else:
        await message.reply("Всё успешно обновлено!")
