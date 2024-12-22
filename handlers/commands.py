from aiogram import types, Dispatcher
from config.contex import commands_text

async def send_help(message: types.Message):
    await message.reply(commands_text, parse_mode="Markdown")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(send_help, commands=['commands'])