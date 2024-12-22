import sqlite3

connection = sqlite3.connect('coins_db.db')
cursor = connection.cursor()

def connect():
    return sqlite3.connect('coins_db.db')

def check_user(user_id):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute('SELECT id_users FROM Users_coins WHERE id_users = ?', (user_id,))
    result = cursor.fetchone()
    connection.close()
    return result is not None

def add_user(user_id, id_pay, coins):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Users_coins (id_users, id_pay, coins) VALUES (?, ?, ?)', (user_id, id_pay, coins))
    connection.commit()
    connection.close()

def get_user_balance(user_id):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute('SELECT coins FROM Users_coins WHERE id_users = ?', (user_id,))
    balance = cursor.fetchone()
    connection.close()
    return balance[0] if balance else 0

def get_user_idpay(user_id):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute('SELECT id_pay FROM Users_coins WHERE id_users = ?', (user_id,))
    idpay = cursor.fetchone()
    connection.close()
    return idpay[0] if idpay else None

def transfer_coins(sender_id, receiver_idpay, coin_amount):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute('SELECT coins FROM Users_coins WHERE id_users = ?', (sender_id,))
    sender_balance = cursor.fetchone()

    if sender_balance is None or sender_balance[0] < coin_amount:
        connection.close()
        return False, None

    cursor.execute('SELECT coins FROM Users_coins WHERE id_pay = ?', (receiver_idpay,))
    receiver_balance = cursor.fetchone()

    if not receiver_balance:
        connection.close()
        return False, None

    new_sender_balance = sender_balance[0] - coin_amount
    new_receiver_balance = receiver_balance[0] + coin_amount

    cursor.execute('UPDATE Users_coins SET coins = ? WHERE id_users = ?', (new_sender_balance, sender_id))
    cursor.execute('UPDATE Users_coins SET coins = ? WHERE id_pay = ?', (new_receiver_balance, receiver_idpay))
    connection.commit()
    connection.close()

    return True, new_sender_balance