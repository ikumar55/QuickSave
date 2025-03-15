# backend/main.py

from fastapi import FastAPI, Request
from pydantic import BaseModel
import sqlite3
import time
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
# Enable CORS for all origins (for testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can later restrict this to your extension's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1) Let's define a Pydantic model for incoming wishlist items
class WishlistItem(BaseModel):
    title: str
    url: str
    price: float = 0.0
    image_url: str = ""

# 2) Initialize DB (simple version – we’ll keep it in the same file for now)
def init_db():
    conn = sqlite3.connect("wishlist.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url TEXT,
            price REAL,
            image_url TEXT,
            created_at REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()  # Ensure the table is created when the app starts

@app.get("/")
def read_root():
    return {"message": "Hello from the Universal Wishlist API!"}

@app.post("/api/wishlist")
def add_item(item: WishlistItem):
    """Receive a wishlist item and store it in SQLite."""
    conn = sqlite3.connect("wishlist.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO items (title, url, price, image_url, created_at) VALUES (?, ?, ?, ?, ?)",
        (item.title, item.url, item.price, item.image_url, time.time())
    )
    conn.commit()
    conn.close()
    return {"status": "success", "item_received": item.dict()}

@app.get("/api/wishlist")
def get_items():
    """Return all wishlist items."""
    conn = sqlite3.connect("wishlist.db")
    c = conn.cursor()
    c.execute("SELECT id, title, url, price, image_url, created_at FROM items")
    rows = c.fetchall()
    conn.close()

    items = []
    for row in rows:
        items.append({
            "id": row[0],
            "title": row[1],
            "url": row[2],
            "price": row[3],
            "image_url": row[4],
            "created_at": row[5]
        })
    return {"items": items}
