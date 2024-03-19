import logging

from aiogram import Router #, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.utils import markdown as md

from settings import UserData

router = Router()
user_data: UserData = UserData()

HOW_TO_USE = f"""{md.hbold('How to Use:')}
1. Add keywords to the bot using the /add (keyword) command.
2. The bot will continuously monitor the Steam Workshop for updates.
3. When a map containing your keywords is found, you'll receive a notification via Telegram."""

HELP_TEXT = f"""/help - Displays information about the bot and its available commands.
/add - Adds a keyword to the user's list of keywords. The bot will then search for items in the Steam Workshop that match these keywords.
/remove - Removes a keyword from the user's list of keywords.
/list - Displays all the keywords that the user has added.
/about - Displays information about the bot's developers and contact information.
/feedback - Sends feedback to the bot's developers.

{HOW_TO_USE}"""


ABOUT_BOT = f"""{md.hbold('P2ARCER')} (pArser + Portal 2 = P2Arser) is a Telegram bot that helps Portal 2 players discover new and updated maps in the Steam Workshop based on keywords. This can be useful if you want to know immediately about the usage of your assets, hehe.

{HOW_TO_USE}

{md.hbold('Additional Information::')}
• Created by {md.hbold('laVashik')} ({md.hlink('GitHub', 'https://github.com/IaVashik')}, {md.hlink('YouTube', 'https://www.youtube.com/@laVashikProductions')})
• View the source code and learn more about installation on the project's {md.hlink('GitHub repository', 'https://github.com/IaVashik/P2arser')}.

From a modder for modders!
"""


def parsing_args(raw_args):
    args = raw_args.args.split(" ")
    return list(map(lambda val: val.replace("_", " ").lower(), args))

def logging_info(msg, command_text):
    logging.info(f"User {msg.from_user.full_name} (id: {msg.from_user.id}) called {command_text}")


@router.message(Command("start"))
async def start_handler(msg: Message):
    user_data.info[str(msg.from_user.id)] = []
    user_data.save_change()
    await msg.answer(f"Welcome, {md.hbold(msg.from_user.full_name)}")
    logging_info(msg, "/start")


@router.message(Command("list"))
async def get_desire_handler(msg: Message):
    user_words = user_data.info[str(msg.from_user.id)]
    await msg.answer(md.hbold("Your words: ") + "\n• " + '\n• '.join(user_words))
    logging_info(msg, "/list")
    

@router.message(Command("add"))
async def add_desire_handler(msg: Message, command: CommandObject):
    if command.args is None:
        return await msg.answer("Error! Need to provide an argument" + md.hpre("/add {desired_word}, {desired_word}, ..."))
    
    desired_words = parsing_args(command)
    id = str(msg.from_user.id)
    
    # todo
    if id in user_data.info:
        user_data.info[id].extend(desired_words) #! there could be duplicates
        user_data.save_change()
    else:
        logging.error("No user info? Huh?")
    
    await msg.answer(md.hbold("Added the following words: ") + "\n• " + '\n• '.join(desired_words))
    logging_info(msg, f"/add {desired_words}")
    
    
@router.message(Command("remove"))
async def remove_desire_handler(msg: Message, command: CommandObject):
    if command.args is None:
        return await msg.answer("Error! Need to provide an argument" + md.hpre("/remove {desired_word}, {desired_word}, ..."))
    
    desired_words = parsing_args(command)
    user_words = user_data.info[str(msg.from_user.id)]
    
    deleted_words = []
    for word in desired_words:
        if word in user_words:
            user_words.remove(word)
            deleted_words.append(word)
    user_data.save_change()
        
    await msg.answer(md.hbold("Removed the following words: ") + "\n• " + '\n• '.join(deleted_words))
    logging_info(msg, f"/remove {desired_words}")


@router.message(Command("clear"))
async def clear_handler(msg: Message):
    user_data.info[str(msg.from_user.id)].clear()
    user_data.save_change()
    
    await msg.answer("Done!")
    logging_info(msg, "/clear")
    
    
@router.message(Command("help"))
async def help_handler(msg: Message):
    await msg.answer(HELP_TEXT)
    logging_info(msg, "/help")
    
    
    
@router.message(Command("about"))
async def about_handler(msg: Message):
    await msg.answer(ABOUT_BOT)
    logging_info(msg, "/about")
    
    
@router.message(Command("feedback"))
async def feedback_handler(msg: Message, command: CommandObject):
    if command.args is None:
        return await msg.answer("Error! Need to provide an argument" + md.hpre("/feedback {your text}"))

    # send_msg = await .send_photo(chat_id=chat_id, caption=text, photo=thumbnail_url)
    # await msg.answer(f"Your feedback has been forwarded to the administrator of this bot, {}")
    await msg.answer("Sorry, but it's TODO func")
    logging_info(msg, f"/feedback {command.args}")
