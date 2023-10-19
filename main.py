import asyncio
import datetime

from bs4 import BeautifulSoup
import aiohttp

from utils import *

# List to store processed maps and workshop URLs
processed_maps = []
workshop_urls = []


# Fetch workshop items from a given URL
async def GetWorkshopItems(url: str) -> list[WME.WorkshopItem]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()

            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            workshop_items = soup.select('.workshopItem')
            maps = []

            for item in workshop_items:
                url = item.select_one('.item_link')['href']

                if url in workshop_urls:
                    continue
                workshop_urls.append(url)

                map_item = WME.WorkshopItem(url)
                maps.append(map_item)
                debug_print(f"\033[90m{map_item.get_title()}", end=", ")

            return maps


# Process workshop items
async def process_workshop_items(workshop_items: list[WME.WorkshopItem]) -> bool:
    result = False
    
    for MapItem in workshop_items:
        map_id = MapItem.get_fileid()
        time = datetime.datetime.now()
        map_updated_time = MapItem.get_time_updated()
        timedelta = (time - map_updated_time).total_seconds()
        time = time.strftime('%m.%d %H:%M:%S')

        if map_id in processed_maps and timedelta > 800:
            continue
        elif timedelta < 800 and map_updated_time == MapItem.get_time_created():
            continue

        processed_maps.append(map_id)
        result = True

        log_postfix = ""
        if map_updated_time == MapItem.get_time_created():
            log_postfix = "New map"
        else:
            log_postfix = "Map Update"
        
        megabytes_value = MapItem.get_file_size() / 1024 / 1024
        
        print(f"{time}: \033[33m{MapItem.get_title()}\033[0m ({log_postfix})")
        debug_print(f"\ttimedelta: \033[90m{abs(timedelta)} seconds\033[0m\n"
                    f"\tUpload time: \033[90m{MapItem.get_time_created()}\033[0m\n"
                    f"\tUpdate time: \033[90m{map_updated_time}\033[0m\n"
                    f"\tMap size: \033[90m{megabytes_value:.2f}mb\033[0m")

        if config["Check_map_content"] is True:
            bsp_content = MapItem.get_file_content()
            if bsp_content is None:
                continue
            bsp_content = bsp_content.decode("latin-1").lower()
            found_words = find_desired_words(bsp_content)
            if len(found_words) > 0:
                await send_special_msg(MapItem, f"{log_postfix} with content found:", ", ".join(found_words))
                continue
            
        if config["Check_map_description"] is True:
            description = MapItem.get_description()
            if description is None:
                continue

            found_words = find_desired_words(description.lower())
            if len(found_words) > 0:
                await send_special_msg(MapItem, f"{log_postfix} with description found:", ", ".join(found_words))
    
    return result


# Find desired words in the bsp
def find_desired_words(text: str) -> list[str]:
    found_words = []
    for desired_word in config["desired_content"]:
        if desired_word.lower() in text:
            found_words.append(desired_word)
    return found_words


# Main function to run the program
async def main():
    workshop_url = f"https://steamcommunity.com/workshop/browse/?appid={config['game_id']}&browsesort="
    workshop_new_map = workshop_url + 'mostrecent'
    workshop_updated_map = workshop_url + 'lastupdated'

    while True:
        time = datetime.datetime.now().strftime('%m.%d %H:%M:%S')
        print(f"{time}: \033[95mSearch for new maps:\033[0m")

        workshop_urls.clear()
        new_workshop_items = await GetWorkshopItems(workshop_new_map)
        updated_workshop_items = await GetWorkshopItems(workshop_updated_map)

        debug_print("\n\033[0m" + "="*100 + "\n"
                    "Links to maps have been detected, starting the analysis...")

        process_success = await process_workshop_items(new_workshop_items + updated_workshop_items)
        if process_success is False:
            print("\033[36mNo new/updated map found\033[0m")

        # Delay before the next iteration
        now = datetime.datetime.now()
        delay = config["delay"]
        delay_time = now + datetime.timedelta(seconds=delay)
        print(f"{now.strftime('%m.%d %H:%M:%S')}: \033[36mWaiting {delay_time.strftime('%H:%M:%S')}...\033[0m")
        await asyncio.sleep(delay)  


asyncio.run(main())