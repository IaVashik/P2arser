import time
import asyncio

import settings
import notification
from WorkshopParser import WorkshopParser
from BspAnalyzer import BSpAnalyzer


async def main() -> None:
    config = settings.ConfigManager("config.json")
    tg_bot = notification.tgBot(config["Tg_bot_token"])
    parser = WorkshopParser(config["API_KEY"], config["game_id"]) # todo
    analyzer = BSpAnalyzer(config)
        
    while True:
        print("Search for new maps")
        new_workshop_items = await parser.get_new_maps()
        updated_workshop_items = await parser.get_updated_maps()
        
        for map in (new_workshop_items + updated_workshop_items):
            result = await analyzer.analys_item(map)
            if result is None:
                continue
            await tg_bot.send(config["Tg_chat_id"], result + " todo")
        
        analyzer.clear_cache()
        time.sleep(config.get("delay"))
        
asyncio.run(main())