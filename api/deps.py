from fastapi import Header, HTTPException
from utils.security import decode_token


def get_curr_user_strict(authorization: str = Header(None)):
    """Получение текущего пользователя (строгий метод, с ним только по авторизации)
    Исходно хотел использовать этот класс, но сейчас не используется.
    Оставил как опциональный
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Auth required")

    token = authorization.split(" ")[1]

    try:
        user_id = decode_token(token)
        return user_id
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
    

def get_curr_user(authorization: str = Header(None)):
    """Опциональное получение текущего пользователя"""
    if not authorization:
        return None

    try:
        token = authorization.split(" ")[1]
        return decode_token(token)
    except:
        return None