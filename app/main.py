from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

import app.models
from app.database import Base, engine, get_db


# Исправленный класс ответов с чётким указанием charset=utf-8 для браузеров
class UnicodeJSONResponse(JSONResponse):
    media_type = "application/json; charset=utf-8"


app = FastAPI(
    title="Kasperini API",
    default_response_class=UnicodeJSONResponse,
)

# Автоматическое создание всех таблиц при запуске
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Добро пожаловать в API приложения Kasperini!"}


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": str(e)}