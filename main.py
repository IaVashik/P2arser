import asyncio
import logging
import coloredlogs

from aiogram import Bot
from aiogram.enums import ParseMode

import settings
import Workshop
from Telegram import bot


coloredlogs.install(level='INFO', fmt="%(asctime)s | %(levelname)s | %(message)s")

async def main() -> None:
    config = settings.ConfigManager("config.json")
    tg_bot = Bot(config["Tg_bot_token"], parse_mode=ParseMode.HTML)  
   
    await asyncio.gather(
        Workshop.analyze(config, tg_bot),
        bot.init(tg_bot)
    )        


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.warning("Bot stopped")
        settings.UserData().save_change()