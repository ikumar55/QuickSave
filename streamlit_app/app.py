import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
from datetime import datetime
import math

# ---------- CONFIG ----------
st.set_page_config(page_title="My Shopping Wishlist", layout="wide")

# --- SINGLE-BORDER PRODUCT CARD CSS ---
st.markdown(
    """
    <style>
    /* Make the overall page background just pure white for clarity */
    body {
        background-color: #ffffff !important;
    }

    /* Card container with a single continuous border, rounded corners */
    .product-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        background-color: #fff;
        margin-bottom: 16px;
        overflow: hidden;  /* Keeps corners rounded at the image top */
        transition: box-shadow 0.2s ease;
        display: flex;
        flex-direction: column;
    }
    .product-card:hover {
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    }

    /* Solid black placeholder for the image area, with a bottom border so that
       we get a distinct line where the image ends and the content begins */
    .product-image-placeholder {
        background-color: #000; 
        width: 100%;
        height: 150px;
        border-bottom: 1px solid #ddd;
    }

    /* Content area inside the card */
    .product-content {
        padding: 12px 16px;
    }
    .product-content h4 {
        margin-top: 0;
        margin-bottom: 8px;
    }
    .product-content p {
        margin: 4px 0;
    }
    .product-content a {
        color: #007bff;
        text-decoration: none;
        font-weight: 500;
    }
    .product-content a:hover {
        text-decoration: underline;
    }

    /* Category 'cards' (left panel) remain the same */
    .category-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 12px;
        cursor: pointer;
        background-color: #f8f8f8;
        transition: background-color 0.2s ease;
    }
    .category-card:hover {
        background-color: #f0f0f0;
    }
    .category-card.active {
        background-color: #e0e0e0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

DB_PATH = Path(__file__).parents[1] / "wishlist.db"

# ---------- LOAD DATA ----------
conn = sqlite3.connect(DB_PATH)
df = pd.read_sql("SELECT * FROM items ORDER BY created_at DESC", conn)
conn.close()

if df.empty:
    st.warning("Your wishlist is currently empty. Start adding items!")
    st.stop()

# Convert timestamp to readable datetime
if 'created_at' in df.columns:
    df["created_at"] = pd.to_datetime(df["created_at"], unit="s", errors="coerce")

# ---------- DEFINE & COUNT CATEGORIES ----------
ALL_CATEGORIES = ["Clothing", "Electronics", "Home & Furniture", "Books", "Miscellaneous", "Uncategorized"]
cat_counts = {cat: 0 for cat in ALL_CATEGORIES}

for cat in df["category"].fillna("Uncategorized"):
    if cat in cat_counts:
        cat_counts[cat] += 1
    else:
        cat_counts[cat] = cat_counts.get(cat, 0) + 1

cat_counts["All"] = len(df)

if "selected_category" not in st.session_state:
    st.session_state["selected_category"] = "All"

# ---------- PAGE HEADER ----------
st.markdown("<h1 style='margin-bottom: 0;'>My Shopping Wishlist</h1>", unsafe_allow_html=True)

# Create two columns: left for categories, right for the wishlist items
left_col, right_col = st.columns([2, 5], gap="large")

# ---------- LEFT COLUMN: CATEGORIES ----------
with left_col:
    st.markdown("<h3 style='margin-top: 20px;'>Categories</h3>", unsafe_allow_html=True)

    def render_category_card(cat_name, cat_count):
        is_active = (cat_name == st.session_state["selected_category"])
        active_class = "active" if is_active else ""

        st.markdown(f"""
        <div class="category-card {active_class}">
            <h4 style="margin: 0; font-weight:600;">{cat_name}</h4>
            <p style="margin: 0;">Total Items: {cat_count}</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Select {cat_name}", key=f"cat_{cat_name}"):
            st.session_state["selected_category"] = cat_name

    # Render "All" card first
    render_category_card("All", cat_counts["All"])

    # Render each known category
    for cat in ALL_CATEGORIES:
        render_category_card(cat, cat_counts[cat])

# ---------- RIGHT COLUMN: "CONSIDERING PURCHASING" + ITEM CARDS ----------
with right_col:
    st.markdown("<h3 style='margin-top: 20px;'>Considering Purchasing</h3>", unsafe_allow_html=True)

    selected_cat = st.session_state["selected_category"]
    if selected_cat == "All":
        df_filtered = df.copy()
    else:
        df_filtered = df[df["category"].fillna("Uncategorized") == selected_cat]

    st.markdown(f"<p style='font-size: 16px; color: #555;'>{len(df_filtered)} items</p>", unsafe_allow_html=True)

    # ---------- DISPLAY PRODUCTS IN A GRID (4 items per row) ----------
    NUM_COLS = 4
    items = df_filtered.reset_index(drop=True)
    num_rows = math.ceil(len(items) / NUM_COLS)

    for row_idx in range(num_rows):
        cols = st.columns(NUM_COLS)
        for col_idx in range(NUM_COLS):
            item_idx = row_idx * NUM_COLS + col_idx
            if item_idx < len(items):
                row = items.loc[item_idx]
                with cols[col_idx]:
                    # Wrap the entire card
                    st.markdown("<div class='product-card'>", unsafe_allow_html=True)

                    # Top "image" area (just a black placeholder)
                    st.markdown("<div class='product-image-placeholder'></div>", unsafe_allow_html=True)

                    # Content
                    st.markdown("<div class='product-content'>", unsafe_allow_html=True)

                    st.markdown(f"<h4>{row['title']}</h4>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-weight:bold;'>${row['price']}</p>", unsafe_allow_html=True)

                    cat_text = row["category"] if row["category"] else "Uncategorized"
                    st.markdown(f"<p>Category: {cat_text}</p>", unsafe_allow_html=True)

                    if pd.notnull(row.get("created_at")):
                        created_str = row["created_at"].strftime('%Y-%m-%d')
                        st.markdown(f"<p>Added: {created_str}</p>", unsafe_allow_html=True)

                    if row.get("url"):
                        st.markdown(
                            f"<a href='{row['url']}' target='_blank'>🔗 View Product</a>", 
                            unsafe_allow_html=True
                        )

                    st.markdown("</div>", unsafe_allow_html=True)  # Close product-content
                    st.markdown("</div>", unsafe_allow_html=True)  # Close product-card
