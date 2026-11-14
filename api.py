from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from fastapi.responses import FileResponse #это специальный класс в FastAPI (и Starlette), который нужен для того, чтобы отдавать клиенту файлы с диска.
from fastapi.staticfiles import StaticFiles
from database import init_db, db_add_task, db_delete_task, db_load_tasks, db_change_status, db_register_user, db_login_user
from contextlib import asynccontextmanager
from auth import get_current_user_id, create_access_token, create_refresh_token, refresh_tokens
from fastapi import Depends
from fastapi import Response, Request

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")


class TaskCreate(BaseModel):
    title: str
class RegisterData(BaseModel):
    email: EmailStr
    password: str

@app.get('/', response_class=FileResponse)
async def get_main_page():
    return "templates/index.html"

@app.get("/registration", response_class=FileResponse)
async def open_registration_page():
    return "templates/registration.html"

@app.post("/api/registration")
async def registration(response: Response, data: RegisterData):
    user_id = await db_register_user(data.email, data.password)
    if user_id is None:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")
    refresh_token = create_refresh_token(data={"sub": str(user_id)})
    access_token = create_access_token(data={"sub": str(user_id)})

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,   # Защита от JS
        secure=True,     # Только HTTPS
        samesite="lax",
        max_age=30 * 24 * 60 * 60 # 30 дней
    )
    return {"access_token": access_token,
            "token_type": "bearer"
            }

@app.get("/login", response_class=FileResponse)
async def open_login_page():
    return "templates/login.html"

@app.post("/api/login")
async def login(response: Response, data: RegisterData):
    user_id = await db_login_user(data.email, data.password)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Неверный email или пароль")
    refresh_token = create_refresh_token(data={"sub": str(user_id)})
    access_token = create_access_token(data={"sub": str(user_id)})

    # Отправляем Refresh Token в HttpOnly Cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,  # <-- JavaScript не увидит
        secure=True,    # <-- Только по HTTPS (обязательно для продакшена)
        samesite="lax", # <-- Защита от CSRF
        max_age=30 * 24 * 60 * 60 # 30 дней
    )

    return {"access_token": access_token}

@app.post("/refresh/token/validation")
async def refresh_token_validation(request: Request, response: Response) -> dict:
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Нет Refresh Token")

    try:
        new_tokens = refresh_tokens(refresh_token)

        response.set_cookie(
            key="refresh_token",
            value=new_tokens["refresh_token"],
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=30 * 24 * 60 * 60
        )
        return {"access_token": new_tokens["access_token"], "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))




@app.get("/tasks", response_class=FileResponse)
async def tasks_page():
    return "templates/tasks.html"

@app.get("/load/tasks")
async def load_tasks(user_id: int = Depends(get_current_user_id)):
    list_tasks = await db_load_tasks(user_id)
    return list_tasks

@app.post("/add/tasks")
async def add_tasks(task: TaskCreate, user_id: int = Depends(get_current_user_id)):# <-- FastAPI сам достанет ID из токена
    await db_add_task(task.title, user_id)
    return {"status": "ok", "message": "Задача добавлена"}

@app.delete("/delete/tasks/{task_id}")
async def delete_task(task_id: int, user_id: int = Depends(get_current_user_id)):
    success = await db_delete_task(task_id, user_id)
    if success:
        return {"status": "ok", "message": "Задача удалена"}
    else:
        raise HTTPException(status_code=404, detail="Задача не найдена")

@app.patch("/change/status/tasks/{task_id}")
async def change_status(task_id: int, user_id: int = Depends(get_current_user_id)):
    success = await db_change_status(task_id, user_id)
    if success:
        return {"status": "ok", "message": "Статус задачи обновлен"}
    else:
        raise HTTPException(status_code=404, detail="Задача не найдена")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)