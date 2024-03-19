import logging
import asyncio

from aiogram import Bot
from aiogram.utils import markdown as md

import settings

from .workshop_parser import WorkshopParser
from .Analyzers import Analyzer, AnalyzerResult


class P2Arser:
    def __init__(self, config: settings.ConfigManager, tg_bot: Bot) -> None:
        self.config = config
        self.tg_bot = tg_bot
        
        self.parser = WorkshopParser(self.config["API_KEY"], self.config["game_id"]) # todo
        self.analyzer = Analyzer(self.config)
        
    
    async def analyze(self):
        logging.info("Search for new maps")
        new_workshop_items = await self.parser.get_new_maps()
        updated_workshop_items = await self.parser.get_updated_maps()
        
        for map in set(new_workshop_items + updated_workshop_items):
            result: AnalyzerResult = await self.analyzer.analys_item(map)
            if result is None:
                continue
            
            msg_text = self.create_description(result)   
            recipients = self.get_recipients(result)       
            for chat_id, found_words in recipients.items():  
                custom_msg_text = msg_text + "Desired Words: " + md.hitalic(', '.join(found_words))
                await self.send_info(int(chat_id), custom_msg_text, result.item.get_preview_url())
        
        self.analyzer.clear_cache()
        
        
    async def infinity_analyze(self):
        delay = self.config.get("delay")
        while True:
            await self.analyze()
            logging.info(f"Time to sleep {delay} seconds..")
            await asyncio.sleep(delay)
        

    def create_description(self, result: AnalyzerResult):
        return (md.hbold(f"{result.upload_type} with {result.find_type} found:\n") +
            f"Name: {md.hcode(result.item.get_title())}\n"
            f"Author: {md.hlink(result.item.get_creator_name(), result.item.get_creator_url())}\n"
            f"{md.hlink('[MAP LINK]', result.item.map_link)}\n")
        
        
    def get_recipients(self, found_words: AnalyzerResult):
        user_words = settings.UserData().info
        result = {}

        for user_id, words in user_words.items():
            common_words = found_words.desired & set(words)
            if common_words:
                result[user_id] = common_words

        return result
            
    
    async def send_info(self, chat_id, text, thumbnail_url):
        try:
            await self.tg_bot.send_photo(chat_id=chat_id, caption=text, photo=thumbnail_url)
        except Exception:
            text += "\n\nWarning! Unknown exception while getting thumbnail. This item may no longer exist"
            await self.tg_bot.send_message(chat_id=chat_id, text=text)