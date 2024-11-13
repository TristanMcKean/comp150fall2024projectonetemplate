# game_logic.py
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

class Character:
    def __init__(self, name: str, health: int = 100, attack_power=1):
        self.name = name
        self.health = health
        self.attack_power = attack_power
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

    def get_stats(self):
        if self.name == "Captain America":
            return [self.strength, self.endurance]
        elif self.name == "Thor":
            return [self.strength, self.magic]
        else:
            return [self.strength, self.intelligence]

class Game:
    def __init__(self, characters: List[Character]):
        self.party = characters

    def get_party(self):
        return [{"name": char.name, "health": char.health, "hero_class": char.hero_class} for char in self.party]
