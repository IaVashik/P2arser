from aiogram import Router #, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.utils import markdown as md
from settings import UserData

router = Router()
user_data: UserData = UserData()

# TODO update this shit
def parsing_args(raw_args):
    args = raw_args.args.split(" ")
    return list(map(lambda val: val.replace("_", " ").lower(), args))


@router.message(Command("start"))
async def start_handler(msg: Message):
    user_data.info[str(msg.from_user.id)] = []
    user_data.save_change()
    await msg.answer(f"Welcome, {md.hbold(msg.from_user.full_name)}")


@router.message(Command("list"))
async def get_desire_handler(msg: Message):
    user_words = user_data.info[str(msg.from_user.id)]
    await msg.answer(md.hbold("Your words: ") + "\n• " + '\n• '.join(user_words))
    

@router.message(Command("add"))
async def add_desire_handler(msg: Message, command: CommandObject):
    if command.args is None:
        return await msg.answer("Error! Need to provide an argument" + md.hitalic("(/add <desired_word>, <desired_word>, ...)"))
    
    desired_words = parsing_args(command)
    user_data.info[str(msg.from_user.id)].extend(desired_words) #! there could be duplicates
    user_data.save_change()
    
    await msg.answer(md.hbold("Added the following words: ") + "\n• " + '\n• '.join(desired_words))
    
    
@router.message(Command("remove"))
async def remove_desire_handler(msg: Message, command: CommandObject):
    if command.args is None:
        return await msg.answer("Error! Need to provide an argument (/remove <desired_word>, <desired_word>, ...)")
    
    desired_words = parsing_args(command)
    await msg.answer(f"Result: TODO {desired_words}")
