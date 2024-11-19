from flask import Flask, render_template, request, jsonify
from game_logic import Character, Game, Event, Location, UserInputParser
import random

app = Flask(__name__)

# Initialize characters and game logic
heroes = [
    Character("Iron Man"),
    Character("Captain America"),
    Character("Thor")
]
parser = UserInputParser()

# Create enemies and events
enemy1 = {
    'name': 'Loki',
    'health': 75,
    'attack': 'Deceptive Strike'
}

enemy2 = {
    'name': 'Ultron',
    'health': 150,
    'attack': 'Laser Beam'
}

thanos = Character("Thanos", health=500, attack_power=25, special_move=50)  # Final boss

# Event for Loki's defeat
event1 = Event({
    'primary_attribute': 'Strength',
    'success_message': 'You overpowered Loki!',
    'failure_message': 'Loki outsmarts you!',
    'partial_pass': {'message': 'Loki retreats, but he will return.'}
}, enemy=enemy1)

# Event for Ultron (added later)
event2 = Event({
    'primary_attribute': 'Intelligence',
    'success_message': 'You solved the puzzle!',
    'failure_message': 'The trap is triggered!',
    'partial_pass': {'message': 'You barely escape the trap.'}
}, enemy=enemy2)

# Location with Loki and Ultron
location1 = Location("Asgard Throne Room", [event1])
location2 = Location("Mystic Forest", [event2])
locations = [location1, location2]

game = Game(parser, heroes, locations)

# Flags for checking if Loki and Ultron are defeated
loki_defeated = False
ultron_defeated = False

@app.route('/')
def index():
    """Landing page with a button to go to battle.html"""
    return render_template('index.html')


@app.route('/battle')
def battle():
    """Main game page"""
    global loki_defeated, ultron_defeated

    # If Loki and Ultron are both defeated, set Thanos as the final enemy
    if loki_defeated and ultron_defeated:
        current_enemy = thanos
    elif not loki_defeated:
        current_enemy = enemy1  # Loki is the current enemy
    else:
        current_enemy = enemy2  # Ultron is the current enemy

    return render_template('battle.html', enemy=current_enemy)


@app.route('/get_characters', methods=['GET'])
def get_characters():
    """Get characters data"""
    return jsonify([{
        "name": char.name,
        "health": char.health,
        "class": char.hero_class
    } for char in game.party])


@app.route('/get_event', methods=['GET'])
def get_event():
    """Get a random event from a location"""
    event = random.choice(game.locations).get_event()
    game.current_event = event
    return jsonify({
        "prompt_text": event.prompt_text,
        "enemy": event.enemy.name if event.enemy else None,
        "enemy_health": event.enemy.health if event.enemy else None
    })


@app.route('/attack', methods=['POST'])
def attack():
    """Handle character attacks"""
    global loki_defeated, ultron_defeated
    data = request.json
    char_name = data['character']
    attack_type = data['attack_type']
    
    character = next((c for c in game.party if c.name == char_name), None)
    if not character:
        return jsonify({"error": "Character not found"}), 404

    # Determine the current enemy (Loki, Ultron, or Thanos)
    current_enemy = None
    if not loki_defeated:
        current_enemy = enemy1  # Loki is the current enemy
    elif not ultron_defeated:
        current_enemy = enemy2  # Ultron is the current enemy
    else:
        current_enemy = thanos  # Thanos is the current enemy

    if attack_type == "special":
        character.special_move(current_enemy)
    else:
        chosen_stat = character.get_stats()[0]
        character.basic_attack(chosen_stat, current_enemy)

    # Check if enemy is defeated
    if current_enemy['health'] <= 0:
        if current_enemy == enemy1:
            loki_defeated = True
        elif current_enemy == enemy2:
            ultron_defeated = True
        elif current_enemy == thanos:
            return jsonify({"message": "You have defeated Thanos! Victory!"})

    # Enemy's counter-attack
    current_enemy['health'] -= 10  # Simple counter-attack for now (adjust as needed)
    
    return jsonify({
        "message": f"{character.name} attacked {current_enemy['name']}!",
        "enemy_health": current_enemy['health'],
        "character_health": character.health
    })


if __name__ == '__main__':
    app.run(debug=True)
