from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.client.session.aiohttp import AiohttpSession
from config.config import API_TOKEN
from handlers import start, commands, profile, payment, default
import asyncio

async def main():
    session = AiohttpSession()
    bot = Bot(token=API_TOKEN, session=session)
    dp = Dispatcher()

    start.register_handlers(dp)
    commands.register_handlers(dp)
    profile.register_handlers(dp)
    payment.register_handlers(dp)
    default.register_handlers(dp)

    await bot.set_my_commands([
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="commands", description="Available commands"),
        BotCommand(command="me", description="Show profile"),
        BotCommand(command="pay", description="Make a payment"),
        BotCommand(command="profile", description="Show profile"),
    ])

    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())
