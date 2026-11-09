from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse #это специальный класс в FastAPI (и Starlette), который нужен для того, чтобы отдавать клиенту файлы с диска.
from fastapi.staticfiles import StaticFiles
from database import init_db, db_add_task, db_delete_task, db_load_tasks, db_change_status
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")


class TaskCreate(BaseModel):
    title: str

@app.get("/", response_class=FileResponse)
async def get_main_page():
    return "templates/index.html"

@app.get("/api/tasks")
async def get_tasks():
    list_tasks = await db_load_tasks()
    return list_tasks

@app.post("/api/tasks")
async def add_tasks(task: TaskCreate):
    await db_add_task(task.title)
    return {"status": "ok", "message": "Задача добавлена"}

@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: int):
    success = await db_delete_task(task_id)
    if success:
        return {"status": "ok", "message": "Задача удалена"}
    else:
        raise HTTPException(status_code=404, detail="Задача не найдена")

@app.patch("/api/tasks/{task_id}")
async def change_status(task_id: int):
    success = await db_change_status(task_id)
    if success:
        return {"status": "ok", "message": "Статус задачи обновлен"}
    else:
        raise HTTPException(status_code=404, detail="Задача не найдена")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)