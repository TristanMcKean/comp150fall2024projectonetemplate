import random
import json
from typing import List
from enum import Enum
from database import db


class EventStatus(Enum):
    UNKNOWN = "unknown"
    PASS = "pass"
    FAIL = "fail"
    PARTIAL_PASS = "partial_pass"


class Statistic:
    def __init__(self, name: str, value: int = 0):
        self.name = name
        self.value = value


class Location:
    def __init__(self, description, events=None):
        """
        Initializes a location.
        :param description: A brief description of the location.
        :param events: A list of events associated with this location.
        """
        self.description = description
        self.events = events if events else []

    def get_event(self):
        """Return a random event from this location."""
        return random.choice(self.events)


class Enemy:
    def __init__(self, name: str, health: int, strength: int):
        self.name = name
        self.health = health
        self.strength = strength

    def is_alive(self):
        """Check if the enemy is alive."""
        return self.health > 0


class Character:
    def __init__(self, name: str, health: int = 100, attack_power=1, special_move=None):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.special_move = special_move
        self.hero_class = "Hero"
        self.inventory = []

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
        elif name == "Thanos":  # Add special moves for Thanos
            self.hero_class = "Titan"
            self.strength = Statistic("Strength", 50)
            self.intelligence = Statistic("Intelligence", 40)
            self.special_move = special_move if special_move else "Snap"

    def get_stats(self):
        """Return the character's primary stats."""
        if self.name == "Captain America":
            return [self.strength, self.endurance]
        elif self.name == "Thor":
            return [self.strength, self.magic]
        elif self.name == "Thanos":
            return [self.strength, self.intelligence]
        else:
            return [self.strength, self.intelligence]

    def is_alive(self):
        """Check if the character is alive."""
        return self.health > 0

    def basic_attack(self, stat, target):
        """Perform a basic attack using a given stat."""
        damage = stat.value + self.attack_power
        target.health -= damage
        print(f"{self.name} attacks {target.name} for {damage} damage!")

    def perform_special_move(self, target):
        """Perform a special move."""
        if not target.is_alive():
            print(f"{target.name} is already defeated!")
            return
        damage = self.attack_power * 2
        target.health -= damage
        print(f"{self.name} uses a special move on {target.name} for {damage} damage!")

    def use_item(self, item: str):
        """Use an item from the inventory."""
        if item in self.inventory:
            print(f"{self.name} uses {item}.")
            self.inventory.remove(item)


class Game:
    def __init__(self, parser, heroes, locations, user=None):
        self.parser = parser
        self.party = heroes
        self.locations = locations
        self.user = user
        self.current_event = None
        self.load_progress()

    def load_progress(self):
        """Load the user's progress into the game state."""
        if self.user and self.user.progress:
            try:
                progress = json.loads(self.user.progress)
                for hero_name, stats in progress.get("heroes", {}).items():
                    character = next((c for c in self.party if c.name == hero_name), None)
                    if character:
                        character.health = stats.get("health", character.health)
                        character.inventory = stats.get("inventory", [])
                print("Progress loaded successfully!")
            except (json.JSONDecodeError, KeyError):
                print("Failed to load progress; starting fresh.")

    def save_progress(self):
        """Save the current game state to the user's progress."""
        if self.user:
            progress = {
                "heroes": {
                    hero.name: {
                        "health": hero.health,
                        "inventory": hero.inventory
                    }
                    for hero in self.party
                }
            }
            self.user.progress = json.dumps(progress)
            db.session.commit()
            print("Progress saved successfully!")

    def explore_location(self):
        """Explore a random location and trigger its event."""
        location = random.choice(self.locations)
        print(f"Exploring: {location.description}")
        event = location.get_event()
        self.current_event = event
        print(f"Event Triggered: {event.description}")
        return event

    def check_game_over(self):
        """Check if all heroes are defeated."""
        if all(not hero.is_alive() for hero in self.party):
            print("\n🛑 Your heroes have fallen. The world is lost...")
            self.save_progress()
            return True
        return False


class Event:
    def __init__(self, data, enemy=None):
        """
        Initializes an event.
        :param data: A dictionary containing event details.
        :param enemy: The enemy associated with the event (optional).
        """
        self.primary_attribute = data.get('primary_attribute')
        self.success_message = data.get('success_message')
        self.failure_message = data.get('failure_message')
        self.partial_pass_message = data.get('partial_pass', {}).get('message', "")
        self.enemy = enemy

    def trigger(self):
        """Simulate the event and return the outcome."""
        print(f"Event Triggered: {self.primary_attribute}")
        if self.enemy:
            print(f"Enemy Encountered: {self.enemy['name']} with {self.enemy['health']} health")
        return {
            "status": EventStatus.PASS if not self.enemy else EventStatus.UNKNOWN,
            "enemy": self.enemy
        }


class FinalBoss(Character):
    def __init__(self, name, health, special_moves):
        super().__init__(name, health)
        self.special_moves = special_moves

    def attack(self):
        """Choose a random special move to attack."""
        move = random.choice(self.special_moves)
        print(f"{self.name} uses {move}!")
        return move


class UserInputParser:
    @staticmethod
    def get_user_input(prompt):
        """Get input from the user."""
        return input(prompt)

    @staticmethod
    def parse_input(user_input):
        """Parse the input to determine the action."""
        return user_input.strip().lower()