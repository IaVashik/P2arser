import logging
import aiohttp
from tqdm import tqdm
from bs4 import BeautifulSoup
import WorkshopMetadataExtract as WME


class WorkshopParser:
    def __init__(self, steam_api_key, game_id) -> None:
        WME.set_api_key(steam_api_key)
        
        # todo?
        workshop_url = f"https://steamcommunity.com/workshop/browse/?appid={game_id}&browsesort="
        self.new_map_url = workshop_url + 'mostrecent'
        self.updated_map_url = workshop_url + 'lastupdated'
            
    
    async def get_new_items(self, url: str) -> list[WME.WorkshopItem]:
        logging.info(f"Start parsing workshop page ({url})")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()

                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                workshop_items = soup.select('.workshopItem')
                maps = []

                for item in tqdm(workshop_items):
                    url = item.select_one('.item_link')['href']

                    try:
                        map_item = WME.WorkshopItem(url)
                    except Exception:
                        continue
                    
                    if map_item is None:
                        continue

                    maps.append(map_item)
                    logging.debug(f"* {map_item.get_title()}")

                return maps
            
    
    async def get_new_maps(self) -> list[WME.WorkshopItem]:
        return await self.get_new_items(self.new_map_url)
    
    async def get_updated_maps(self) -> list[WME.WorkshopItem]:
        return await self.get_new_items(self.updated_map_url)