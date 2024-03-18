import asyncio
import logging
import coloredlogs
from itertools import chain

from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.utils import markdown as md

import settings
import jsonDB
import TelegramBot
from WorkshopParser import WorkshopParser
from BspAnalyzer import BSpAnalyzer, AnalyzerResult


coloredlogs.install(level='INFO', fmt="%(asctime)s | %(levelname)s | %(message)s")


async def main() -> None:
    config = settings.ConfigManager("config.json")
    db = jsonDB.JsonDatabase()
    tg_bot = Bot(config["Tg_bot_token"], parse_mode=ParseMode.HTML)     
    await asyncio.gather(
        analyze(config, tg_bot, db),
        # TelegramBot.init_bot(tg_bot, db)
    )
    
    
async def analyze(config: settings.ConfigManager, tg_bot: Bot, db: jsonDB.JsonDatabase):
    parser = WorkshopParser(config["API_KEY"], config["game_id"]) # todo
    analyzer = BSpAnalyzer(config)
    users_words = db.load_table("users").data

    while True:
        logging.info("Search for new maps")
        new_workshop_items = await parser.get_new_maps()
        updated_workshop_items = await parser.get_updated_maps()
        
        # todo update rarely!
        all_words = set()
        for value in users_words.values():
            all_words.update(value)

        analyzer.desired_words = all_words # todo code
        
        for map in set(new_workshop_items + updated_workshop_items):
            result: AnalyzerResult = await analyzer.analys_item(map)
            if result is None:
                continue
            
            thumbnail_url = result.item.get_preview_url()
            caption = (md.hbold(f"{result.upload_type} with {result.find_type} found:\n") +
                f"Name: {md.hcode(result.item.get_title())}\n"
                f"Author: {md.hlink(result.item.get_creator_name(), result.item.get_creator_url())}\n"
                f"{md.hlink('[MAP LINK]', result.item.map_link)}\n"
                f"Desired Words: " + md.hitalic(', '.join(result.desired_list)))
            
            try:
                if thumbnail_url == "https://steamuserimages-a.akamaihd.net/ugc/2017083277472492412/EB235572BEC9027955BE30941C38AC1E72344323/":
                    await tg_bot.send_photo(chat_id=config["Tg_chat_id"], caption=caption, photo=thumbnail_url) # uuugh, yeaaah... bb
            except Exception:
                caption += "\n\nWarning! Unknown exception while getting thumbnail. This item may no longer exist"
                await tg_bot.send_message(chat_id=config["Tg_chat_id"], text=caption)
        
        analyzer.clear_cache()
        delay = config.get("delay")
        logging.info(f"Time to sleep {delay} seconds..")
        await asyncio.sleep(delay)
        

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.warning("Bot stopped")