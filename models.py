from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(256), unique=True, nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    game_progress = db.Column(db.Text, nullable=True)  # JSON string to store progress

    def __init__(self, google_id, email, game_progress="{}"):
        self.google_id = google_id
        self.email = email
        self.game_progress = game_progress
