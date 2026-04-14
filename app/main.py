from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import os

app = FastAPI(title="DevOps Learning API")

# Подключение к БД
def get_db_connection():
    conn = psycopg2.connect(
        dbname="app_db",
        user="app_user",
        password="password",
        host="db",
        port="5432"
    )
    return conn


# Модель данных
class Item(BaseModel):
    name: str


# Проверка API
@app.get("/")
def root():
    return {"status": "ok"}


# Проверка БД
@app.get("/db-check")
def db_check():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        result = cur.fetchone()
        conn.close()
        return {"db_status": "connected", "result": result}
    except Exception as e:
        return {"db_status": "error", "error": str(e)}


# Создание таблицы (временно через endpoint)
@app.get("/init-db")
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        );
    """)

    conn.commit()
    conn.close()

    return {"message": "table created"}


# Добавление item
@app.post("/items")
def add_item(item: Item):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO items (name) VALUES (%s) RETURNING id;",
        (item.name,)
    )
    item_id = cur.fetchone()[0]

    conn.commit()
    conn.close()

    return {"id": item_id, "name": item.name}


# Получение items
@app.get("/items")
def get_items():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, name FROM items;")
    rows = cur.fetchall()

    conn.close()

    return [{"id": r[0], "name": r[1]} for r in rows]
