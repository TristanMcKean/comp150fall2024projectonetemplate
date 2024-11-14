import json
import os
import sys
import random
import auth
from statistics import StatisticsError
from typing import List
from enum import Enum
from flask import Flask, request, jsonify, redirect, session, url_for
from game_logic import Character, Event, UserInputParser, Game, Location


# Import your existing classes here
# from your_game_code import Character, Event, UserInputParser, FinalBoss, Game, Location

app = Flask(__name__)

# Initialize characters and game
characters = [
    Character("Iron Man"),
    Character("Captain America"),
    Character("Thor")
]
locations = [Location([Event({'primary_attribute': 'Strength',
            'secondary_attribute': 'Magic',
            'prompt_text': 'A powerful enemy appears. What will you do?',
            'pass': {'message': 'You successfully defeated the enemy!'},
            'fail': {'message': 'The enemy overpowered you.'},
            'partial_pass': {'message': 'You managed to escape, but the enemy is still out there.'}
                              })
                       ])
             ]
parser = UserInputParser()
game = Game(parser, characters, locations)

# API endpoint to get available characters
@app.route('/get_characters', methods=['GET'])
def get_characters():
    return jsonify([{"name": char.name, "health": char.health, "hero_class": char.hero_class} for char in characters])

# API endpoint to attack
@app.route('/attack', methods=['POST'])
def attack():
    data = request.json
    char_name = data['character']
    attack_type = data['attack_type']

    character = next((c for c in characters if c.name == char_name), None)
    if not character:
        return jsonify({"error": "Character not found"}), 404

    chosen_stat = character.get_stats()[0]
    enemy = game.locations[0].get_event().enemy
    character.attack(chosen_stat, attack_type, enemy)

    return jsonify({"message": f"{character.name} attacked {enemy.name}"})

if __name__ == '__main__':
    app.run(debug=True)

# Import for additional sections
# from flask import Flask, redirect, request, url_for, session
# import auth

app.secret_key = os.getenv("FLASK_SECRET_KEY")


@app.route("/login")
def login():
    google_auth_url = auth.get_google_auth_url()
    return redirect(google_auth_url)


@app.route("/callback")
def callback():
    code = request.args.get("code")
    user_info = auth.get_google_user_info(code)
    session['user'] = user_info
    return redirect(url_for("game"))


@app.route("/game")
def game():
    if 'user' not in session:
        return redirect(url_for("login"))
    return "Game Start!"

# Classes definitions start here
class EventStatus(Enum):
    UNKNOWN = "unknown"
    PASS = "pass"
    FAIL = "fail"
    PARTIAL_PASS = "partial_pass"


class Statistic:
    def __init__(self, name: str, value: int = 0):
        self.name = name
        self.value = value


