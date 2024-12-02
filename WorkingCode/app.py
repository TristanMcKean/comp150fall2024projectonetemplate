from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from database import db, init_app  # Import `db` and `init_app` from database.py
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

# Initialize the database
init_app(app)

# Database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120))
    progress = db.Column(db.Text, default="{}")  # JSON field to store game progress
    total_hp = db.Column(db.Integer, default=100)  # Default HP
    level = db.Column(db.Integer, default=1)  # Default Level

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

@app.route('/arena')
def arena():
    # Check if the user is signed in
    if "user_id" in session:
        user = User.query.get(session["user_id"])
        if user:
            # Render the arena with the user's progress
            return render_template(
                'arena.html',
                total_hp=user.total_hp,
                level=user.level,
                user_name=user.name
            )

    # If the user is not signed in, render the arena with default stats
    return render_template(
        'arena.html',
        total_hp=100,  # Default HP for guests
        level=1,  # Default level for guests
        user_name="Guest"
    )


@app.route('/heroes')
def heroes():
    return render_template('heroes.html')

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "Missing authorization code from Google."}), 400

    # Fetch user info from Google
    try:
        user_info = auth.get_google_user_info(code)
    except Exception as e:
        return jsonify({"error": f"Failed to fetch user info: {str(e)}"}), 400

    # Ensure user info contains email
    if "email" not in user_info:
        return jsonify({"error": "Google did not return an email address."}), 400

    # Retrieve the user or create a new one
    user = User.query.filter_by(email=user_info["email"]).first()
    if not user:
        try:
            user = User(
                email=user_info["email"],
                name=user_info.get("name", "Unknown"),
                progress="{}"  # Initialize empty progress if new user
            )
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            return jsonify({"error": f"Failed to create user: {str(e)}"}), 500

    # Store user ID in session
    session["user_id"] = user.id

    # Debugging: Log the session info
    print("Session info after login:", session)

    # Redirect to the main page
    return redirect(url_for("index"))


@app.route("/gamestart")
def gamestart():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])
    if not user:
        return jsonify({"error": "User not found. Please log in again."}), 404

    # Load user's progress
    progress = json.loads(user.progress)

    # Extract level and total_hp, defaulting to 1 and 100 if not set
    level = progress.get("level", 1)
    total_hp = progress.get("total_hp", 100)

    # Render the game start screen and pass the progress data
    return render_template("index.html", level=level, total_hp=total_hp, user_name=user.name)

@app.route("/game")
def game_route():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])
    if not user:
        return jsonify({"error": "User not found. Please log in again."}), 404

    progress = json.loads(user.progress)
    return jsonify({"message": f"Welcome back, {user.name}!", "progress": progress})


@app.route("/save", methods=["POST"])
def save():
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 403

    user = User.query.get(session["user_id"])
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Retrieve the progress data from the request
    level = request.json.get("level")
    total_hp = request.json.get("total_hp")

    if level is not None and total_hp is not None:
        user.total_hp = total_hp
        user.level = level
        db.session.commit()
        return jsonify({"message": "Progress saved!"}), 200

    return jsonify({"error": "Missing level or total_hp in request"}), 400

@app.route("/")
def index():
    # Determine login status
    is_logged_in = "user_id" in session and session["user_id"]

    # Retrieve user information if logged in
    if is_logged_in:
        user = User.query.get(session["user_id"])
        if not user:  # Handle invalid user session
            session.pop("user_id", None)
            is_logged_in = False

    # Pass login status to template
    return render_template("index.html", is_logged_in=is_logged_in)


@app.route("/battle")
def battle():
    # Check if only Thanos is left
    thanos_only = len(game.enemies) == 1 and game.enemies[0]["name"] == "Thanos"
    return render_template("battle.html", thanos_only=thanos_only)

@app.route("/get_characters", methods=["GET"])
def get_characters():
    return jsonify([{
        "name": char.name,
        "health": char.health,
        "class": char.hero_class
    } for char in game.party])

@app.route("/attack", methods=["POST"])
def attack():
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 403

    user = User.query.get(session["user_id"])
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    char_name = data['character']
    attack_type = data['attack_type']

    # Find the character
    character = next((c for c in game.party if c.name == char_name), None)
    if not character:
        return jsonify({"error": "Character not found"}), 404

    # Select the first available enemy
    if not game.enemies:
        return jsonify({"message": "All enemies are defeated! Prepare for the next challenge."}), 200

    current_enemy = game.enemies[0]

    # Calculate damage dealt
    if attack_type == "special":
        damage_dealt = character.perform_special_move(current_enemy)
    else:
        chosen_stat = character.get_stats()[0]
        damage_dealt = character.basic_attack(chosen_stat, current_enemy)

    # Update Total HP (as total damage dealt)
    progress = json.loads(user.progress)
    total_hp = progress.get("total_hp", 0) + damage_dealt

    # Calculate new level
    level = 1 + total_hp // 100

    # Save updated progress
    progress["total_hp"] = total_hp
    progress["level"] = level
    user.progress = json.dumps(progress)
    db.session.commit()

    # Check if enemy is defeated
    if current_enemy['health'] <= 0:
        game.enemies.pop(0)  # Remove the defeated enemy
        if game.enemies:
            next_enemy = game.enemies[0]
            return jsonify({
                "message": f"You defeated {current_enemy['name']}! Next enemy: {next_enemy['name']}",
                "next_enemy": {
                    "name": next_enemy['name'],
                    "health": next_enemy['health']
                },
                "total_hp": total_hp,
                "level": level
            })
        else:
            return jsonify({"message": f"You defeated {current_enemy['name']}! All enemies are defeated!", "total_hp": total_hp, "level": level})

    return jsonify({
        "message": f"{character.name} attacked {current_enemy['name']}!",
        "enemy_health": current_enemy['health'],
        "character_health": character.health,
        "total_hp": total_hp,
        "level": level
    })

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Initialize database tables

    # Dynamically bind to PORT environment variable
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
