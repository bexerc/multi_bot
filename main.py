import asyncio
import logging

from aiogram import Bot, Dispatcher
from os import getenv
from dotenv import load_dotenv
from app.handlers import router
from aiogram.types import BotCommandScopeDefault
from comands.comand_List import List

bot = Bot(token=getenv('TOKEN'))
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await bot.set_my_commands(commands= List, scope = BotCommandScopeDefault())
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('exit')
        