from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from database import db  # Import `db` from database.py
import random
import json
from game_logic import Character, Game, Event, Location, UserInputParser
from dotenv import load_dotenv
import os

# Explicitly specify the .env file path if needed
load_dotenv(dotenv_path=".env")

import auth

# Debugging: Print variables to confirm they're loaded
print("GOOGLE_CLIENT_ID:", os.getenv("GOOGLE_CLIENT_ID"))
print("GOOGLE_CLIENT_SECRET:", os.getenv("GOOGLE_CLIENT_SECRET"))
print("REDIRECT_URI:", os.getenv("REDIRECT_URI"))
print("FLASK_SECRET_KEY:", os.getenv("FLASK_SECRET_KEY"))
print("DATABASE_URL:", os.getenv("DATABASE_URL"))

import auth

# Use environment variables for sensitive data
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "default_secret_key")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///game.db")


# Flask app setup
# Explicitly specify `templates` and `static` folders within the "WorkingCode" directory
app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "static")
)
app.secret_key = FLASK_SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL

# Initialize `db` with the Flask app
db.init_app(app)

# Database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120))
    progress = db.Column(db.Text, default="{}")  # JSON field to store game progress

# Game initialization
def initialize_game():
    heroes = [Character("Iron Man"), Character("Captain America"), Character("Thor")]
    parser = UserInputParser()

    enemies = [
        {"name": "Loki", "health": 75, "attack": "Deceptive Strike"},
        {"name": "Ultron", "health": 150, "attack": "Laser Beam"}
    ]

    thanos = Character("Thanos", health=500, attack_power=25, special_move=50)  # Final boss

    event1 = Event({
        'primary_attribute': 'Strength',
        'success_message': 'You overpowered Loki!',
        'failure_message': 'Loki outsmarts you!',
        'partial_pass': {'message': 'Loki retreats, but he will return.'}
    }, enemy=enemies[0])

    event2 = Event({
        'primary_attribute': 'Intelligence',
        'success_message': 'You solved the puzzle!',
        'failure_message': 'The trap is triggered!',
        'partial_pass': {'message': 'You barely escape the trap.'}
    }, enemy=enemies[1])

    location1 = Location("Asgard Throne Room", [event1])
    location2 = Location("Mystic Forest", [event2])

    game = Game(parser, heroes, [location1, location2])
    game.enemies = enemies  # Attach enemies to the game object for global access
    return game

# Initialize game globally
game = initialize_game()

@app.route("/login")
def login():
    google_auth_url = auth.get_google_auth_url()
    return redirect(google_auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    user_info = auth.get_google_user_info(code)

    user = User.query.filter_by(email=user_info["email"]).first()
    if not user:
        user = User(email=user_info["email"], name=user_info["name"], progress="{}")
        db.session.add(user)
    session["user_id"] = user.id
    db.session.commit()

    return redirect(url_for("game_route"))

@app.route("/game")
def game_route():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])
    progress = json.loads(user.progress)
    return jsonify({"message": f"Welcome back, {user.name}!", "progress": progress})

@app.route("/save", methods=["POST"])
def save():
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 403

    user = User.query.get(session["user_id"])
    progress = request.json.get("progress")
    if progress:
        user.progress = json.dumps(progress)
        db.session.commit()
        return jsonify({"message": "Progress saved!"})
    return jsonify({"error": "No progress data provided"}), 400

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/battle")
def battle():
    return render_template("battle.html")

@app.route("/get_characters", methods=["GET"])
def get_characters():
    return jsonify([{
        "name": char.name,
        "health": char.health,
        "class": char.hero_class
    } for char in game.party])

@app.route("/attack", methods=["POST"])
def attack():
    data = request.json
    char_name = data['character']
    attack_type = data['attack_type']

    character = next((c for c in game.party if c.name == char_name), None)
    if not character:
        return jsonify({"error": "Character not found"}), 404

    # Select a random enemy from the game object
    current_enemy = random.choice(game.enemies)

    if attack_type == "special":
        character.perform_special_move(current_enemy)
    else:
        chosen_stat = character.get_stats()[0]
        character.basic_attack(chosen_stat, current_enemy)

    # Check if enemy is defeated
    if current_enemy['health'] <= 0:
        game.enemies.remove(current_enemy)  # Remove defeated enemy
        return jsonify({"message": f"You defeated {current_enemy['name']}!"})

    return jsonify({
        "message": f"{character.name} attacked {current_enemy['name']}!",
        "enemy_health": current_enemy['health'],
        "character_health": character.health
    })

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Initialize database tables
    app.run(debug=True)
