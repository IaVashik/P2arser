from aiogram import Dispatcher

from .handlers import commands

async def init(bot):  
    dp = Dispatcher()
    dp.include_router(commands.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)