import logging
import datetime
from collections import deque
import WorkshopMetadataExtract as WME

from json_controller import ConfigManager

from .handlers.handler import AnalyzerHandler
from .handlers import item_bsp
from .handlers import item_description

from .result import AnalyzerResult

class ItemType:
    New = "New Map"
    Update = "Map Update"
    
    def get(workshop_item: WME.WorkshopItem):
        if workshop_item.get_time_updated() == workshop_item.get_time_created():
            return ItemType.New
        return ItemType.Update


class Analyzer:
    def __init__(self, config: ConfigManager) -> None:
        # self.config = config
        self.delay = config.get("delay")
        self.processed = deque(maxlen=100) # mb use `OrderedDict`?
        
        self.analyzers: list[AnalyzerHandler] = [
            item_bsp.BspAnalyzer(config).is_valid(),
            item_description.DescriptionAnalyzer(config).is_valid()
        ]
        
        if all(element is None for element in self.analyzers):
            logging.critical("All filters are disabled in the config, analyzer will never find a match!")
            exit("Filters are disabled in the config, program execution is useless!!")
        
        
    async def analys_item(self, workshop_item: WME.WorkshopItem) -> AnalyzerResult:
        map_updated_time = workshop_item.get_time_updated()
        time = datetime.datetime.now()
        timedelta = (time - map_updated_time).total_seconds()
    
        map_id = workshop_item.get_fileid()
        upload_type = ItemType.get(workshop_item)
        
        # if this map already processed or ...todo
        if upload_type == ItemType.Update and timedelta > self.delay:
            return None
        if map_id in self.processed: 
            return None
        
        # todo comment
        self.processed.append(map_id)
        
        megabytes_value = workshop_item.get_file_size() / 1024 / 1024
        
        logging.info(f"Main Analyzer ({upload_type}): \033[33m{workshop_item.get_title()}\033[0m")
        logging.debug(f"\ttimedelta: \033[90m{abs(timedelta)} seconds\033[0m\n"
                    f"\tUpload time: \033[90m{workshop_item.get_time_created()}\033[0m\n"
                    f"\tUpdate time: \033[90m{map_updated_time}\033[0m\n"
                    f"\tMap size: \033[90m{megabytes_value:.2f}mb\033[0m")
        
        # todo comment
        for handler in self.analyzers:
            if handler and (result := await handler.analyze(workshop_item)):
                logging.info(f"Main Analyzer: Found a match in the {handler}!")
                return AnalyzerResult(workshop_item, upload_type, str(handler), result)
        
    
    def clear_cache(self):
        self.processed.clear()

    def add_analyzer(self, handler: AnalyzerHandler):
        self.analyzers.append(handler.is_valid())