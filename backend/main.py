from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import sqlite3
import time

# Single source‑of‑truth database path
DB_PATH = Path(__file__).parents[1] / "wishlist.db"

# Utility to get a connection
def get_conn():
    return sqlite3.connect(DB_PATH)

app = FastAPI()

# Enable CORS for local/dev testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WishlistItem(BaseModel):
    title: str
    url: str
    price: float = 0.0
    image_url: str = ""

# Create table if it doesn’t exist
def init_db():
    conn = get_conn()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url TEXT,
            price REAL,
            image_url TEXT,
            created_at REAL
        )
        """
    )
    conn.commit()
    conn.close()

init_db()

@app.get("/")
async def read_root():
    return {"message": "Hello from the Universal Wishlist API!"}

@app.post("/api/wishlist")
async def add_item(item: WishlistItem):
    conn = get_conn()
    conn.execute(
        "INSERT INTO items (title, url, price, image_url, created_at) VALUES (?, ?, ?, ?, ?)",
        (item.title, item.url, item.price, item.image_url, time.time())
    )
    conn.commit()
    conn.close()
    return {"status": "success", "item": item.dict()}

@app.get("/api/wishlist")
async def get_items():
    conn = get_conn()
    rows = conn.execute(
        "SELECT id, title, url, price, image_url, created_at FROM items"
    ).fetchall()
    conn.close()

    items = [
        {"id": r[0], "title": r[1], "url": r[2], "price": r[3], "image_url": r[4], "created_at": r[5]}
        for r in rows
    ]
    return {"items": items}
