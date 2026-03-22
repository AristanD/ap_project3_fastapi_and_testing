from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from db.session import get_db
from repos.user_repo import UserRepo
from utils.security import verify_password, create_access_token, hash_password


router = APIRouter()


# Регистрация пользователя
@router.post("/auth/register")
def register(data: dict, db: Session = Depends(get_db)):

    repo = UserRepo(db)

    user = repo.create_user(
        data["email"],
        hash_password(data["password"])
    )

    return {"user_id": user.id}


# Авторизация
@router.post("/auth/login")
def login(data: dict, db: Session = Depends(get_db)):

    repo = UserRepo(db)
    user = repo.get_by_email(data["email"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(data["password"], user.password_hash):
        raise HTTPException(status_code=401, detail="Wrong password")

    token = create_access_token(user.id)

    return {"access_token": token}