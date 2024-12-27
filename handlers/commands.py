from aiogram import types, Router, Dispatcher
from aiogram.filters import Command
from config.contex import commands_text

router = Router()

@router.message(Command(commands=['commands']))
async def send_help(message: types.Message):
    await message.answer(commands_text, parse_mode="Markdown")

def register_handlers(dp: Dispatcher):
    dp.include_router(router)
