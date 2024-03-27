import asyncio
import logging
import coloredlogs

from aiogram import Bot
from aiogram.enums import ParseMode

import json_controller
from Workshop import P2Arser
from Telegram import bot

# * Add limits in config & update config
logger_fmt = "%(asctime)s | %(levelname)s | %(message)s"
coloredlogs.install(level='INFO', fmt=logger_fmt)
file_handler = logging.FileHandler('logs.log')
file_handler.setFormatter(logging.Formatter(fmt=logger_fmt))
logging.getLogger().addHandler(file_handler)


async def main() -> None:
    config = json_controller.ConfigManager("config.json")
    tg_bot = Bot(config["Tg_bot_token"], parse_mode=ParseMode.HTML)  
   
    try:
        await asyncio.gather(
            P2Arser(config, tg_bot).infinity_analyze(),
            bot.init(tg_bot)
        )
    except (asyncio.exceptions.CancelledError, KeyboardInterrupt) as err:
        logging.warning("Bot stopped")
        json_controller.UserData().save_change()


if __name__ == "__main__":
    asyncio.run(main())