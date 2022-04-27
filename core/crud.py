from sqlalchemy.orm import Session

from . import models, schemas
from datetime import datetime


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


# create a user with username, password, role
def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    db_user = models.User(username=user.username, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_taxpayers(db: Session):
    return db.query(models.User).filter(models.User.role == "TAXPAYER").all()


# create tax object for taxpayer
def create_tax(db: Session, tax: schemas.TaxCreate, username_id: int, accountant_id: int):
    tax.tax_due_date = datetime.strptime(tax.tax_due_date,'%d-%m-%Y')
    db_tax = models.Tax(**tax.dict(), tax_percent=0.2, username_id=username_id, accountant_id=accountant_id, tax_paid=0, tax_paid_status=False, tax_paid_date="", tax_amount=0.2*tax.user_income)
    db.add(db_tax)
    db.commit()
    db.refresh(db_tax)
    return db_tax

# check if user_id matches tax obj
def check_taxpayer(db: Session, username_id: int, tax_id: int):
    qs = db.query(models.Tax).filter(models.Tax.id == tax_id).all()
    # check exists
    if qs: 
        # check if user_id matches tax obj
        return qs[0].username_id == username_id
    else:
        return False

# check if tax status is paid
def check_tax_paid(db: Session, tax_id: int):
    qs = db.query(models.Tax).filter(models.Tax.id == tax_id).all()
    return qs[0].tax_paid_status
    

# update the tax object when tax paid
def pay_tax(db: Session, tax: schemas.TaxPayCreate, tax_id: int):
    print(f"tax_id: {tax_id}")
    # update existing tax object
    db_tax = db.query(models.Tax).filter(models.Tax.id == tax_id).first()
    db_tax.tax_paid += tax.tax_paid
    if db_tax.tax_paid >= db_tax.tax_amount:
        db_tax.tax_paid_status = True
        db_tax.tax_status = 'PAID'
        db_tax.paid_date = datetime.now()
    # create TaxPay object
    db_tax_pay = models.TaxPay(tax_obj_id=tax_id, tax_paid=tax.tax_paid, tax_paid_date=datetime.now())
    db.add(db_tax_pay)
    db.commit()
    db.refresh(db_tax_pay)
    return db_tax

# check taxpayer exists
def check_user_exists(db: Session, user_id: int):
    qs = db.query(models.User).filter(models.User.id == user_id).all()
    return True if qs else False