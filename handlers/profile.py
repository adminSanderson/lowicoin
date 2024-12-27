from aiogram import types, Router, Dispatcher
from aiogram.filters import Command
from database.database import get_user_balance, get_user_idpay
from datetime import datetime

router = Router()

@router.message(Command(commands=['me', 'profile']))
async def user_profile(message: types.Message):
    now = datetime.now()
    user_id = message.from_user.id

    balance = get_user_balance(user_id)
    idpay = get_user_idpay(user_id)

    profile_text = f'''
    👤 *{message.from_user.full_name}'s* profile

*ID PAY:* `{idpay}`
*Date:* {now.strftime("%Y-%m-%d")}, {now.strftime("%H:%M:%S")}
*Balance:* {balance}
    '''
    await message.answer(profile_text, parse_mode="Markdown")

def register_handlers(dp: Dispatcher):
    dp.include_router(router)
