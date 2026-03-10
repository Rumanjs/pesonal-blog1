"""
wsgi.py — WSGI Entry Point for Production Deployment
-------------------------------------------------------
This file is used by production WSGI servers (Gunicorn, Waitress)
to import and run the Flask application.

Used by:
    • Render  → gunicorn wsgi:app
    • Railway → gunicorn wsgi:app
    • Vercel  → references this in vercel.json
"""

from app import app

# Download NLTK data on first startup (needed for keyword extraction)
import nltk
import os

# Set NLTK data path for cloud environments
nltk_data_dir = os.path.join(os.path.dirname(__file__), "nltk_data")
os.makedirs(nltk_data_dir, exist_ok=True)
nltk.data.path.append(nltk_data_dir)

# Download required NLTK packages if not already present
for package in ["punkt", "stopwords", "punkt_tab"]:
    try:
        nltk.data.find(f"tokenizers/{package}" if "punkt" in package else f"corpora/{package}")
    except LookupError:
        nltk.download(package, download_dir=nltk_data_dir)

if __name__ == "__main__":
    app.run()
