from pydantic import BaseModel, EmailStr, constr, UUID4
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    login: EmailStr
    project_id: UUID4
    env: str
    domain: str


class UserCreate(BaseModel):
    login: EmailStr
    password: constr(min_length=7)
    project_id: UUID4
    env: str
    domain: str


class UserUpdate(BaseModel):
    password: Optional[constr(min_length=7)] = None


class UserOut(UserBase):
    id: UUID4
    created_at: datetime
    is_locked: Optional[bool] = None

    class Config:
        from_attributes = True
