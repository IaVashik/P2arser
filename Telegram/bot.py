from aiogram import Dispatcher

from .handlers import commands
from .handlers import admin

async def init(bot):  
    dp = Dispatcher()
    dp.include_routers(commands.router, admin.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    raise KeyboardInterrupt