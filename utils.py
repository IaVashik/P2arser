import json

import WorkshopMetadataExtract as WME
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode


# Load the configuration from a JSON file
with open("config.json", "r") as file:
    config = json.load(file)

# Set the API key
WME.set_api_key(config["API_KEY"])

# Get the Telegram bot token, chat ID, and debug flag from the configuration file
BOT_TOKEN = config["Tg_bot_token"]
CHAT_ID = config["Tg_chat_id"]
DEBUG = config["DEBUG"]

# Create a bot and dispatcher
dp = Dispatcher()
tgbot = Bot(token=BOT_TOKEN)


# Send a message with a caption and image URL
async def send_message(caption: str, image_url:str) -> None:
    await tgbot.send_photo(chat_id=CHAT_ID, caption=caption, photo=image_url, parse_mode=ParseMode.HTML)


# Send a special message with workshop item details
async def send_special_msg(MapItem: WME.WorkshopItem, title: str, desired_word: str) -> None:
    try:
        caption = f"<b>{md.escape(title)}</b>\n" \
            f"Name: <code>{md.escape(MapItem.get_title())}</code>\n" \
            f"Author: <a href=\"{md.escape(MapItem.get_creator_url())}\">{md.escape(MapItem.get_creator_name())}</a>\n" \
            f"<a href=\"{md.escape(MapItem.map_link)}\">Map link</a>\n" \
            f"Desired Words: \"{md.escape(desired_word)}\""
        image_url = MapItem.get_preview_url()
        await send_message(caption, image_url)
    except Exception as err:
        await send_message(f"Oops! Something went wrong in <code>send_special_msg</code> func. \n[{err}]", None)
        

# Print debug message if debug flag is enabled
def debug_print(msg: str, end="\n") -> None:
    if DEBUG:
        print(msg, end=end, flush=True)
