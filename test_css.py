import streamlit as st
import pandas as pd
from datetime import datetime

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="My Shopping Wishlist", layout="wide")

# ─── SESSION STATE ─────────────────────────────────────────────────────────────
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = "All"
if 'sort_by' not in st.session_state:
    st.session_state.sort_by = "timestamp"           # ← now defaults to Date Added
if 'view_table' not in st.session_state:
    st.session_state.view_table = False

# ─── DUMMY DATA ────────────────────────────────────────────────────────────────
def get_dummy_data():
    items = [
        {"id":1, "title":"MacBook Pro M3",       "price":1800.00, "category":"Electronics",      "priority":"High",   "url":"https://www.apple.com/macbook-pro/",  "timestamp":datetime.now()},
        {"id":2, "title":"Nike Interact Run",     "price":200.00,  "category":"Clothing",         "priority":"High",   "url":"https://www.nike.com/",               "timestamp":datetime.now()},
        {"id":3, "title":"Yoga Mat",              "price":60.00,   "category":"Home & Furniture", "priority":"High",   "url":"https://www.lululemon.com/",           "timestamp":datetime.now()},
        {"id":4, "title":"Winter Coat",           "price":990.00,  "category":"Clothing",         "priority":"Medium", "url":"https://www.patagonia.com/",           "timestamp":datetime.now()},
        {"id":5, "title":"S1 Lift Standing Desk", "price":449.00,  "category":"Home & Furniture", "priority":"Medium","url":"https://www.fully.com/",                "timestamp":datetime.now()},
        {"id":6, "title":"Laptop Backpack",       "price":79.99,   "category":"Miscellaneous",    "priority":"Medium","url":"https://www.thenorthface.com/",         "timestamp":datetime.now()}
    ]
    return pd.DataFrame(items)

data = get_dummy_data()

# ─── GLOBAL CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* CATEGORY BUTTONS */
div.stButton > button {
    width: 100% !important;
    display: block;
    text-align: left;
    padding: 12px 16px;
    margin-bottom: 12px;
    background-color: #f5f5f5 !important;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    transition: background-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
}
div.stButton > button:hover {
    background-color: #e0e0e0 !important;
    transform: scale(1.03) !important;
    box-shadow: 0 6px 12px rgba(0,0,0,0.1) !important;
}
div.stButton > button:focus {
    background-color: #e3f2fd !important;
    transform: scale(1.05);
    box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    outline: none;
}
div.stButton > button, div.stButton > button > * {
    white-space: pre-line !important;
}

/* HEADERS */
.main-header { font-size: 42px; font-weight: bold; margin-bottom: 30px; }
.section-header {
    background-color: #f5f5f5; padding: 15px; border-radius: 5px;
    font-weight: bold; margin-bottom: 20px;
}

/* ITEM CARDS */
.item-card {
    border: 1px solid #e0e0e0; border-radius: 10px;
    padding: 15px; margin-bottom: 15px;
    transition: transform 0.2s, box-shadow 0.2s;
}
.item-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

/* PRIORITY PILL */
.priority-High { background-color: #e8f5e9; padding:5px 10px; border-radius:15px; font-size:14px; }
.priority-Medium { background-color: #e3f2fd; padding:5px 10px; border-radius:15px; font-size:14px; }

/* PRICE & LINK */
.item-price { font-weight:bold; font-size:18px; }
.item-link a { margin-top:10px; text-decoration:none; }
</style>
""", unsafe_allow_html=True)

# ─── LAYOUT ───────────────────────────────────────────────────────────────────
st.markdown("<h1 class='main-header'>My Shopping Wishlist</h1>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 3])

# ─── LEFT: CATEGORIES ─────────────────────────────────────────────────────────
with col1:
    st.markdown("<div class='section-header'>CATEGORIES</div>", unsafe_allow_html=True)
    categories = ["All", "Clothing", "Electronics", "Home & Furniture", "Miscellaneous"]
    counts     = data['category'].value_counts().to_dict()
    counts['All'] = len(data)

    for cat in categories:
        label = f"{cat}\nTotal Items: {counts.get(cat, 0)}"
        if st.button(label, key=f"btn_{cat.replace(' & ','_').lower()}"):
            st.session_state.selected_category = cat
            st.session_state.view_table = False  # reset back to grid

# ─── RIGHT: SEARCH + SORT + TOGGLE + DISPLAY ──────────────────────────────────
with col2:
    st.markdown("<div class='section-header'>PURCHASING THIS MONTH</div>", unsafe_allow_html=True)

    # ── three columns: search | sort | table‑view toggle ──
    c_search, c_sort, c_view = st.columns([4, 1, 1])

    # Search input
    search = c_search.text_input("", placeholder="🔍 Search items", key="search")

    # Sort dropdown **bound directly** to session_state.sort_by
    sort_opts = {
        "timestamp":       "Date Added",        # ← moved first
        "price_low_high":  "Price: Low → High",
        "price_high_low":  "Price: High → Low",
        "priority":        "Priority"
    }
    _ = c_sort.selectbox(
        "",
        options=list(sort_opts.keys()),
        format_func=lambda x: sort_opts[x],
        key="sort_by"
    )
    # immediately reset to grid when user picks a new sort
    if st.session_state.get("_last_sort") != st.session_state.sort_by:
        st.session_state.view_table = False
    st.session_state._last_sort = st.session_state.sort_by

    # Table view checkbox, nudged down to align vertically
    with c_view:
        st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)
        view_table = st.checkbox(
            "Table view",
            value=st.session_state.view_table,
            key="view_table"
        )

    # Filter & search
    df = data if st.session_state.selected_category == "All" else data[data.category == st.session_state.selected_category]
    if search:
        df = df[df.title.str.contains(search, case=False, na=False)]

    # Sorting logic
    if st.session_state.sort_by == "price_low_high":
        df = df.sort_values("price")
    elif st.session_state.sort_by == "price_high_low":
        df = df.sort_values("price", ascending=False)
    elif st.session_state.sort_by == "priority":
        order = {"High":0, "Medium":1, "Low":2}
        df = df.sort_values("priority", key=lambda s: s.map(order))
    else:
        df = df.sort_values("timestamp", ascending=False)

    # Display
    if df.empty:
        st.info("No items found.")
    else:
        if view_table:
            # hide the index by resetting it
            st.dataframe(df.reset_index(drop=True))
        else:
            cols = st.columns(3)
            for i, item in enumerate(df.to_dict("records")):
                with cols[i % 3]:
                    st.markdown(f"""
                        <div class='item-card'>
                          <div style='height:150px; background:#f0f0f0;
                                      border-radius:5px; margin-bottom:10px;
                                      display:flex; align-items:center;
                                      justify-content:center;'>
                            <span style='color:#999;'>Product Image</span>
                          </div>
                          <h3>{item['title']}</h3>
                          <div class='item-price'>${item['price']:.2f}</div>
                          <div style='margin-top:10px;'>
                            <span class='priority-{item['priority']}'>{item['priority']}</span>
                          </div>
                          <div class='item-link'>
                            <a href="{item['url']}" target="_blank">Visit Website →</a>
                          </div>
                        </div>
                    """, unsafe_allow_html=True)







# THINGS TO FIX: Keep the categories on the LHS shaded blue even after we click elsewhere on the dashboard
# get rid of index column on dataframe when in table view