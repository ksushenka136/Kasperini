from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Название файла базы данных, который создастся в корне проекта
SQLALCHEMY_DATABASE_URL = "sqlite:///./kasperini.db"

# Создаём движок подключения к SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False
    },  # Нужно только для работы SQLite в FastAPI
)

# Фабрика сессий для подключения к БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс, от которого будут наследоваться все наши 5 таблиц (модели)
Base = declarative_base()


# Вспомогательная функция (Dependency) для создания сессии на один запрос
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()