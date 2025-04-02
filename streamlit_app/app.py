import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
from datetime import datetime
import math

# ---------- CONFIG ----------
st.set_page_config(page_title="Shopping Wishlist", layout="wide")

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

# Count how many items fall into each category
cat_counts = {cat: 0 for cat in ALL_CATEGORIES}
for cat in df["category"].fillna("Uncategorized"):
    if cat in cat_counts:
        cat_counts[cat] += 1
    else:
        # If there are categories in the DB not in ALL_CATEGORIES, add them:
        cat_counts[cat] = cat_counts.get(cat, 0) + 1

# Also add an "All" option
cat_counts["All"] = len(df)

# Initialize selected category in session state
if "selected_category" not in st.session_state:
    st.session_state["selected_category"] = "All"

# ---------- SIDEBAR LAYOUT ----------
with st.sidebar:
    st.markdown("<h2 style='font-weight: bold;'>CATEGORIES</h2>", unsafe_allow_html=True)

    # CSS for the category cards in the sidebar
    st.markdown("""
    <style>
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
    """, unsafe_allow_html=True)

    def render_category_card(cat_name, cat_count):
        """Renders a clickable card in the sidebar for each category."""
        is_active = (cat_name == st.session_state["selected_category"])
        active_class = "active" if is_active else ""

        # Render the card
        st.markdown(f"""
        <div class="category-card {active_class}">
            <h4 style="margin: 0; font-weight:600;">{cat_name}</h4>
            <p style="margin: 0;">Total Items: {cat_count}</p>
        </div>
        """, unsafe_allow_html=True)

        # Invisible button to handle the click
        if st.button(f"Select {cat_name}", key=f"cat_{cat_name}"):
            st.session_state["selected_category"] = cat_name
            # If your Streamlit supports it, refresh the page:
            # st.experimental_rerun()

    # Render "All" card
    render_category_card("All", cat_counts["All"])
    # Render each known category
    for cat in ALL_CATEGORIES:
        render_category_card(cat, cat_counts[cat])

# ---------- MAIN AREA ----------
st.markdown("<h1 style='margin-bottom: 0;'>My Shopping Wishlist</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='color: #666; margin-top: 0;'>Purchasing This Month</h4>", unsafe_allow_html=True)

selected_cat = st.session_state["selected_category"]

# Filter DataFrame
if selected_cat == "All":
    df_filtered = df.copy()
else:
    df_filtered = df[df["category"].fillna("Uncategorized") == selected_cat]

# Show item count
st.markdown(f"<p style='font-size: 16px; color: #555;'>{len(df_filtered)} items</p>", unsafe_allow_html=True)

# CSS for product cards
st.markdown("""
<style>
.product-card {
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 16px;
    margin-bottom: 16px;
    background-color: #fff;
    transition: box-shadow 0.2s ease;
}
.product-card:hover {
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# Display products in a grid
NUM_COLS = 3
items = df_filtered.reset_index(drop=True)
num_rows = math.ceil(len(items) / NUM_COLS)

for row_idx in range(num_rows):
    cols = st.columns(NUM_COLS)
    for col_idx in range(NUM_COLS):
        item_idx = row_idx * NUM_COLS + col_idx
        if item_idx < len(items):
            row = items.loc[item_idx]
            with cols[col_idx]:
                st.markdown("<div class='product-card'>", unsafe_allow_html=True)
                
                # Image
                if row.get("image_url"):
                    st.image(row["image_url"], use_column_width=True)

                # Title
                st.markdown(f"<h4 style='margin-top: 10px;'>{row['title']}</h4>", unsafe_allow_html=True)

                # Price
                st.markdown(f"<p style='margin:0; font-weight:bold;'>${row['price']}</p>", unsafe_allow_html=True)

                # Category
                cat_text = row["category"] if row["category"] else "Uncategorized"
                st.markdown(f"<p style='margin:0;'>Category: {cat_text}</p>", unsafe_allow_html=True)

                # Created date
                if pd.notnull(row.get("created_at")):
                    created_str = row["created_at"].strftime('%Y-%m-%d')
                    st.markdown(f"<p style='margin:0;'>Added: {created_str}</p>", unsafe_allow_html=True)

                # Product link
                if row.get("url"):
                    st.markdown(f"<a href='{row['url']}' target='_blank'>🔗 View Product</a>", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)
