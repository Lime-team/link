from asyncio import run, Event

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from aiogram.fsm.storage.memory import MemoryStorage

from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from aiohttp.web import AppRunner, TCPSite
from aiohttp.web_app import Application

import logging

from config_reader import config


async def on_start():
    await bot.delete_webhook(drop_pending_updates=True)
    if config.webhook.get_secret_value() == "TRUE":
        await bot.set_webhook(f"{config.webhook_base_url}/update")
    for admin_id in bot_admins:
        try:
            await bot.send_message(admin_id, f'Бот запущен!')
        except:
            pass


async def on_stop():
    try:
        for admin_id in bot_admins:
            await bot.send_message(admin_id, 'Бот остановлен. Но почему?..')
    finally:
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.session.close()


async def main():
    from cmds.group_moder import router as group_moder_router
    from cmds.group import router as group_router
    from cmds.direct import router as direct_router
    from cmds.all import router as all_router
    from bot_models import classic_model, random_mode
    from menu import mainkb, useit, aboutkb, pagination

    dp.include_routers(direct_router, group_router, group_moder_router, mainkb.router,
                       useit.router, aboutkb.router, pagination.router, classic_model.router,
                       random_mode.router, all_router)

    dp.startup.register(on_start)
    dp.shutdown.register(on_stop)

    if config.webhook.get_secret_value() == "TRUE":
        dp["base_url"] = config.webhook_base_url.get_secret_value()

        app = Application()

        SimpleRequestHandler(
            dispatcher=dp,
            bot=bot,
        ).register(app, path="/update")
        setup_application(app, dp, bot=bot)

        logger.info("Starting bot")

        runner = AppRunner(app)

        await runner.setup()
        site = TCPSite(runner, host=config.webhook_host.get_secret_value(), port=config.webhook_port.get_secret_value())
        await site.start()
        await Event().wait()
    else:
        await dp.start_polling(bot)


bot = Bot(token=config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode='html'))

storage = MemoryStorage()

dp = Dispatcher(storage=storage)

bot_admins = [int(id_) for id_ in config.admins_ids.get_secret_value().split(',')]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def start_bot():
    await main()
