from flask import Flask, render_template, request, jsonify, session
from comp150fall2024projectonetemplate.project_code.src.models import db, User
import os
from comp150fall2024projectonetemplate.project_code.src.game_logic import Character, Game

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.secret_key = os.getenv("FLASK_SECRET_KEY")  # Required for session management
db.init_app(app)

# Initialize characters and game
characters = [
    Character("Iron Man"),
    Character("Captain America"),
    Character("Thor")
]
game = Game(characters)

# Ensure database tables are created
with app.app_context():
    db.create_all()


# Routes for the game
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/battle')
def battle():
    return render_template('battle.html')


@app.route('/get_characters', methods=['GET'])
def get_characters():
    return jsonify(game.get_party())


@app.route('/attack', methods=['POST'])
def attack():
    data = request.json
    char_name = data['character']
    attack_type = data['attack_type']

    character = next((c for c in characters if c.name == char_name), None)
    if not character:
        return jsonify({"error": "Character not found"}), 404

    # Attack logic here (simplified for the example)
    return jsonify({"message": f"{character.name} used {attack_type} attack!"})


# New route to save game progress
@app.route("/save_progress", methods=["POST"])
def save_progress():
    if "user_id" not in session:
        return jsonify({"error": "User not logged in"}), 403

    user = User.query.get(session["user_id"])
    user.game_progress = request.json.get("game_progress")
    db.session.commit()

    return jsonify({"message": "Progress saved successfully"})


# New route to load game progress
@app.route("/load_progress", methods=["GET"])
def load_progress():
    if "user_id" not in session:
        return jsonify({"error": "User not logged in"}), 403

    user = User.query.get(session["user_id"])
    return jsonify({"game_progress": user.game_progress})


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
