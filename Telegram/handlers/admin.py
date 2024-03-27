import logging

from aiogram import Router, Bot #, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.utils import markdown as md

from json_controller import UserData, ConfigManager

router = Router()
user_data: UserData = UserData()
config = ConfigManager("config.json") # well.. yeah

def is_admin(msg):
    return msg.chat.id == config.get("admin_id")


@router.message(Command("users"))
async def users_handler(msg: Message, bot: Bot):    
    if not is_admin(msg):
        return
    
    users_info = ""
    for user_id, words in user_data.data.items():
        try:
            user = await bot.get_chat(user_id)
            user_name = user.full_name
        except Exception:
            user_name = "Unknown"
        users_info += f"\n• {md.hcode(user_name)} (id: {user_id}) - total words: {len(words)}"
    
    await msg.answer(md.hbold("A list of all users:") + users_info)
    
    
@router.message(Command("user"))
async def user_handler(msg: Message, command: CommandObject, bot: Bot):
    if not is_admin(msg) or command.args is None:
        return
    
    try:
        user = await bot.get_chat(command.args)
    except Exception:
        return await msg.answer("Unknown user!")
    
    user_words = user_data.setdefault(str(user.id), [])
    await msg.answer(md.hbold("Info about ") + md.hcode(user.full_name) + ":\n" +
                     f"• Id: {user.id}\n" + 
                     f"• Custom words: {md.hcode(', '.join(user_words))}\n" +
                     f"• Total words: {len(user_words)}")