class Character:
    def __init__(self, name: str, health: int = 100, attack_power=1):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.minimum_proc_chance = 70
        self.minimum_damage = 1
        self.inventory = []
        self.hero_class = "Hero"

        if name == "Iron Man":
            self.hero_class = "Genius"
            self.strength = Statistic("Strength", 15)
            self.intelligence = Statistic("Intelligence", 25)
        elif name == "Captain America":
            self.hero_class = "Super Soldier"
            self.strength = Statistic("Strength", 20)
            self.endurance = Statistic("Endurance", 15)
        elif name == "Thor":
            self.hero_class = "Asgardian"
            self.strength = Statistic("Strength", 30)
            self.magic = Statistic("Magic", 25)
        else:
            self.strength = Statistic("Strength", 10)
            self.intelligence = Statistic("Intelligence", 10)

    def __str__(self):
        return f"Character: {self.name}, Strength: {self.strength}, Intelligence: {self.intelligence}"

    def get_stats(self):
        if self.name == "Captain America":
            return [self.strength, self.endurance]
        elif self.name == "Thor":
            return [self.strength, self.magic]
        else:
            return [self.strength, self.intelligence]

    def is_alive(self):
        return self.health > 0

    def modify_health(self, amount):
        new_health = self.health + amount
        self.health = max(new_health, 0)

    def use_item(self, item: str):
        if item in self.inventory:
            print(f"{self.name} uses {item}.")
            if item == "Vibranium Shield":
                self.health += 30
                print(f"{self.name} heals for 30 HP with Vibranium Shield!")
                self.inventory.remove(item)

    def enemy_attack(self, target: "Character"):
        success_chance = random.randint(1, 100)
        if success_chance <= self.minimum_proc_chance:
            damage = random.randint(self.attack_power, self.attack_power * 2)
            print(f"\n🔥 {self.name} roars with fury and launches a powerful attack on {target.name}!")
            print(f"{self.name} strikes... ", end="")
            target.modify_health(-damage)
            print(f"and deals {damage} damage to {target.name}! 🩸")
        else:
            print(f"\n{self.name} swings wildly, but {target.name} skillfully dodges the attack! 🛡️")

    def attack(self, statistic, kind_of_attack, target):
        if kind_of_attack == "Special":
            self.special_move(target)
        else:
            self.basic_attack(statistic, target)

    def basic_attack(self, statistic: Statistic, target: "Character"):
        success_chance = random.randint(1, 100)
        if success_chance <= self.minimum_proc_chance:
            min_damage = min(statistic.value, self.attack_power)
            max_damage = max(statistic.value, self.attack_power)
            damage = random.randint(min_damage, max_damage)

            print(f"\n⚔️ {self.name} leaps into action, using their {statistic.name.lower()} to strike!")
            print(f"{self.name} swings with a mighty blow... ", end="")
            target.modify_health(-damage)
            print(f"and deals {damage} damage to {target.name}! 💥")
        else:
            print(f"\n{self.name} attacks with all their might... but the attack misses its mark! ❌")

    def special_move(self, target: "Character"):
        if self.hero_class == "Genius":
            print(f"\n🔋 {self.name} activates his suit's Repulsor Blast! Energy beams shoot towards {target.name}!")
            success_chance = random.randint(1, 100)
            if success_chance <= 50:
                damage = random.randint(25, 50)
                target.modify_health(-damage)
                print(f"{self.name}'s Repulsor Blast lands, dealing {damage} damage to {target.name}! ⚡️")
            else:
                print(f"{self.name}'s Repulsor Blast misses! {target.name} dodges just in time!")
        elif self.hero_class == "Asgardian":
            print(
                f"\n⚡️ {self.name} raises Mjolnir to the skies, summoning a storm. The hammer crashes down on {target.name}!")
            damage = random.randint(15, 40)
            target.modify_health(-damage)
            print(f"{self.name}'s Mjolnir strike lands with a thunderous boom, dealing {damage} damage! 🌩️")
        elif self.hero_class == "Super Soldier":
            print(f"\n🛡️ {self.name} raises his Vibranium Shield, blocking incoming attacks and fortifying himself.")
            self.health += 20
            print(f"{self.name} gains 20 HP, preparing for the next strike. 💪")

    def show_inventory(self):
        return self.inventory


class UserInputParser:
    def parse(self, prompt: str) -> str:
        return input(prompt)

    def select_party_member(self, party: List[Character]) -> Character:
        print("Choose a Marvel hero:")
        for idx, member in enumerate(party):
            print(f"{idx + 1}. {member.name}")

        while True:
            try:
                choice = int(self.parse("Enter the number of the chosen hero: ")) - 1
                if 0 <= choice < len(party):
                    return party[choice]
            except ValueError:
                pass
            print("Invalid choice. Please try again.")

    def select_stat(self, character: Character) -> Statistic:
        print(f"Select a stat for {character.name}:")
        stats = character.get_stats()
        for idx, stat in enumerate(stats):
            print(f"{idx + 1}. {stat.name}")

        while True:
            try:
                choice = int(self.parse("Enter the number of the chosen stat: ")) - 1
                if 0 <= choice < len(stats):
                    return stats[choice]
            except ValueError:
                pass
            print("Invalid choice. Please try again.")

    def what_kind_of_attack(self, character: Character) -> str:
        while True:
            print(f"Do you want to use {character.name}'s special move? (y/n)")
            use_special = input().strip().lower()
            if use_special in {'y', 'yes'}:
                return "Special"
            elif use_special in {'n', 'no'}:
                return "normal"


