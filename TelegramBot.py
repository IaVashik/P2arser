from aiogram import Dispatcher, Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.utils import markdown as md

dp = Dispatcher()
router = Router()
userbase = None

def parsing_args(raw_args):
    args = raw_args.args.split(" ")
    return list(map(lambda val: val.replace("_", " ").lower(), args))


@router.message(Command("start"))
async def start_handler(msg: Message):
    userbase.add(msg.from_user.id, [])
    await msg.answer(f"Welcome, {md.hbold(msg.from_user.full_name)}")


@router.message(Command("list"))
async def get_desire_handler(msg: Message):
    user_words = userbase.get(msg.from_user.id)
    await msg.answer(md.hbold("Your words: ") + "\n• " + '\n• '.join(user_words))
    

@router.message(Command("add"))
async def add_desire_handler(msg: Message, command: CommandObject):
    if command.args is None:
        return await msg.answer("Error! Need to provide an argument" + md.hitalic("(/add <desired_word>, <desired_word>, ...)"))
    
    desired_words = parsing_args(command)
    userbase.get(msg.from_user.id).extend(desired_words) #! there could be duplicates
    userbase.update()
    
    await msg.answer(md.hbold("Added the following words: ") + "\n• " + '\n• '.join(desired_words))
    
    
@router.message(Command("remove"))
async def remove_desire_handler(msg: Message, command: CommandObject):
    if command.args is None:
        return await msg.answer("Error! Need to provide an argument (/remove <desired_word>, <desired_word>, ...)")
    
    desired_words = parsing_args(command)
    await msg.answer(f"Result: TODO {desired_words}")



async def init_bot(bot, db):  
    global userbase  # junk code meh
    userbase = db.load_table("users")
    
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)