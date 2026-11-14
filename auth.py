import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv

# Загружаем переменные из .env в окружение
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

def create_access_token(data: dict):
    user_id_copy = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    user_id_copy.update({"exp": expire, "type": "access"})
    return jwt.encode(user_id_copy, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    user_id_copy = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    user_id_copy.update({"exp": expire, "type": "refresh"})
    return jwt.encode(user_id_copy, SECRET_KEY, algorithm=ALGORITHM)

# Проверка токена (для Depends)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user_id(access_token: str = Depends(oauth2_scheme)) -> int:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверный токен",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    return int(user_id)


def refresh_tokens(refresh_token: str) -> dict:
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        new_access = create_access_token(data={"sub": user_id})
        new_refresh = create_refresh_token(data={"sub": user_id})

        return {"access_token": new_access, "refresh_token": new_refresh}
    except jwt.PyJWTError:
        raise ValueError("Токен просрочен или неверен")
