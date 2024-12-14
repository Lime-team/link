async def main():
    import logging

    from aiogram import Bot, Dispatcher
    from aiogram.client.default import DefaultBotProperties

    from config_reader import config

    logging.basicConfig(level=logging.ERROR)

    bot = Bot(token=config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode='html'))

    dp = Dispatcher()

    from cmds.group_moder import router as group_moder_router
    from cmds.group import router as group_router
    from cmds.direct import router as direct_router

    dp.include_routers(direct_router, group_router, group_moder_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    from asyncio import run
    run(main())