class Event:
    def __init__(self, data: dict, enemy: Character = None):
        self.primary_attribute = data['primary_attribute']
        self.secondary_attribute = data['secondary_attribute']
        self.prompt_text = data['prompt_text']
        self.pass_message = data['pass']['message']
        self.fail_message = data['fail']['message']
        self.partial_pass_message = data['partial_pass']['message']
        self.status = EventStatus.UNKNOWN
        self.enemy = enemy

    def execute(self, party: List[Character], parser):
        print(self.prompt_text)
        if self.enemy:
            print(f"An enemy {self.enemy.name} appears!")
            self.battle_with_enemy(party, parser)
        else:
            character = parser.select_party_member(party)
            chosen_stat = parser.select_stat(character)
            self.resolve_choice(character, chosen_stat)

    def battle_with_enemy(self, party: List[Character], parser: UserInputParser):
        while self.enemy.is_alive() and any(member.is_alive() for member in party):
            for member in party:
                if member.is_alive():
                    character = member
                    chosen_stat = parser.select_stat(character)
                    attack_kind = parser.what_kind_of_attack(character)
                    character.attack(chosen_stat, attack_kind, self.enemy)

                    if not self.enemy.is_alive():
                        print(f"\n⚔️ {self.enemy.name} has been defeated!")
                        self.status = EventStatus.PASS

                        if self.enemy.name == "Loki":
                            print(
                                "\n🔒 Loki falls to his knees, his illusions shattered. 'This isn't over, Avengers!' he hisses before disappearing in a flash of green light.")
                        elif self.enemy.name == "Ultron":
                            print(
                                "\n💥 Ultron's robotic shell crumbles to the ground. 'You think you've won, Avengers?' he crackles. 'I am everywhere...' But the lights in his eyes flicker and die.")
                        break

                if self.enemy.is_alive():
                    self.enemy.enemy_attack(member)

        if not any(member.is_alive() for member in party):
            print("\n💀 Your party has been defeated! The world falls into darkness.")
            self.status = EventStatus.FAIL

    def resolve_choice(self, character: Character, chosen_stat: Statistic):
        if chosen_stat.name == self.primary_attribute:
            self.status = EventStatus.PASS
            print(self.pass_message)
        elif chosen_stat.name == self.secondary_attribute:
            self.status = EventStatus.PARTIAL_PASS
            print(self.partial_pass_message)
        else:
            self.status = EventStatus.FAIL
            print(self.fail_message)


class FinalBoss(Event):
    def __init__(self):
        super().__init__({
            'primary_attribute': 'Strength',
            'secondary_attribute': 'Endurance',
            'prompt_text': '🌌 Thanos has arrived! Can you stop him before he claims all the Infinity Stones?',
            'pass': {'message': 'You defeated Thanos and saved the universe!'},
            'fail': {'message': 'Thanos defeats you, and the universe falls into chaos!'},
            'partial_pass': {'message': 'You wound Thanos, but he escapes, vowing to return.'}
        })
        self.enemy = Character("Thanos", health=100, attack_power=40)

    def execute(self, party: List[Character], parser):
        print(self.prompt_text)
        print("\n⚠️ The ground trembles as Thanos approaches. 'I am inevitable,' he declares.")
        print("The final battle begins!")

        while self.enemy.is_alive() and any(member.is_alive() for member in party):
            self.battle_with_enemy(party, parser)

        if self.enemy.is_alive():
            print("\n💀 Thanos raises the Infinity Gauntlet, and with a snap, your heroes fall one by one.")
            self.status = EventStatus.FAIL
            print(self.fail_message)
        else:
            print("\n🔥 Thanos collapses, his gauntlet slipping from his grasp.")
            print("As he fades into dust, the universe is safe once more... for now.")
            self.status = EventStatus.PASS
            print(self.pass_message)


