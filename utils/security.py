from datetime import datetime, timezone, timedelta
from jose import jwt
import hashlib
from passlib.context import CryptContext
from config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")   # Шифрование пароля (всё ради безы!)
ALGORITHM = "HS256"     # Таким образом, в базе храню не сами пароли, а их хэши (просто и безопасно)


def hash_password(password: str):
    """Хэширование пароля"""
    pwd_hash = hashlib.sha256(password.encode()).hexdigest()   # Тк бкрипт не работает со строками длинее 76 байт, сначала хэширую
    return pwd_context.hash(pwd_hash)


def verify_password(password: str, hashed: str):
    """Верификация пользователя"""
    pwd_hash = hashlib.sha256(password.encode()).hexdigest()
    return pwd_context.verify(pwd_hash, hashed)


def create_access_token(user_id: int):
    """Токен доступа, после надо перелогиниться"""
    expire = datetime.now(timezone.utc) + timedelta(hours=24)
    payload = {
        "user_id": user_id,
        "exp": expire
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=ALGORITHM)


def decode_token(token: str):
    """Декодирование хэша пароля"""
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[ALGORITHM])
    return payload["user_id"]