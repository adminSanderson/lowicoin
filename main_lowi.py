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
async def send_help(message: types.Message):
    # Извлекаем текст команды
    command_text = message.text
    parts = command_text.split()

    if len(parts) < 3:
        await message.reply("❌ Неверный формат команды. Пример: /pay 2 812638482", parse_mode="Markdown")
        return

    # Параметры команды
    coin_amount = int(parts[1])  # Количество токенов
    user_key = int(parts[2])  # ID получателя
    sender_id = message.from_user.id  # ID отправителя

    # Проверяем баланс отправителя
    cursor.execute("SELECT coins FROM Users_coins WHERE user_id = ?", (sender_id,))
    sender_data = cursor.fetchone()

    if sender_data is None:
        await message.reply("❌ У вас нет аккаунта или баланса.")
        return

    sender_balance = sender_data[0]

    if sender_balance < coin_amount:
        await message.reply("❌ Недостаточно токенов для перевода.")
        return

    # Проверяем наличие получателя
    cursor.execute("SELECT coins FROM Users_coins WHERE user_id = ?", (user_key,))
    receiver_data = cursor.fetchone()

    if receiver_data is None:
        await message.reply("❌ Получатель с указанным ID не найден.")
        return

    # Списываем токены у отправителя
    new_sender_balance = sender_balance - coin_amount
    cursor.execute("UPDATE Users_coins SET coins = ? WHERE user_id = ?", (new_sender_balance, sender_id))

    # Добавляем токены получателю
    receiver_balance = receiver_data[0]
    new_receiver_balance = receiver_balance + coin_amount
    cursor.execute("UPDATE Users_coins SET coins = ? WHERE user_id = ?", (new_receiver_balance, user_key))

    # Генерация уникального ID транзакции
    transaction_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    # Лог транзакции (по желанию)
    cursor.execute(
        "INSERT INTO Transactions (transaction_id, sender_id, receiver_id, amount) VALUES (?, ?, ?, ?)",
        (transaction_id, sender_id, user_key, coin_amount)
    )

    # Уведомление об успешной транзакции
    await message.reply(
        f"✅ Успешно переведено {coin_amount} токенов пользователю с ID {user_key}.\n"
        f"💳 Ваш новый баланс: {new_sender_balance} токенов.",
        parse_mode="Markdown"
    )

    # Уведомление получателя (опционально)
    try:
        await bot.send_message(
            user_key,
            f"💸 Вам поступило {coin_amount} токенов от пользователя с ID {sender_id}."
        )
    except:
        await message.reply("⚠️ Не удалось уведомить получателя. Он может быть недоступен.")

@dp.message_handler()
async def echo(message: types.Message):
   await message.answer(message.text)
 
if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)