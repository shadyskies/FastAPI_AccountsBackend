from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default='TAXPAYER')

    items = relationship("Item", back_populates="owner")
    taxes = relationship("Tax", back_populates="username")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")


class Tax(Base):
    __tablename__ = 'taxes'

    id = Column(Integer, primary_key=True, index=True)
    username_id = Column(Integer, ForeignKey('users.id'))
    user_income = Column(Float)
    pan_card = Column(String, index=True)
    tax_percent = Column(Integer, index=True)
    tax_paid = Column(Float, index=True)
    tax_amount = Column(Float, index=True)
    tax_paid_date = Column(String, index=True)
    tax_due_date = Column(String, index=True)
    tax_status = Column(String, index=True)
    tax_paid_status = Column(Boolean, index=True)
    accountant_id = Column(Integer, foreign_key='users.id')
    
    username = relationship("User", back_populates="taxes")
    paid_taxes = relationship("TaxPay", back_populates="tax_obj")


'''
Track when a user has paid their tax / useful when rollback needs to be done by accountant
'''
class TaxPay(Base):
    __tablename__ = 'tax_pay'

    id = Column(Integer, primary_key=True, index=True)
    tax_paid_date = Column(String, index=True)
    tax_paid = Column(Float, index=True)
    tax_obj_id = Column(Integer, ForeignKey('taxes.id'))

    tax_obj = relationship("Tax", back_populates="paid_taxes")