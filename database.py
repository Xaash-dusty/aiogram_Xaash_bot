import aiosqlite

DB_NAME = "users.db"

# 1. Функция создания таблицы (запускается один раз при старте бота)
async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                reg_date TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.commit()

# 2. Функция добавления пользователя в базу
async def add_user(user_id: int, username: str):
    async with aiosqlite.connect(DB_NAME) as db:
        # INSERT OR IGNORE значит: если пользователь уже есть в базе, мы его не перезаписываем
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)",
            (user_id, username)
        )
        await db.commit()

# 3. Функция подсчета общего числа пользователей
async def get_users_count():
    async with aiosqlite.connect(DB_NAME) as db:
        # SELECT COUNT(*) вычисляет количество строк в таблице
        async with db.execute("SELECT COUNT(*) FROM users") as cursor:
            row = await cursor.fetchone()
            return row[0] # Возвращаем само число пользователей

# 4. Функция получения списка всех пользователей
async def get_all_users():
    async with aiosqlite.connect(DB_NAME) as db:
        # Извлекаем ID и никнейм всех строк
        async with db.execute("SELECT user_id, username FROM users") as cursor:
            rows = await cursor.fetchall()  # fetchall() забирает ВСЕ строки сразу
            return rows
