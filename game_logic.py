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
    def __init__(self, parser: UserInputParser, characters: List[Character], locations: List[Location]):
        self.parser = parser
        self.party = characters
        self.locations = locations
        self.continue_playing = True
        self.defeated_thanos = False

    def get_party(self):
        return [{"name": char.name, "health": char.health, "hero_class": char.hero_class} for char in self.party]

class Event:
    def __init__(self, data: dict, enemy: Character = None):
        self.primary_attribute = data.get('primary_attribute')
        self.secondary_attribute = data.get('secondary_attribute')
        self.prompt_text = data.get('prompt_text')
        self.pass_message = data.get('pass', {}).get('message')
        self.fail_message = data.get('fail', {}).get('message')
        self.partial_pass_message = data.get('partial_pass', {}).get('message')
        self.status = EventStatus.UNKNOWN
        self.enemy = enemy

    def execute(self, party: List[Character], parser):
        # Logic for executing the event
        print(self.prompt_text)
        # Additional event handling logic can go here

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

class Location:
    def __init__(self, events: List[Event]):
        self.events = events

    def get_event(self) -> Event:
        return random.choice(self.events)