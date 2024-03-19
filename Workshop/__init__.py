import logging
import asyncio

from aiogram import Bot
from aiogram.utils import markdown as md

import settings

from .workshop_parser import WorkshopParser
from .Analyzers import Analyzer, AnalyzerResult


async def analyze(config: settings.ConfigManager, tg_bot: Bot):
    parser = WorkshopParser(config["API_KEY"], config["game_id"]) # todo
    analyzer = Analyzer(config)

    while True:
        logging.info("Search for new maps")
        new_workshop_items = await parser.get_new_maps()
        updated_workshop_items = await parser.get_updated_maps()
        
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
                await tg_bot.send_photo(chat_id=config["Tg_chat_id"], caption=caption, photo=thumbnail_url) # uuugh, yeaaah... bb
            except Exception:
                caption += "\n\nWarning! Unknown exception while getting thumbnail. This item may no longer exist"
                await tg_bot.send_message(chat_id=config["Tg_chat_id"], text=caption)
        
        analyzer.clear_cache()
        delay = config.get("delay")
        logging.info(f"Time to sleep {delay} seconds..")
        await asyncio.sleep(delay)