from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL для подключения к базе данных SQLite
# Файл voting.db будет создан в корневой папке проекта
SQLALCHEMY_DATABASE_URL = "sqlite:///./voting.db"

# Создаем движок для работы с базой данных
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Необходимо только для SQLite
)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для всех моделей таблиц
Base = declarative_base()
