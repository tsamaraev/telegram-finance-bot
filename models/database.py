from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base

# Создаем подключение к базе данных и инициализируем таблицы
engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)

# Создаем сессию
Session = sessionmaker(bind=engine)
session = Session()