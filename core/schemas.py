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



class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True

class TaxCreate(BaseModel):
    user_income: float
    pan_card: str
    tax_due_date: str
    tax_status: str

# created by accountant 
class UserTax(TaxCreate):
    id: int
    username_id: int
    tax_percent: float
    tax_amount: float
    tax_paid: float
    tax_paid_date: str
    tax_status: str # NEW, PAID, DELAYED 
    tax_paid_status: bool
    tax_percent: int
    accountant_id: int
    
    class Config:
        orm_mode = True


# pay tax class 
class TaxPayCreate(BaseModel):
    tax_paid_date: str
    tax_paid: float

class TaxPay(TaxPayCreate):
    id: int
    tax_obj_id: int # which tax object is being paid