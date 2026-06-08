from sqlalchemy import Column, Integer, String, DateTime, Index, Boolean
from backend.database import Base
import datetime

class Candidate(Base):
    __tablename__ = "candidates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, default="")
    votes = Column(Integer, default=0)

class Vote(Base):
    """Модель таблицы голосов"""
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)      # ID пользователя
    candidate_id = Column(Integer, nullable=False)
    user_ip = Column(String, nullable=True)                     # IP для статистики (не для блокировки)
    timestamp = Column(DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc))

    __table_args__ = (
        Index('ix_votes_user', 'user_id'),  # Индекс для быстрой проверки
    )

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)