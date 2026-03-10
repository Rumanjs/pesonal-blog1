"""
config.py — Application Configuration
---------------------------------------
Stores all configuration settings for the Flask application.
"""

import os

# Base directory of the project (used to construct the database path)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Configuration class for the Flask application.

    Attributes:
        SECRET_KEY: Used by Flask for session management and CSRF protection.
        SQLALCHEMY_DATABASE_URI: Connection string for the SQLite database.
        SQLALCHEMY_TRACK_MODIFICATIONS: Disables modification tracking to save memory.
    """

    # Secret key for encrypting session cookies
    # Set the SECRET_KEY environment variable in production!
    SECRET_KEY = os.environ.get("SECRET_KEY", "my-super-secret-key-change-me")

    # Database URI — supports cloud Postgres via DATABASE_URL env var,
    # falls back to local SQLite for development.
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "blog.db"),
    )

    # Fix for Render/Railway: they provide postgres:// but SQLAlchemy needs postgresql://
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgres://", "postgresql://", 1
        )

    # Disable Flask-SQLAlchemy event system (not needed, reduces overhead)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
