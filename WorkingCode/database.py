import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Default to SQLite for local storage if DATABASE_URL is not set
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///local_game.db")

# Initialize the SQLAlchemy object
db = SQLAlchemy()

def init_app(app):
    """
    Initialize the Flask app with SQLAlchemy.
    """
    # Set the database connection URL for SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable SQLAlchemy event system (optional performance boost)

    # Bind SQLAlchemy to the app
    db.init_app(app)
