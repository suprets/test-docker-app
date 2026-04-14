from fastapi import FastAPI
from pydantic import BaseModel

# Создаем экземпляр приложения
app = FastAPI()

# Временное хранилище (в памяти)
items = []

# Модель данных (схема запроса)
class Item(BaseModel):
    name: str


# Проверка сервиса (healthcheck)
@app.get("/")
def root():
    return {"status": "ok"}


# Получить список элементов
@app.get("/items")
def get_items():
    return items


# Добавить элемент
@app.post("/items")
def add_item(item: Item):
    items.append(item.dict())
    return {
        "message": "item added",
        "item": item
    }
