from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.user_service import get_user, create_user, update_user, delete_user, acquire_lock, release_lock, get_all_users
from app.db.schemas import UserCreate, UserOut, UserUpdate
from uuid import UUID

router = APIRouter()


@router.post("/", response_model=UserOut)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    """
        Создает нового пользователя в базе данных.

        Args:
            user (UserCreate): Данные нового пользователя.
            db (Session, optional): Сессия базы данных.

        Returns:
            UserOut: Данные созданного пользователя.
    """
    return create_user(user, db)


@router.get("/")
def read_users_endpoint(db: Session = Depends(get_db)):
    users = get_all_users(db)
    return users


@router.get("/{user_id}", response_model=UserOut)
def read_user_endpoint(user_id: UUID, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserOut)
def update_user_endpoint(user_id: UUID, user: UserUpdate, db: Session = Depends(get_db)):
    return update_user(db, user_id, user)


@router.delete("/{user_id}")
def delete_user_endpoint(user_id: UUID, db: Session = Depends(get_db)):
    delete_user(db, user_id)
    return {"status": "success"}


@router.post("/{user_id}/lock", response_model=UserOut)
def acquire_lock_endpoint(user_id: UUID, db: Session = Depends(get_db)):
    return acquire_lock(db, user_id)


@router.post("/{user_id}/unlock", response_model=UserOut)
def release_lock_endpoint(user_id: UUID, db: Session = Depends(get_db)):
    return release_lock(db, user_id)