class Location:
    def __init__(self, events: List[Event]):
        self.events = events

    def get_event(self) -> Event:
        return random.choice(self.events)


class Game:
    def __init__(self, parser, characters: List[Character], locations: List[Location]):
        self.parser = parser
        self.party = characters
        self.locations = locations
        self.continue_playing = True
        self.defeated_thanos = False

    def start(self):
        print("\n" + "=" * 50)
        print("🌌 Welcome to Marvel Heroes Adventure 🌌")
        print("=" * 50)
        print(
            "\nThe world is in peril. Dark forces are gathering, and powerful enemies are attacking cities across the globe.")
        print("Iron Man, Captain America, Thor, and other heroes have come together to protect humanity.")
        print("But the heroes know that these battles are just a prelude to a larger threat...")
        print(
            "Thanos, the Mad Titan, is on the horizon, seeking the Infinity Stones to reshape the universe to his twisted vision.")
        print("\nYour mission:")
        print("- Assemble your team of heroes")
        print("- Defeat the villains threatening each location")
        print("- Gather your strength for the final battle with Thanos")
        print("\nThe fate of the universe rests in your hands!")
        print("=" * 50 + "\n")

        while self.continue_playing:
            location = random.choice(self.locations)
            event = location.get_event()
            event.execute(self.party, self.parser)
            if self.check_game_over():
                self.continue_playing = False

        if self.defeated_thanos:
            print("\n🌟 Congratulations! You have saved the universe from Thanos' tyranny! 🌟")
        else:
            print("Game Over. Thanos proved too powerful, and darkness has fallen upon the universe.")

    def check_game_over(self):
        if all(not member.is_alive() for member in self.party):
            print("\n🛑 Your heroes have fallen. The world is lost...")
            self.continue_playing = False
            return True
        elif not self.defeated_thanos:
            print("\n🚨 Final Battle! Thanos has arrived, wielding the Infinity Gauntlet!")
            thanos_battle = FinalBoss()
            thanos_battle.execute(self.party, self.parser)

            if thanos_battle.status == EventStatus.PASS:
                self.defeated_thanos = True
                print("\n🎉 The Avengers stand victorious! The universe is safe from Thanos' tyranny.")
                return True
            elif thanos_battle.status == EventStatus.FAIL:
                print("\n💀 Thanos stands triumphant. Half of all life fades into dust...")
                self.continue_playing = False
                return True
        return False


def main():
    parser = UserInputParser()

    heroes = [
        Character("Iron Man"),
        Character("Captain America"),
        Character("Thor")
    ]

    enemy1 = Character("Loki", 50, 20)
    event1 = Event({
        'primary_attribute': 'Strength',
        'secondary_attribute': 'Magic',
        'prompt_text': 'Loki is causing chaos! What will you do?',
        'pass': {'message': 'You defeated Loki!'},
        'fail': {'message': 'Loki escapes!'},
        'partial_pass': {'message': 'You fought Loki, but he managed to escape!'}
    }, enemy=enemy1)

    enemy2 = Character("Ultron", 50, 25)
    event2 = Event({
        'primary_attribute': 'Intelligence',
        'secondary_attribute': 'Strength',
        'prompt_text': 'Ultron is attacking the city! What will you do?',
        'pass': {'message': 'You defeated Ultron!'},
        'fail': {'message': 'Ultron escapes!'},
        'partial_pass': {'message': 'You fought Ultron, but he managed to escape!'}
    }, enemy=enemy2)

    location1 = Location([event1])
    location2 = Location([event2])

    game = Game(parser, heroes, [location1, location2])
    game.start()

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render sets $PORT
    app.run(host="0.0.0.0", port=port)


