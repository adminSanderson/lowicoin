from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from config.config import API_TOKEN
from handlers import start, commands, profile, payment, default

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

start.register_handlers(dp)
commands.register_handlers(dp)
profile.register_handlers(dp)
payment.register_handlers(dp)
default.register_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)