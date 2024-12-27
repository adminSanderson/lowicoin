from aiogram import types, Router, Dispatcher
from aiogram.filters import Command
from database.database import cursor, connection

router = Router()

@router.message(Command(commands=['pay']))
async def handle_pay(message: types.Message):
    parts = message.text.split()
    
    if len(parts) < 3:
        await message.answer("❌ Incorrect command format. Example: /pay 2.5 (coins) jnRHDtjlCfhNfc5b (Pay id)")
        return

    try:
        coin_amount = float(parts[1])
        user_key = parts[2]
    except ValueError:
        await message.answer("❌ Specify the correct number for coin.")
        return

    if coin_amount < 0.01:
        await message.answer("❌ Minimum transfer amount: 0.01 coin.")
        return

    sender_id = message.from_user.id

    cursor.execute("SELECT coins FROM Users_coins WHERE id_users = ?", (sender_id,))
    sender_data = cursor.fetchone()

    if sender_data is None or sender_data[0] < coin_amount:
        await message.answer("❌ There are not enough coins to transfer.")
        return

    new_sender_balance = sender_data[0] - coin_amount
    cursor.execute("UPDATE Users_coins SET coins = ? WHERE id_users = ?", (round(new_sender_balance, 2), sender_id))

    cursor.execute("SELECT coins FROM Users_coins WHERE id_pay = ?", (user_key,))
    receiver_data = cursor.fetchone()

    if receiver_data:
        new_receiver_balance = receiver_data[0] + coin_amount
        cursor.execute("UPDATE Users_coins SET coins = ? WHERE id_pay = ?", (round(new_receiver_balance, 2), user_key))
    else:
        await message.answer("❌ User with this Pay ID does not exist.")
        connection.commit()
        return

    connection.commit()

    await message.answer(
        f"✅ Successfully transferred {coin_amount} tokens to the user with the ID PAY {user_key}.\n"
        f"💳 Your new balance: {round(new_sender_balance, 2)} coins."
    )

def register_handlers(dp: Dispatcher):
    dp.include_router(router)
