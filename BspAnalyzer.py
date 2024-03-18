import datetime
import logging

import WorkshopMetadataExtract as WME

class AnalyzerResult:
    def __init__(self, map_item: WME.WorkshopItem, upload_type, find_type, desired) -> None:
        self.item = map_item
        self.upload_type = upload_type
        self.find_type = find_type
        self.desired_list = desired
        
    def create_description(self):
        return (f"{self.upload_type} with {self.find_type} found:\n"
                f"Name: {self.item.get_title()}\n"
                f"Author: {self.item.get_creator_name()}\n"
                f"[Map Link]({self.item.map_link})\n"
                f"Desired Words: {', '.join(self.desired_list)}")
        
        
class BSpAnalyzer:
    def __init__(self, config, desired_words = []) -> None:
        self.processed = []
        self.config = config
        self.desired_words = desired_words
        self.check_content = config.get("check_map_content")
        self.check_description = config.get("check_map_description")
    
    
    async def analys_item(self, workshop_item: WME.WorkshopItem) -> bool:        
        map_id = workshop_item.get_fileid()
        map_updated_time = workshop_item.get_time_updated()
        time = datetime.datetime.now()
        timedelta = (time - map_updated_time).total_seconds()
        # time = time.strftime('%m.%d %H:%M:%S')

        if map_id in self.processed and timedelta > self.config.get("delay"): 
            return None
        # TODO what is it? XD
        # elif timedelta < 800 and map_updated_time == workshop_item.get_time_created():
        #     return None

        self.processed.append(map_id)

        upload_type = self.get_item_type(workshop_item)
        
        megabytes_value = workshop_item.get_file_size() / 1024 / 1024
        logging.info(f"BSP Analyzer ({upload_type}): \033[33m{workshop_item.get_title()}\033[0m")
        logging.debug(f"\ttimedelta: \033[90m{abs(timedelta)} seconds\033[0m\n"
                    f"\tUpload time: \033[90m{workshop_item.get_time_created()}\033[0m\n"
                    f"\tUpdate time: \033[90m{map_updated_time}\033[0m\n"
                    f"\tMap size: \033[90m{megabytes_value:.2f}mb\033[0m")

        if self.check_content and (desired := await self.check_map_content(workshop_item)):
            logging.info("Found a match in the map content!")
            return AnalyzerResult(workshop_item, upload_type, "map content", desired)
            
            
        if self.check_description and (desired := await self.check_map_description(workshop_item)):
            logging.info("Found a match in the item description!")
            return AnalyzerResult(workshop_item, upload_type, "item description", desired)
        
        if not self.check_description and not self.check_content:
            logging.error("Both filters are disabled in the config, analyzer will never find a match!")
        
        return None
            
    
    def get_item_type(_, workshop_item):
        if workshop_item.get_time_updated() == workshop_item.get_time_created():
            return "New map"
        return "Map Update" 
    
    
    async def check_map_content(self, workshop_item):
        bsp_content = workshop_item.get_file_content()
        if bsp_content is None:
            return False
            
        bsp_content = bsp_content.decode("latin-1").lower()
        found_words = await self._find_desired_words(bsp_content)
        if len(found_words) > 0:
            return found_words
        
        
    async def check_map_description(self, workshop_item):
        description = workshop_item.get_description()
        if description is None:
            return False

        found_words = await self._find_desired_words(description.lower())
        if len(found_words) > 0:
            return found_words
            
    
    async def _find_desired_words(self, text: str) -> list[str]:
        found_words = []
        for desired_word in self.desired_words:
            if desired_word in text:
                found_words.append(desired_word)
        return found_words
    
    
    def clear_cache(self):
        self.processed.clear()