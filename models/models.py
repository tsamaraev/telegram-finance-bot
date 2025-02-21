from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean, Enum, create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, unique=True, nullable=False)
    username = Column(String, nullable=True)
    currency = Column(String, nullable=False)
    reminder_time = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    type = Column(Enum('income', 'expense', name='transaction_type'), nullable=False)
    category = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=True)
    name = Column(String, nullable=False)
    type = Column(Enum('income', 'expense', name='category_type'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class AssetLiability(Base):
    __tablename__ = 'assets_liabilities'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    type = Column(Enum('asset', 'liability', name='asset_liability_type'), nullable=False)
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    date_added = Column(DateTime, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Reminder(Base):
    __tablename__ = 'reminders'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    message = Column(String, nullable=False)
    time = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

