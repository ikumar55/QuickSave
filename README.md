# QuickSave

source venv/bin/activate







Project Name: Universal Shopping Wishlist App (with Data-Science-Friendly Backend)

High-Level Idea:

A Chrome extension that lets users save product info (title, price, URL, image) from any website with a single click.
A Python backend (using Flask or FastAPI) to store those items in a small database (e.g., SQLite).
A Streamlit (or similar) web app to display the saved items, filter them, add/delete, and optionally run data analysis (pandas, basic ML, etc.).
Core Goals:

Capture & Organize Products

The user visits a product page and clicks the browser extension button.
The extension sends product data to the Python API.
The data is stored in a database for later viewing and editing.
Provide a Simple Dashboard

A Streamlit dashboard shows the user’s wishlist items.
Users can view, edit, or delete items and see basic stats (e.g., how many items from each store).
Serve as a foundation for future data analysis (categorizing items, price comparisons, etc.).
Enable Data Science Exploration

Because the backend is in Python, we can easily incorporate pandas or scikit-learn for more advanced functionality:
NLP-based categorization of product titles,
Potential price tracking or ML-based price predictions later,
Visualization of user’s saved items and purchase trends.
Extend & Scale Gradually

Start with minimal features (just save items and display them).
Later, add user accounts, sharing, budgeting, or advanced analytics.
Low-cost, with potential to move to a small cloud deployment (e.g. free tier hosting) once stable.
Value Proposition:

A universal wishlist for any online store, not tied to Amazon or a single platform.
A data-friendly architecture that helps you practice Python, REST APIs, and data science libraries within a single project.
A foundation for future expansions like price alerts, social sharing, or ML recommendations.












Project Overview:
I’m building a Universal Shopping Wishlist App that lets users quickly save product info from any website using a Chrome extension. The saved data (title, URL, price, image URL, and timestamp) is sent to a Python backend built with FastAPI, stored in a SQLite database, and later displayed through a Streamlit dashboard for viewing and basic data analysis.

Project Structure:

graphql
Copy
quicksave/
├─ backend/
│   └─ main.py         # FastAPI backend that defines endpoints for POST and GET (handles wishlist items)
├─ extension/
│   ├─ manifest.json   # Chrome Extension manifest (Manifest V3) specifying default_popup
│   ├─ popup.html      # Basic UI for inputting title and price
│   └─ popup.js        # JavaScript that extracts data (including current tab URL) and sends a POST request to FastAPI
├─ streamlit_app/
│   └─ app.py          # Streamlit dashboard that reads the SQLite DB and displays the wishlist items
├─ wishlist.db         # SQLite database where the wishlist items are stored
└─ venv/               # Virtual environment with required Python packages (FastAPI, uvicorn, streamlit, etc.)
What’s Implemented So Far:

FastAPI Backend:
Runs at http://127.0.0.1:8000
Exposes a GET endpoint to fetch wishlist items and a POST endpoint (/api/wishlist) to add new items.
Uses CORSMiddleware to allow requests from any origin (resolving a CORS issue with the extension).
Initializes a SQLite database (wishlist.db) with a table for wishlist items.
Chrome Extension:
Manifest (v3) that points to popup.html for the user interface.
Popup interface lets the user manually enter a product title and price.
JavaScript (in popup.js) grabs the current tab’s URL, builds a JSON payload, and sends a POST request to the FastAPI backend.
Now properly sending requests after fixing CORS issues.
SQLite Database:
Data is stored in wishlist.db. I’ve confirmed entries exist via SQLite CLI.
Streamlit Dashboard:
A simple app in streamlit_app/app.py to query the SQLite database and display wishlist items in a table.
Current Status:

The FastAPI server is running, accessible via http://127.0.0.1:8000/docs.
The Chrome extension successfully sends POST requests to the backend (verified by data entries in SQLite).
Data has been verified in the database using the SQLite command line (entries are present).