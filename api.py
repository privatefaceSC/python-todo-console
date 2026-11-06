from core import TaskManager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse #это специальный класс в FastAPI (и Starlette), который нужен для того, чтобы отдавать клиенту файлы с диска.
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
manager = TaskManager()


class TaskCreate(BaseModel):
    title: str
@app.get("/", response_class=FileResponse)
def get_main_page():
    return "templates/index.html"

@app.get("/api/tasks")
def get_tasks():
    list_tasks = [task.to_dict() for task in manager.tasks]
    return list_tasks
@app.post("/api/tasks")
def add_tasks(task: TaskCreate):
    if task.title.strip():
        manager.add_task(task.title)
        return {"status": "ok", "message": "Задача добавлена"}
    else:
        raise HTTPException(status_code=400, detail="Название не может быть пустым")
@app.delete("/tasks/{index}")
def delete_task(index: int):
    if 0 <= index <= len(manager.tasks):
        manager.delete_task(index)
        return {"status": "ok", "message": "Задача удалена"}
    else:
        raise HTTPException(status_code=404, detail="Задача не найдена")
@app.patch("/tasks/{index}")
def select_task(index: int):
    if 0 <= index <= len(manager.tasks):
        manager.select_task(index)
        return {"status": "ok", "message": "Статус задачи обновлен"}
    else:
        raise HTTPException(status_code=404, detail="Задача не найдена")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)