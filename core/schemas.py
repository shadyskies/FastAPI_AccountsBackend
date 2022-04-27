from typing import List, Optional

from pydantic import BaseModel
from enum import Enum


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserRoles(str, Enum):
    TAXPAYER = 'TAXPAYER'
    ACCOUNTANT = 'ACCOUNTANT'
    ADMIN = 'ADMIN'


class UserCreate(UserBase):
    password: str
    role: UserRoles = None


# user roles class


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True
