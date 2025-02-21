from sqlalchemy.orm import Session
from models.models import User, Transaction, Category, AssetLiability, Reminder

# Create operations
def create_user(session: Session, user_id: int, username: str, currency: str, reminder_time: str):
    user = User(user_id=user_id, username=username, currency=currency, reminder_time=reminder_time)
    session.add(user)
    session.commit()
    return user

def create_transaction(session: Session, user_id: int, type: str, category: str, amount: float, date, description: str = None):
    transaction = Transaction(user_id=user_id, type=type, category=category, amount=amount, date=date, description=description)
    session.add(transaction)
    session.commit()
    return transaction

def create_category(session: Session, user_id: int, name: str, type: str):
    category = Category(user_id=user_id, name=name, type=type)
    session.add(category)
    session.commit()
    return category

def create_asset_liability(session: Session, user_id: int, type: str, name: str, amount: float, date_added, description: str = None):
    asset_liability = AssetLiability(user_id=user_id, type=type, name=name, amount=amount, date_added=date_added, description=description)
    session.add(asset_liability)
    session.commit()
    return asset_liability

def create_reminder(session: Session, user_id: int, message: str, time: str, is_active: bool = True):
    reminder = Reminder(user_id=user_id, message=message, time=time, is_active=is_active)
    session.add(reminder)
    session.commit()
    return reminder

# Read operations
def get_user(session: Session, user_id: int):
    return session.query(User).filter(User.user_id == user_id).first()

def get_transaction(session: Session, transaction_id: int):
    return session.query(Transaction).filter(Transaction.id == transaction_id).first()

def get_category(session: Session, category_id: int):
    return session.query(Category).filter(Category.id == category_id).first()

def get_asset_liability(session: Session, asset_liability_id: int):
    return session.query(AssetLiability).filter(AssetLiability.id == asset_liability_id).first()

def get_reminder(session: Session, reminder_id: int):
    return session.query(Reminder).filter(Reminder.id == reminder_id).first()

# Update operations
def update_user(session: Session, user_id: int, **kwargs):
    session.query(User).filter(User.user_id == user_id).update(kwargs)
    session.commit()

def update_transaction(session: Session, transaction_id: int, **kwargs):
    session.query(Transaction).filter(Transaction.id == transaction_id).update(kwargs)
    session.commit()

def update_category(session: Session, category_id: int, **kwargs):
    session.query(Category).filter(Category.id == category_id).update(kwargs)
    session.commit()

def update_asset_liability(session: Session, asset_liability_id: int, **kwargs):
    session.query(AssetLiability).filter(AssetLiability.id == asset_liability_id).update(kwargs)
    session.commit()

def update_reminder(session: Session, reminder_id: int, **kwargs):
    session.query(Reminder).filter(Reminder.id == reminder_id).update(kwargs)
    session.commit()

# Delete operations
def delete_user(session: Session, user_id: int):
    session.query(User).filter(User.user_id == user_id).delete()
    session.commit()

def delete_transaction(session: Session, transaction_id: int):
    session.query(Transaction).filter(Transaction.id == transaction_id).delete()
    session.commit()

def delete_category(session: Session, category_id: int):
    session.query(Category).filter(Category.id == category_id).delete()
    session.commit()

def delete_asset_liability(session: Session, asset_liability_id: int):
    session.query(AssetLiability).filter(AssetLiability.id == asset_liability_id).delete()
    session.commit()

def delete_reminder(session: Session, reminder_id: int):
    session.query(Reminder).filter(Reminder.id == reminder_id).delete()
    session.commit()