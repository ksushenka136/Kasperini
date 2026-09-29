from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Создаем специальный ответ, который умеет передавать русский язык
class UnicodeJSONResponse(JSONResponse):
    media_type = "application/json; charset=utf-8"

app = FastAPI(default_response_class=UnicodeJSONResponse)

@app.get("/")
def home():
    return {"status": "OK", "message": "Проект Kasperini успешно запущен!"}