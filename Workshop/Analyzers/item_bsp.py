import logging
import aiohttp

from typing import Union
import WorkshopMetadataExtract as WME
from .handler import AnalyzerHandler

# TODO config read where??
class BspAnalyzer(AnalyzerHandler):
    async def analyze(self, workshop_item: WME.WorkshopItem) -> Union[list[str], None]:
        logging.debug(f"Bsp Analyzer Handler: start download bsp content ({workshop_item.get_filename()})")
        url = workshop_item.get_file_url()
        if url is None:
            return False

        async with aiohttp.ClientSession() as session: # TODO! What if the map weighs too much -> crash
            async with session.get(url) as response:
                if response.status == 200:
                    bsp_content = await response.read()
                else:
                    print(f"File upload error. Status code: {response.status}")
                    return False
        
        bsp_content = bsp_content.decode("latin-1").lower() # uuught todo optimize it
        found_words = await self._find_desired_words(bsp_content)
        if len(found_words) > 0:
            return found_words
    
    def __str__(self):
        return "map content"
    
    def is_valid(self):
        return self if self.config.get("check_map_content") else None