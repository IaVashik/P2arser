import asyncio
import logging
import coloredlogs

from aiogram import Bot
from aiogram.enums import ParseMode

import settings
from Workshop import P2Arser
from Telegram import bot

# * Add limits in config & update config
coloredlogs.install(level='INFO', fmt="%(asctime)s | %(levelname)s | %(message)s")

async def main() -> None:
    config = settings.ConfigManager("config.json")
    tg_bot = Bot(config["Tg_bot_token"], parse_mode=ParseMode.HTML)  
   
    await asyncio.gather(
        P2Arser(config, tg_bot).infinity_analyze(),
        bot.init(tg_bot)
    )        


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.warning("Bot stopped")
        settings.UserData().save_change()