import datetime

import WorkshopMetadataExtract as WME


class BSpAnalyzer:
    def __init__(self, config) -> None:
        self.processed = []
        self.config = config
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
        elif timedelta < 800 and map_updated_time == workshop_item.get_time_created():
            return None

        self.processed.append(map_id)

        log_postfix = self.get_item_type(workshop_item)
        
        # megabytes_value = workshop_item.get_file_size() / 1024 / 1024
        # print(f"{time}: \033[33m{MapItem.get_title()}\033[0m ({log_postfix})")
        # debug_print(f"\ttimedelta: \033[90m{abs(timedelta)} seconds\033[0m\n"
        #             f"\tUpload time: \033[90m{MapItem.get_time_created()}\033[0m\n"
        #             f"\tUpdate time: \033[90m{map_updated_time}\033[0m\n"
        #             f"\tMap size: \033[90m{megabytes_value:.2f}mb\033[0m")

        if self.check_content and self.check_map_content(workshop_item):
            return workshop_item + " with description"
            
            
        if self.check_description and self.check_map_description(workshop_item):
            return log_postfix + " with content"
        
        return None
            
            
    
    def get_item_type(_, workshop_item):
        if workshop_item.get_time_updated() == workshop_item.get_time_created():
            return "New map"
        return "Map Update" 
    
    
    def check_map_content(self, workshop_item):
        bsp_content = workshop_item.get_file_content()
        if bsp_content is None:
            return False
            
        bsp_content = bsp_content.decode("latin-1").lower()
        found_words = self._find_desired_words(bsp_content)
        if len(found_words) > 0:
            # await send_special_msg(MapItem, f"{log_postfix} with content found:", ", ".join(found_words))
            return True
        
        
    def check_map_description(self, workshop_item):
        description = workshop_item.get_description()
        if description is None:
            return False

        found_words = self._find_desired_words(description.lower())
        if len(found_words) > 0:
            return True
            # await send_special_msg(MapItem, f"{log_postfix} with description found:", ", ".join(found_words))
            
    
    def _find_desired_words(self, text: str) -> list[str]:
        found_words = []
        for desired_word in self.config["desired_content"]:
            if desired_word.lower() in text:
                found_words.append(desired_word)
        return found_words
    
    
    def clear_cache(self):
        self.processed.clear()