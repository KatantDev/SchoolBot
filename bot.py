from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import setup_application, SimpleRequestHandler
from aiohttp.web import run_app
from aiohttp.web_app import Application
from tgbot.routes.login import login_handler, check_data_handler, send_message_handler

from tgbot import config, handlers, database
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tgbot.utils import new_marks


async def on_startup(bot: Bot, base_url: str):
    await database.run_database()

    scheduler = AsyncIOScheduler()
    scheduler.add_job(new_marks.send_notify, "interval", minutes=5, args=(bot,))
    scheduler.start()

    response = await bot.set_webhook(f"{base_url}/{config.BOT_TOKEN}")


def main():
    import locale
    from tgbot.utils import logging

    locale.setlocale(locale.LC_ALL, "ru_RU.utf-8")

    bot = Bot(token=config.BOT_TOKEN, parse_mode='HTML')
    dispatcher = Dispatcher()
    dispatcher["base_url"] = config.APP_BASE_URL
    dispatcher.startup.register(on_startup)

    logging.setup()

    handlers.guest.setup(dispatcher)
    handlers.student.setup(dispatcher)
    handlers.admin.setup(dispatcher)

    app = Application()
    app["bot"] = bot

    app.router.add_get("/login", login_handler)
    app.router.add_post("/login/checkData", check_data_handler)
    app.router.add_post("/login/sendMessage", send_message_handler)
    SimpleRequestHandler(
        dispatcher=dispatcher,
        bot=bot,
    ).register(app, path=f"/{config.BOT_TOKEN}")
    setup_application(app, dispatcher, bot=bot)

    run_app(app, host="127.0.0.1", port=8080)


if __name__ == '__main__':
    main()
