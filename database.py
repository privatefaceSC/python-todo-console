import aiosqlite

DB_PATH = "database.db"


async def init_db():
    async with aiosqlite.connect("database.db") as db:
        # Здесь db — это ваше соединение
        await db.execute("""
            CREATE TABLE IF NOT EXISTS tasks_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tasks TEXT NOT NULL,
                status INTEGER DEFAULT 0
            )
        """)
        await db.commit()
async def db_load_tasks():
    async with aiosqlite.connect("database.db") as db:
        async with db.execute("SELECT * FROM tasks_table") as cursor:#возвращает курсор, что бы читать результат запроса
            rows = await cursor.fetchall()
            tasks = []
            for row in rows:
                tasks.append({
                    "id": row[0],
                    "title": row[1],
                    "status": bool(row[2])
                })
            return tasks

async def db_add_task(name_task, status=0):
    async with aiosqlite.connect("database.db") as db:
        if name_task.strip():
                await db.execute(
                    "INSERT INTO tasks_table (tasks, status) VALUES (?, ?)",
                    (name_task, status)
                )
                await db.commit()


async def db_delete_task(task_id):
    async with aiosqlite.connect("database.db") as db:
        async with db.execute("DELETE FROM tasks_table WHERE id = ?", (task_id,)) as cursor:
                await db.commit()
                if cursor.rowcount > 0:
                    return True
                else:
                    return False

async def db_change_status(task_id):
    async with aiosqlite.connect("database.db") as db:
        async with db.execute(
                    "UPDATE tasks_table SET status = CASE WHEN status = 1 THEN 0 ELSE 1"
                    " END WHERE id = ?", (task_id,)) as cursor:
            await db.commit()
            if cursor.rowcount > 0:# количество строк, которые были затронуты
                return True
            else:
                return False
