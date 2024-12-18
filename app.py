async def on_start():
    for admin_id in bot_admins:
        try:
            await bot.send_message(admin_id, f'Бот запущен!')
        except:
            pass


async def on_stop():
    try:
        for admin_id in bot_admins:
            await bot.send_message(admin_id, 'Бот остановлен. Но почему?..')
    except:
        pass


async def main():
    from aiogram import Dispatcher

    dp = Dispatcher()

    dp.startup.register(on_start)
    dp.shutdown.register(on_stop)

    from cmds.group_moder import router as group_moder_router
    from cmds.group import router as group_router
    from cmds.direct import router as direct_router
    from cmds.all import router as all_router
    from bot_models import classic_model, random_mode
    from menu import mainkb, useit, aboutkb, pagination

    dp.include_routers(direct_router, group_router, group_moder_router, mainkb.router,
                       useit.router, aboutkb.router, pagination.router, classic_model.router,
                       random_mode.router, all_router)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


from config_reader import config
bot_admins = [int(id_) for id_ in config.admins_ids.get_secret_value().split(',')]

if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    from config_reader import config

    from aiogram import Bot
    from aiogram.client.default import DefaultBotProperties

    bot = Bot(token=config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode='html'))

    from asyncio import run

    run(main())
