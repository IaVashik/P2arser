import time
import asyncio
import logging
import coloredlogs

import settings
import notification
from WorkshopParser import WorkshopParser
from BspAnalyzer import BSpAnalyzer, AnalyzerResult

coloredlogs.install(level='INFO', fmt="%(asctime)s | %(levelname)s | %(message)s")

async def main() -> None:
    config = settings.ConfigManager("config.json")
    tg_bot = notification.tgBot(config["Tg_bot_token"])
    parser = WorkshopParser(config["API_KEY"], config["game_id"]) # todo
    analyzer = BSpAnalyzer(config)
        
    while True:
        logging.info("Search for new maps")
        new_workshop_items = await parser.get_new_maps()
        updated_workshop_items = await parser.get_updated_maps()
        
        for map in (new_workshop_items + updated_workshop_items):
            result: AnalyzerResult = await analyzer.analys_item(map)
            if result is None:
                continue
            thumbnail_url = result.item.get_preview_url()
            await tg_bot.bot.send_photo(chat_id=config["Tg_chat_id"], caption=result.create_description(), photo=thumbnail_url)
        
        analyzer.clear_cache()
        delay = config.get("delay")
        logging.info(f"Time to sleep {delay} seconds..")
        time.sleep(delay)
        
asyncio.run(main())