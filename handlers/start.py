from aiogram import types, Router, Dispatcher
from database.database import add_user, check_user
from utils.random_16 import random_string
from aiogram.filters import Command

router = Router()

@router.message(Command(commands=['start']))
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    if not check_user(user_id):
        add_user(user_id, random_string(), 2)
        await message.answer(
            f'Hello, *{full_name}*!\nNice to meet you.\nYour profile has been *created* and we have replenished your balance with 2 lowi coins!\nTap /commands to start or /help to _... help message?_!',
            parse_mode="Markdown"
        )
    else:
        await message.answer(
            f'Welcome back, *{full_name}*!\nYour profile already exists. Tap /commands to start or /help to _... help message?_!',
            parse_mode="Markdown"
        )

def register_handlers(dp: Dispatcher):
    dp.include_router(router)