from sqlalchemy.orm import Session
from app.db.models import User
from app.db.schemas import UserCreate, UserUpdate
from fastapi import HTTPException
from uuid import UUID


def get_user_by_email(db: Session, email: str):
    """
        Получение пользователя по email.

        Args:
        db (Session): Сессия базы данных.
        email (str): Электронная почта пользователя для поиска.

        Returns:
        User: Экземпляр пользователя или None, если пользователь не найден.
    """
    return db.query(User).filter(User.login == email).first()


def get_user(db: Session, user_id: UUID):
    """
        Получение пользователя по ID.

        Args:
        db (Session): Сессия базы данных.
        user_id (UUID): Уникальный идентификатор пользователя.

        Returns:
        User: Экземпляр пользователя или None, если пользователь не найден.
    """
    return db.query(User).filter(User.id == user_id).first()


def get_all_users(db: Session):
    """
        Получение списка всех пользователей из базы данных.

        Args:
        db (Session): Сессия базы данных.

        Returns:
        List[User]: Список всех пользователей в базе данных.
    """
    return db.query(User).all()


def create_user(user_data: UserCreate, db: Session):
    """
        Создает нового пользователя в базе данных.

        Args:
            db (Session): Сессия базы данных для выполнения операций.
            user_data (UserCreate): Объект с данными пользователя для создания.

        Returns:
            UserOut: Данные созданного пользователя.

        Raises:
            HTTPException: Если пользователь с таким email уже существует.
    """
    db_user = get_user_by_email(db, email=user_data.login)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(
        login=user_data.login,
        password=user_data.password,
        project_id=user_data.project_id,
        env=user_data.env,
        domain=user_data.domain
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def update_user(db: Session, user_id: UUID, user_data: UserUpdate):
    """
        Обновление данных пользователя.

        Args:
        db (Session): Сессия базы данных.
        user_id (UUID): Уникальный идентификатор пользователя.
        user_data (UserUpdate): Данные для обновления пользователя.

        Returns:
        UserOut: Обновленные данные пользователя.
    """
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user_data.dict(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: UUID):
    """
        Удаление пользователя по ID.

        Args:
        db (Session): Сессия базы данных.
        user_id (UUID): Уникальный идентификатор пользователя.

        Returns:
        None
    """
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()


def acquire_lock(db: Session, user_id: UUID):
    """
        Блокировка пользователя.

        Args:
        db (Session): Сессия базы данных.
        user_id (UUID): Уникальный идентификатор пользователя.

        Returns:
        User: Экземпляр заблокированного пользователя.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.is_locked:
        raise HTTPException(status_code=400, detail="User already locked")
    user.is_locked = True
    db.commit()
    return user


def release_lock(db: Session, user_id: UUID):
    """
        Разблокировка пользователя.

        Args:
        db (Session): Сессия базы данных.
        user_id (UUID): Уникальный идентификатор пользователя.

        Returns:
        User: Экземпляр разблокированного пользователя.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_locked:
        raise HTTPException(status_code=400, detail="User is not locked")
    user.is_locked = False
    db.commit()
    return user
