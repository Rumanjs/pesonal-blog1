"""
models.py — Database Models
-----------------------------
Defines the SQLAlchemy ORM models for the blog application.
Each class maps to a table in the SQLite database.
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy database instance.
# This object is imported in app.py and bound to the Flask app.
db = SQLAlchemy()


class BlogPost(db.Model):
    """
    Represents a single blog post in the database.

    Columns:
        id              — Primary key (auto-incremented integer).
        title           — Title of the blog post (max 200 chars).
        content         — Full body text of the post.
        author          — Name of the person who wrote the post (max 100 chars).
        category        — User-selected category (e.g., AI/ML, Web Dev).
        sentiment       — AI-generated sentiment label (Positive / Negative / Neutral).
        sentiment_score — Numerical polarity score from TextBlob (-1.0 to 1.0).
        keywords        — AI-extracted keywords stored as a comma-separated string.
        date_posted     — Timestamp of when the post was created (defaults to now).
    """

    # Table name (optional — SQLAlchemy auto-generates from class name)
    __tablename__ = "blog_post"

    # ── Columns ──────────────────────────────────────────────────────────────

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    content = db.Column(db.Text, nullable=False)

    author = db.Column(db.String(100), nullable=False, default="Anonymous")

    category = db.Column(db.String(50), nullable=False, default="General")

    # AI/ML-generated fields ─────────────────────────────────────────────────

    sentiment = db.Column(db.String(20), default="Neutral")

    sentiment_score = db.Column(db.Float, default=0.0)

    keywords = db.Column(db.String(500), default="")

    # Timestamp ──────────────────────────────────────────────────────────────

    date_posted = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )

    def __repr__(self):
        """Return a human-readable representation of the post."""
        return f"BlogPost('{self.title}', '{self.date_posted}')"
