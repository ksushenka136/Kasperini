from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


# 1. Таблица пользователей
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="student")  # 'student' или 'admin'
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связь: у одного пользователя может быть много словарей
    dictionaries = relationship("Dictionary", back_populates="owner")


# 2. Таблица словарей
class Dictionary(Base):
    __tablename__ = "dictionaries"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="dictionaries")
    # Связь: при удалении словаря удаляются и все его карточки
    cards = relationship(
        "Card", back_populates="dictionary", cascade="all, delete-orphan"
    )


# 3. Таблица карточек (слов)
class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, nullable=False)
    translation = Column(String, nullable=False)
    dictionary_id = Column(Integer, ForeignKey("dictionaries.id"))

    dictionary = relationship("Dictionary", back_populates="cards")
    # Связь 1-к-1 с прогрессом изученности
    progress = relationship(
        "Progress",
        back_populates="card",
        uselist=False,
        cascade="all, delete-orphan",
    )


# 4. Таблица прогресса интервального повторения (SRS)
class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, ForeignKey("cards.id"), unique=True)
    interval = Column(Integer, default=1)  # Интервал в днях
    repetition_count = Column(Integer, default=0)  # Кол-во успешных повторений
    next_review = Column(DateTime, default=datetime.utcnow)  # Дата следующего показа

    card = relationship("Card", back_populates="progress")


# 5. Таблица журнала тренировок (история ответов)
class TrainingLog(Base):
    __tablename__ = "training_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    card_id = Column(Integer, ForeignKey("cards.id"))
    user_answer = Column(String)
    is_correct = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow)