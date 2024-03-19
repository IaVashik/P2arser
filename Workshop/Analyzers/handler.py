from typing import Union
from settings import ConfigManager, UserData
import WorkshopMetadataExtract as WME

class AnalyzerHandler:
    def __init__(self, config: ConfigManager) -> None:
        self.config = config

    
    async def analyze(self, workshop_item: WME.WorkshopItem) -> Union[list[str], None]:
        pass
    

    async def _find_desired_words(self, text: str) -> set[str]:
        found_words = set()
        
        for desired_word in UserData().get_unique_words():
            if desired_word in text:
                found_words.add(desired_word)
        
        return found_words
    
        
    def is_valid(self):
        return self if self.config.get("filter_name") else None
        
    def __str__(self):
        return "unknown (item handler)"