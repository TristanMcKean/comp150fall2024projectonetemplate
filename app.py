from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for the battle page
@app.route('/battle')
def battle():
    return render_template('battle.html')

if __name__ == '__main__':
    app.run(debug=True)

# app.py
from flask import Flask, request, jsonify
from game_logic import Character, Game

app = Flask(__name__)

# Initialize characters and game
characters = [
    Character("Iron Man"),
    Character("Captain America"),
    Character("Thor")
]
game = Game(characters)

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

if __name__ == '__main__':
    app.run(debug=True)

