import streamlit as st
import pandas as pd
from datetime import datetime

# Set page config and title
st.set_page_config(page_title="My Shopping Wishlist", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 30px;
    }
    .section-header {
        background-color: #f5f5f5;
        padding: 15px;
        border-radius: 5px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .item-card {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        transition: transform 0.2s;
    }
    .item-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .priority-high {
        background-color: #e8f5e9;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 14px;
    }
    .priority-medium {
        background-color: #e3f2fd;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 14px;
    }
    .item-price {
        font-weight: bold;
        font-size: 18px;
    }
    .item-link {
        margin-top: 10px;
        text-decoration: none;
    }
    .category-bubble {
        background-color: #f5f5f5;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        cursor: pointer;
        transition: all 0.3s;
    }
    .category-bubble:hover {
        background-color: #e0e0e0;
    }
    .category-bubble.active {
        background-color: #e3f2fd;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transform: scale(1.05);
    }
    .category-count {
        color: #616161;
        font-size: 14px;
        margin-top: 5px;
    }
    .sort-container {
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    /* Hide the button elements */
    div[data-testid="element-container"]:has(button[data-testid="baseButton-Select All"]),
    div[data-testid="element-container"]:has(button[data-testid="baseButton-Select Clothing"]),
    div[data-testid="element-container"]:has(button[data-testid="baseButton-Select Electronics"]),
    div[data-testid="element-container"]:has(button[data-testid="baseButton-Select Home & Furniture"]),
    div[data-testid="element-container"]:has(button[data-testid="baseButton-Select Miscellaneous"]) {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("<h1 class='main-header'>My Shopping Wishlist</h1>", unsafe_allow_html=True)

# Initialize session state for selected category and sort option
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = "All"
if 'sort_by' not in st.session_state:
    st.session_state.sort_by = "price_low_high"

# Sample data (this would come from your SQLite database)
def get_dummy_data():
    items = [
        {
            "id": 1,
            "title": "MacBook Pro M3",
            "price": 1800.00,
            "image_url": "https://example.com/macbook.jpg",
            "url": "https://www.apple.com/macbook-pro/",
            "category": "Electronics",
            "note": "Wait for student discount season",
            "priority": "High",
            "timestamp": datetime.now()
        },
        {
            "id": 2,
            "title": "Nike Interact Run",
            "price": 200.00,
            "image_url": "https://example.com/nike.jpg",
            "url": "https://www.nike.com/",
            "category": "Clothing",
            "note": "Need for spring training",
            "priority": "High",
            "timestamp": datetime.now()
        },
        {
            "id": 3,
            "title": "Yoga Mat",
            "price": 60.00,
            "image_url": "https://example.com/yogamat.jpg",
            "url": "https://www.lululemon.com/",
            "category": "Home & Furniture",
            "note": "For home workouts",
            "priority": "High",
            "timestamp": datetime.now()
        },
        {
            "id": 4,
            "title": "Winter Coat",
            "price": 990.00,
            "image_url": "https://example.com/coat.jpg",
            "url": "https://www.patagonia.com/",
            "category": "Clothing",
            "note": "Check end-of-season sales",
            "priority": "Medium",
            "timestamp": datetime.now()
        },
        {
            "id": 5,
            "title": "S1 Lift Standing Desk",
            "price": 449.00,
            "image_url": "https://example.com/desk.jpg",
            "url": "https://www.fully.com/",
            "category": "Home & Furniture",
            "note": "Better posture for work",
            "priority": "Medium",
            "timestamp": datetime.now()
        },
        {
            "id": 6,
            "title": "Laptop Backpack",
            "price": 79.99,
            "image_url": "https://example.com/backpack.jpg",
            "url": "https://www.thenorthface.com/",
            "category": "Miscellaneous",
            "note": "For daily commute",
            "priority": "Medium",
            "timestamp": datetime.now()
        }
    ]
    return pd.DataFrame(items)

# Get data
data = get_dummy_data()

# Create a two-column layout
col1, col2 = st.columns([1, 3])

# Column 1: Categories sidebar
with col1:
    st.markdown("<div class='section-header'>CATEGORIES</div>", unsafe_allow_html=True)
    
    # Function to handle category clicks
    def handle_category_click(category):
        st.session_state.selected_category = category
        
    # Add "All" category option
    all_active = st.session_state.selected_category == "All"
    all_class = "category-bubble active" if all_active else "category-bubble"
    all_count = len(data)
    
    all_bubble = f"""
    <div class='{all_class}' id="all-category">
        <strong>All</strong>
        <div class='category-count'>Total Items: {all_count}</div>
    </div>
    """
    st.markdown(all_bubble, unsafe_allow_html=True)
    
    # Use a hidden button that will be clicked by our JavaScript
    if st.button("Select All", key="select_all_btn", help="Show all items"):
        handle_category_click("All")
    
    # Get unique categories and their counts
    categories = ["Clothing", "Electronics", "Home & Furniture", "Miscellaneous"]
    
    # Display each category with count
    for i, category in enumerate(categories):
        item_count = len(data[data['category'] == category])
        is_active = st.session_state.selected_category == category
        bubble_class = "category-bubble active" if is_active else "category-bubble"
        
        category_bubble = f"""
        <div class='{bubble_class}' id="{category.lower().replace(' & ', '-')}-category">
            <strong>{category}</strong>
            <div class='category-count'>Total Items: {item_count}</div>
        </div>
        """
        st.markdown(category_bubble, unsafe_allow_html=True)
        
        # Add a hidden button for each category
        if st.button(f"Select {category}", key=f"select_{category.lower().replace(' & ', '_')}_btn", help=f"Show {category} items"):
            handle_category_click(category)
    
    # Add JavaScript to make the category bubbles clickable
    st.markdown("""
    <script>
        // Function to wait for elements to be available in the DOM
        function waitForElements(selector, callback) {
            if (document.querySelector(selector)) {
                callback();
            } else {
                setTimeout(function() { waitForElements(selector, callback); }, 100);
            }
        }
        
        // Wait for all category elements to be loaded
        waitForElements('#all-category', function() {
            // Make "All" category clickable
            const allCategory = document.getElementById('all-category');
            allCategory.addEventListener('click', function() {
                const allButton = document.querySelector('button[data-testid="baseButton-Select All"]');
                allButton.click();
            });
            
            // Make "Clothing" category clickable
            const clothingCategory = document.getElementById('clothing-category');
            clothingCategory.addEventListener('click', function() {
                const clothingButton = document.querySelector('button[data-testid="baseButton-Select Clothing"]');
                clothingButton.click();
            });
            
            // Make "Electronics" category clickable
            const electronicsCategory = document.getElementById('electronics-category');
            electronicsCategory.addEventListener('click', function() {
                const electronicsButton = document.querySelector('button[data-testid="baseButton-Select Electronics"]');
                electronicsButton.click();
            });
            
            // Make "Home & Furniture" category clickable
            const homeCategory = document.getElementById('home-furniture-category');
            homeCategory.addEventListener('click', function() {
                const homeButton = document.querySelector('button[data-testid="baseButton-Select Home & Furniture"]');
                homeButton.click();
            });
            
            // Make "Miscellaneous" category clickable
            const miscCategory = document.getElementById('miscellaneous-category');
            miscCategory.addEventListener('click', function() {
                const miscButton = document.querySelector('button[data-testid="baseButton-Select Miscellaneous"]');
                miscButton.click();
            });
        });
    </script>
    """, unsafe_allow_html=True)

# Column 2: Items display
with col2:
    st.markdown("<div class='section-header'>PURCHASING THIS MONTH</div>", unsafe_allow_html=True)
    
    # Add sorting options
    sort_col1, sort_col2 = st.columns([3, 1])
    
    with sort_col1:
        sort_options = {
            "price_low_high": "Price: Low to High",
            "price_high_low": "Price: High to Low",
            "priority": "Priority",
            "timestamp": "Date Added"
        }
        
        selected_sort = st.selectbox(
            "Sort by:",
            options=list(sort_options.keys()),
            format_func=lambda x: sort_options[x],
            index=list(sort_options.keys()).index(st.session_state.sort_by),
            key="sort_selector"
        )
        
        # Update session state when sort option changes
        if selected_sort != st.session_state.sort_by:
            st.session_state.sort_by = selected_sort
    
    # Filter data based on selected category
    filtered_data = data if st.session_state.selected_category == "All" else data[data['category'] == st.session_state.selected_category]
    
    # Sort the data
    if st.session_state.sort_by == "price_low_high":
        filtered_data = filtered_data.sort_values("price")
    elif st.session_state.sort_by == "price_high_low":
        filtered_data = filtered_data.sort_values("price", ascending=False)
    elif st.session_state.sort_by == "priority":
        # Custom sort for priority (High first, then Medium, then Low)
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        filtered_data = filtered_data.sort_values("priority", key=lambda x: x.map(priority_order))
    elif st.session_state.sort_by == "timestamp":
        filtered_data = filtered_data.sort_values("timestamp", ascending=False)
    
    if len(filtered_data) == 0:
        st.info(f"No items found in the '{st.session_state.selected_category}' category.")
    else:
        # Create 3 columns for the items grid
        item_cols = st.columns(3)
        
        # Display items in a grid
        for i, item in enumerate(filtered_data.to_dict('records')):
            col_index = i % 3
            
            with item_cols[col_index]:
                st.markdown(f"""
                <div class='item-card'>
                    <div style='height: 150px; background-color: #f0f0f0; border-radius: 5px; margin-bottom: 10px; display: flex; justify-content: center; align-items: center;'>
                        <span style='color: #999;'>Product Image</span>
                    </div>
                    <h3>{item['title']}</h3>
                    <div class='item-price'>${item['price']:.2f}</div>
                    <div style='margin-top: 10px;'>
                        <span class='priority-{item['priority'].lower()}'>{item['priority']}</span>
                    </div>
                    <div class='item-link'>
                        <a href="{item['url']}" target="_blank">Visit Website →</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)