import sqlite3
from fastapi import FastAPI, HTTPException

app = FastAPI(title="My Goal Tracker API")

# Функция для подключения к базе данных
def get_db():
    conn = sqlite3.connect("goals.db")
    conn.row_factory = sqlite3.Row  # Чтобы получать данные в виде удобных словарей
    return conn

# Создаем таблицу в базе при первом запуске сервера
with get_db() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    """)

# 1. READ — Получить все цели из базы
@app.get("/goals")
def get_goals():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM goals").fetchall()
        return [{"id": r["id"], "title": r["title"], "done": bool(r["done"])} for r in rows]

# 2. CREATE — Добавить новую цель в базу
@app.post("/goals")
def add_goal(title: str):
    with get_db() as conn:
        cursor = conn.execute("INSERT INTO goals (title, done) VALUES (?, ?)", (title, False))
        new_id = cursor.lastrowid
        return {"id": new_id, "title": title, "done": False}

# 3. UPDATE — Отметить цель выполненной (или вернуть в работу)
@app.put("/goals/{goal_id}")
def update_goal(goal_id: int, done: bool = True):
    with get_db() as conn:
        cursor = conn.execute("UPDATE goals SET done = ? WHERE id = ?", (done, goal_id))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Цель с таким ID не найдена")
        return {"id": goal_id, "done": done, "message": "Статус обновлен!"}

# 4. DELETE — Удалить цель навсегда
@app.delete("/goals/{goal_id}")
def delete_goal(goal_id: int):
    with get_db() as conn:
        cursor = conn.execute("DELETE FROM goals WHERE id = ?", (goal_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Цель с таким ID не найдена")
        return {"message": f"Цель #{goal_id} успешно удалена"}