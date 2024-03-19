from typing import Union
import WorkshopMetadataExtract as WME
from .handler import AnalyzerHandler

# TODO config read where??
class BspAnalyzer(AnalyzerHandler):
    async def analyze(self, workshop_item: WME.WorkshopItem) -> Union[list[str], None]:
        bsp_content = workshop_item.get_file_content() # TODO optimize it!
        if bsp_content is None:
            return False
            
        bsp_content = bsp_content.decode("latin-1").lower() # uuught todo optimize it
        found_words = await self._find_desired_words(bsp_content)
        if len(found_words) > 0:
            return found_words
    
    def __str__(self):
        return "map content"
    
    def is_valid(self):
        return self if self.config.get("check_map_content") else None