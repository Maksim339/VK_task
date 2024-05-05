from sqlalchemy import Column, String, DateTime, func, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
import uuid

Base = declarative_base()


class User(Base):
    """
        Модель пользователя.

        Attributes:
            id (UUID): Уникальный идентификатор пользователя.
            login (str): Логин пользователя, используемый для входа.
            password (str): Хешированный пароль пользователя.
            project_id (UUID): Идентификатор проекта, к которому принадлежит пользователь.
            env (str): Окружение, в котором используется пользователь.
            domain (str): Домен, к которому принадлежит пользователь.
            locktime (datetime): Время блокировки пользователя.
    """

    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=func.now())
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    project_id = Column(UUID(as_uuid=True), nullable=False)
    env = Column(String, nullable=False)
    domain = Column(String, nullable=False)
    locktime = Column(DateTime, nullable=True)
    is_locked = Column(Boolean, default=False, nullable=False)
