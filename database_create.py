import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('coins_db.db')
cursor = connection.cursor()

# Создаем таблицу Users
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users_coins (
id INTEGER PRIMARY KEY,
id_users INTEGER,
id_pay INTEGER,
coins REAL
)
''')

# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()