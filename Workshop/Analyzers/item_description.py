from typing import Union
import WorkshopMetadataExtract as WME
from .handler import AnalyzerHandler

class DescriptionAnalyzer(AnalyzerHandler):
    async def analyze(self, workshop_item: WME.WorkshopItem) -> Union[list[str], None]:
        description = workshop_item.get_description()
        if description is None:
            return False

        found_words = await self._find_desired_words(description.lower())
        if len(found_words) > 0:
            return found_words
    
    def __str__(self):
        return "item description"
    
    def is_valid(self):
        return self if self.config.get("check_map_description") else None