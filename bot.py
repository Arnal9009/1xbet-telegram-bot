import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from config import settings
from middlewares.i18n import I18nMiddleware
from handlers import start, topup, withdraw, admin

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

PID_FILE = "/tmp/xbet_bot.pid"


def check_single_instance() -> None:
    if os.path.exists(PID_FILE):
        try:
            old_pid = int(open(PID_FILE).read().strip())
            os.kill(old_pid, 0)
            logging.error(f"Бот уже запущен (PID {old_pid}). Завершаем.")
            sys.exit(1)
        except (ProcessLookupError, ValueError):
            pass
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))


def remove_pid_file() -> None:
    try:
        os.remove(PID_FILE)
    except FileNotFoundError:
        pass


async def main() -> None:
    check_single_instance()

    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота / Start / Ботту баштоо"),
    ])

    dp.message.middleware(I18nMiddleware())
    dp.callback_query.middleware(I18nMiddleware())

    dp.include_router(start.router)
    dp.include_router(topup.router)
    dp.include_router(withdraw.router)
    dp.include_router(admin.router)

    logging.info("Bot started")
    try:
        await dp.start_polling(bot)
    finally:
        remove_pid_file()


if __name__ == "__main__":
    asyncio.run(main())
