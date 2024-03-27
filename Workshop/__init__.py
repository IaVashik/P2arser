import logging
import asyncio

from aiohttp.client_exceptions import ClientResponseError
from aiogram import Bot
from aiogram.utils import markdown as md

import json_controller

from .workshop_parser import WorkshopParser
from .Analyzers import Analyzer, AnalyzerResult


class P2Arser:
    def __init__(self, config, tg_bot: Bot) -> None:
        self.config = config
        self.tg_bot = tg_bot
        
        self.parser = WorkshopParser(self.config["steam_api_key"], self.config["game_id"])
        self.analyzer = Analyzer(self.config)
        
    
    async def analyze(self) -> bool:
        logging.info("Search for new maps")
        try:
            new_workshop_items = await self.parser.get_new_maps()
            updated_workshop_items = await self.parser.get_updated_maps()
        except ClientResponseError as err:
            logging.warning(f"Error when parsing a page! ({err})")
            return False
        
        for map in set(new_workshop_items + updated_workshop_items):
            result: AnalyzerResult = await self.analyzer.analys_item(map)
            if result is None:
                continue
            
            msg_text = self.create_description(result)   
            recipients = self.get_recipients(result)       
            for chat_id, found_words in recipients.items():  
                custom_msg_text = msg_text + "Desired Words: " + md.hitalic(', '.join(found_words))
                msg = await self.send_info(int(chat_id), custom_msg_text, result.item.get_preview_url())
                logging.info(f"User {msg.chat.full_name} ({msg.chat.id}) got a match on the following words: {found_words}. Map Link: {result.item.map_link}")
        
        self.analyzer.clear_cache()
        return True
        
        
    async def infinity_analyze(self):
        delay = self.config.get("delay")
        try:
            while True:
                result = await self.analyze()
                if not result:
                    await asyncio.sleep(60)
                    continue
                logging.info(f"Time to sleep {delay} seconds..")
                await asyncio.sleep(delay)
        except KeyboardInterrupt:
            logging.warning("P2Arser analysis stopped")
        

    def create_description(self, result: AnalyzerResult):
        return (md.hbold(f"{result.upload_type} with {result.find_type} found:\n") +
            f"Name: {md.hcode(result.item.get_title())}\n"
            f"Author: {md.hlink(result.item.get_creator_name(), result.item.get_creator_url())}\n"
            f"{md.hlink('[MAP LINK]', result.item.map_link)}\n")
        
        
    def get_recipients(self, found_words: AnalyzerResult):
        user_words = json_controller.UserData().data
        result = {}

        for user_id, words in user_words.items():
            common_words = found_words.desired & set(words)
            if common_words:
                result[user_id] = common_words

        return result
            
    
    async def send_info(self, chat_id, text, thumbnail_url):
        try:
            msg = await self.tg_bot.send_photo(chat_id=chat_id, caption=text, photo=thumbnail_url)
        except Exception:
            text += "\n\nWarning! Unknown exception while getting thumbnail. This item may no longer exist"
            msg = await self.tg_bot.send_message(chat_id=chat_id, text=text)
        return msg