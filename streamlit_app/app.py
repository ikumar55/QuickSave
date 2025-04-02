import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="Shopping Wishlist", layout="wide")

# --- DATABASE CONNECTION ---
DB_PATH = Path(__file__).parents[1] / "wishlist.db"
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# --- LOAD DATA ---
df = pd.read_sql("SELECT * FROM items ORDER BY created_at DESC", conn)

if df.empty:
    st.warning("Your wishlist is currently empty. Start adding items!")
    st.stop()

# Convert timestamp to readable datetime
if 'created_at' in df.columns:
    df["created_at"] = pd.to_datetime(df["created_at"], unit="s")

# Define categories
CATEGORIES = ["Uncategorized", "Clothing", "Electronics", "Home & Furniture", "Gifts", "Miscellaneous"]

# --- STYLING HEADER ---
st.markdown("""
    <h1 style='text-align: center; font-size: 48px;'>🛍️ My Shopping Wishlist</h1>
    <h4 style='text-align: center; color: gray;'>Visual Dashboard</h4>
""", unsafe_allow_html=True)

st.markdown(f"<p style='text-align: center;'>Total Items: <b>{len(df)}</b></p>", unsafe_allow_html=True)

st.markdown("""<hr style='margin-top: 10px; margin-bottom: 10px;'>""", unsafe_allow_html=True)

# Display items in a responsive grid
cols = st.columns(3)  # Adjust number of columns as needed

for idx, row in df.iterrows():
    col = cols[idx % 3]
    with col:
        st.markdown("""
            <div style='border: 1px solid #ccc; border-radius: 12px; 
                        padding: 16px; margin-bottom: 20px; 
                        background-color: #fafafa; 
                        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);'>
        """, unsafe_allow_html=True)

        # --- IMAGE ---
        if row.get("image_url"):
            st.image(row["image_url"], width=200)

        # --- TITLE ---
        st.markdown(f"<h4 style='margin: 8px 0;'>{row['title']}</h4>", unsafe_allow_html=True)

        # --- PRICE ---
        st.markdown(f"<p style='margin:0;'>💲 <b>{row['price']}</b></p>", unsafe_allow_html=True)

        # --- TIMESTAMP ---
        st.markdown(f"<p style='margin:0;'>🕒 {row['created_at'].strftime('%Y-%m-%d %H:%M:%S')}</p>", unsafe_allow_html=True)

        # --- CATEGORY SELECT ---
        # Determine the index of the current category in the CATEGORIES list
        current_cat = row["category"] if row["category"] else "Uncategorized"
        if current_cat not in CATEGORIES:
            current_cat = "Uncategorized"
        selected_cat = st.selectbox(
            "Category",
            CATEGORIES,
            index=CATEGORIES.index(current_cat),
            key=f"cat_select_{row['id']}"
        )

        # --- UPDATE BUTTON ---
        if st.button("Update Category", key=f"update_btn_{row['id']}"):
            # Update the database
            c.execute("UPDATE items SET category=? WHERE id=?", (selected_cat, row["id"]))
            conn.commit()
            st.experimental_rerun()  # Refresh the page to see updated category

        # --- PRODUCT LINK ---
        if row.get("url"):
            st.markdown(f"<a href='{row['url']}' target='_blank'>🔗 View Product</a>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

conn.close()
