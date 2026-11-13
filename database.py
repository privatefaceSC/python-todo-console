import aiosqlite
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError




# Создаем объект для хеширования (использует безопасные настройки по умолчанию)
ph = PasswordHasher()

DB_PATH = "database.db"


async def init_db():
    async with aiosqlite.connect("database.db") as db:
        # Здесь db — это ваше соединение
        await db.execute("""
            CREATE TABLE IF NOT EXISTS tasks_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tasks TEXT NOT NULL,
                status INTEGER DEFAULT 0,
                user_id INTEGER NOT NULL REFERENCES users(id)
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

async def db_register_user(email, password):
    password_hash = ph.hash(password)
    async with aiosqlite.connect("database.db") as db:
        try:
            await db.execute(
                "INSERT INTO users (email, password_hash) VALUES (?, ?)",
                (email, password_hash)
            )
            await db.commit()
            async with db.execute("SELECT id FROM users WHERE email = ?",
                                  (email,)) as cursor:
                row = await cursor.fetchone()
                if row is None:
                    return None
                user_id = row[0]

                return user_id
        except aiosqlite.IntegrityError:
            return None

async def db_login_user(email, password):
    async with aiosqlite.connect("database.db") as db:
        async with db.execute("SELECT id, password_hash FROM users WHERE email = ?",
                                  (email,)) as cursor:
            row = await cursor.fetchone()
            if row is None:
                return None

            user_id = row[0]
            stored_hash = row[1]
            try:
                ph.verify(stored_hash, password)
                return user_id
            except VerifyMismatchError:
                return None

async def db_load_tasks(user_id: int):
    async with aiosqlite.connect("database.db") as db:
        async with db.execute("SELECT id, tasks, status FROM tasks_table WHERE user_id = ?", (user_id,)) as cursor:#возвращает курсор, что бы читать результат запроса
            rows = await cursor.fetchall()
            tasks = []
            for row in rows:
                tasks.append({
                    "id": row[0],
                    "title": row[1],
                    "status": bool(row[2])
                })
            return tasks

async def db_add_task(name_task, user_id: int, status=0):
    async with aiosqlite.connect("database.db") as db:
        await db.execute(
            "INSERT INTO tasks_table (tasks, status, user_id) VALUES (?, ?, ?)",
            (name_task, status, user_id)
        )
        await db.commit()
        return True



async def db_delete_task(task_id, user_id: int):
    async with aiosqlite.connect("database.db") as db:
        async with db.execute("DELETE FROM tasks_table WHERE id = ? AND user_id = ?", (task_id, user_id)) as cursor:
                await db.commit()
                if cursor.rowcount > 0:
                    return True
                else:
                    return False

async def db_change_status(task_id, user_id: int):
    async with aiosqlite.connect("database.db") as db:
        async with db.execute(
                    "UPDATE tasks_table SET status = CASE WHEN status = 1 THEN 0 ELSE 1"
                    " END WHERE id = ? AND user_id = ?", (task_id, user_id)) as cursor:
            await db.commit()
            if cursor.rowcount > 0:# количество строк, которые были затронуты
                return True
            else:
                return False
