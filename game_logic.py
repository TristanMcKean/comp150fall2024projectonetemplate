import random
from typing import List
from enum import Enum

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

    def get_events(self):
        """Return the list of events associated with this location."""
        return self.events

class Character:
    def __init__(self, name: str, health: int = 100, attack_power=1, special_move=None):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.special_move = special_move
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
        elif name == "Thanos":  # Add special moves for Thanos
            self.hero_class = "Titan"
            self.strength = Statistic("Strength", 50)
            self.intelligence = Statistic("Intelligence", 40)
            self.special_move = special_move if special_move else "Snap"

    def get_stats(self):
        if self.name == "Captain America":
            return [self.strength, self.endurance]
        elif self.name == "Thor":
            return [self.strength, self.magic]
        elif self.name == "Thanos":
            return [self.strength, self.intelligence]
        else:
            return [self.strength, self.intelligence]


    def basic_attack(self, stat, target):
        damage = stat.value + self.attack_power
        target.health -= damage
        print(f"{self.name} attacks {target.name} for {damage} damage!")

    def special_move(self, target):
        damage = self.attack_power * 2
        target.health -= damage
        print(f"{self.name} uses a special move on {target.name} for {damage} damage!")

class Game:
    def __init__(self, parser, heroes, locations):
        self.parser = parser
        self.party = heroes
        self.locations = locations
        self.current_event = None
        self.loki_defeated = False
        self.ultron_defeated = False
        self.thanos_defeated = False

    def explore_location(self):
        # Explore a random location and trigger its event
        location = random.choice(self.locations)
        print(f"Exploring: {location.description}")
        event = location.get_event()
        self.current_event = event
        print(f"Event Triggered: {event.description}")
        if event.enemy:
            print(f"Enemy Encountered: {event.enemy['name']} with {event.enemy['health']} health")
        return event

    def get_current_enemy(self):
        if self.loki_defeated and self.ultron_defeated:
            return Thanos("Thanos", 500, ["Infinity Gauntlet", "Cosmic Power"])
        elif self.loki_defeated:
            return Ultron("Ultron", 150, ["Laser Beam"])
        else:
            return Loki("Loki", 75, ["Deceptive Strike"])

class Event:
    def __init__(self, description, outcome=None, enemy=None):
        """
        Initializes an event.
        :param description: A dictionary containing event details.
        :param outcome: The outcome of the event.
        :param enemy: The enemy associated with the event (optional).
        """
        self.description = description
        self.outcome = outcome
        self.enemy = enemy

    def trigger(self):
        """Simulate the event and return the outcome."""
        print(f"Event Triggered: {self.description}")
        if self.enemy:
            print(f"Enemy Encountered: {self.enemy.name} with {self.enemy.health} health")
        return self.outcome

class FinalBoss(Character):
    def __init__(self, name, health, special_moves):
        super().__init__(name, health)
        self.special_moves = special_moves

    def attack(self):
        """Choose a random special move to attack."""
        move = random.choice(self.special_moves)
        print(f"{self.name} uses {move}!")
        return move


class Loki(Character):
    def __init__(self, name, health, special_moves):
        super().__init__(name, health)
        self.special_moves = special_moves


class Ultron(Character):
    def __init__(self, name, health, special_moves):
        super().__init__(name, health)
        self.special_moves = special_moves


class UserInputParser:
    def __init__(self):
        pass

    @staticmethod
    def get_user_input(prompt):
        """Get input from the user."""
        return input(prompt)

    @staticmethod
    def parse_input(user_input):
        """Parse the input to determine the action."""
        return user_input.strip().lower()
