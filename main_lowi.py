import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import API_TOKEN
from contex import *
from datetime import datetime
import sqlite3
import random
from random_16 import random_string
import string

connection = sqlite3.connect('coins_db.db')
cursor = connection.cursor()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
 
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    cursor.execute('SELECT id_users FROM Users_coins WHERE id_users = ?', (user_id,))
    result = cursor.fetchone()

    if result is None:
        cursor.execute('INSERT INTO Users_coins (id_users,id_pay, coins) VALUES (?, ?, ?)', (user_id, random_string(), 2))
        connection.commit()  # Не забываем зафиксировать изменения в базе
        await message.reply(
            f'Hello, *{full_name}*!\nNice to meet you.\nYour profile has been *created* and we have replenished your balance with 2 lowi coins!\nTap /commands to start or /help to _... help message?_!',
            parse_mode="Markdown"
        )
    else:
        # Пользователь уже существует
        await message.reply(
            f'Welcome back, *{full_name}*!\nYour profile already exists. Tap /commands to start or /help to _... help message?_!',
            parse_mode="Markdown"
        )

@dp.message_handler(commands=['commands'])
async def send_help(message: types.Message):
   await message.reply(commands_text, parse_mode="Markdown")

@dp.message_handler(commands=['me', 'profile'])
async def user_profile(message: types.Message):
    now = datetime.now()
    user_id = message.from_user.id

    cursor.execute('SELECT coins FROM Users_coins WHERE id_users = ?', (user_id,))
    balance = cursor.fetchone()
    balance = balance[0]

    profile_text = f'''
    {message.from_user.full_name}'s profile
Date: {now.strftime("%Y-%m-%d")}, {now.strftime("%H:%M:%S")}
Balance: {balance}
    '''
    await message.reply(profile_text)

@dp.message_handler(commands=['pay'])
async def handle_pay(message: types.Message):
    # Извлекаем текст команды
    parts = message.text.split()
    
    if len(parts) < 3:
        await message.reply("❌ Неверный формат команды. Пример: /pay 2.5 jnRHDtjlCfhNfc5b")
        return

    try:
        coin_amount = float(parts[1])  # Количество токенов
        user_key = parts[2]  # ID получателя
    except ValueError:
        await message.reply("❌ Укажите корректное число для токенов.")
        return

    # Проверка на минимальное значение
    if coin_amount < 0.00001:
        await message.reply("❌ Минимальная сумма перевода: 0.00001 токенов.")
        return

    sender_id = message.from_user.id  # ID отправителя

    # Списываем токены у отправителя
    cursor.execute("SELECT coins FROM Users_coins WHERE id_users = ?", (sender_id,))
    sender_data = cursor.fetchone()

    if sender_data is None or sender_data[0] < coin_amount:
        await message.reply("❌ Недостаточно токенов для перевода.")
        return

    new_sender_balance = sender_data[0] - coin_amount
    cursor.execute("UPDATE Users_coins SET coins = ? WHERE id_users = ?", (new_sender_balance, sender_id))

    # Начисляем токены получателю
    cursor.execute("SELECT coins FROM Users_coins WHERE id_pay = ?", (user_key,))
    receiver_data = cursor.fetchone()

    if receiver_data:
        new_receiver_balance = receiver_data[0] + coin_amount
        cursor.execute("UPDATE Users_coins SET coins = ? WHERE id_pay = ?", (new_receiver_balance, user_key))

    connection.commit()

    # Уведомление об успешной транзакции
    await message.reply(
        f"✅ Успешно переведено {coin_amount:.5f} токенов пользователю с ID {user_key}.\n"
        f"💳 Ваш новый баланс: {new_sender_balance:.5f} токенов."
    )


@dp.message_handler()
async def echo(message: types.Message):
   await message.answer(message.text)
 
if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)