from models.user import User


class UserRepo:
    """Репозиторий для хранения инфо о пользователях"""

    def __init__(self, db):
        self.db = db

    def create_user(self, email, password_hash):
        """Создание пользователя"""
        user = User(
            email=email,
            password_hash=password_hash
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user
    

    def get_by_email(self, email: str):
        """Поиск пользователя по почте"""
        return self.db.query(User).filter(User.email == email).first()