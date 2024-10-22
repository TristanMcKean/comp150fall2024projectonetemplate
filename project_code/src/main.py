import json
import sys
import random
from typing import List
from enum import Enum


class EventStatus(Enum):
    UNKNOWN = "unknown"
    PASS = "pass"
    FAIL = "fail"
    PARTIAL_PASS = "partial_pass"


class Statistic:
    def __init__(self, name: str, hero_class: str, health: int = 0, attack_power: int = 0):
        self.name = name
        self.hero_class = hero_class
        self.health = health
        self.attack_power = attack_power
        self.inventory = []

    def __str__(self):
        return f"{self.name} ({self.hero_class}) - HP: {self.health}, AP: {self.attack_power}"

    def is_alive(self):
        return self.health > 0

    def attack(self, target: "Statistic"):
        print(f"Do you want to use {self.name}'s special move? (y/n)")
        use_special = input().strip().lower()
        if use_special == 'y':
            self.special_move(target)  # Call special move if chosen
        else:
            success_chance = random.randint(1, 100)
            if success_chance <= 70:
                damage = random.randint(1, self.attack_power)
                target.health -= damage
                print(f"{self.name} attacks {target.name} for {damage} damage!")
            else:
                print(f"{self.name}'s attack missed!")

    def special_move(self, target: "Statistic"):
        # Different special moves based on hero class
        if self.hero_class == "Genius":
            print(f"{self.name} uses Repulsor Blast!")
            success_chance = random.randint(1, 100)
            if success_chance <= 50:
                damage = random.randint(25, 50)
                target.health -= damage
                print(f"{self.name} hits {target.name} for {damage} damage with Repulsor Blast!")
        elif self.hero_class == "Asgardian":
            print(f"{self.name} uses Mjolnir Strike!")
            damage = random.randint(15, 40)
            target.health -= damage
            print(f"{self.name} hits {target.name} for {damage} damage with Mjolnir!")
        elif self.hero_class == "Super Soldier":
            print(f"{self.name} uses Shield Block!")
            self.health += 20
            print(f"{self.name} heals 20 HP with Shield Block!")
  
    def add_item(self, item: str):
        self.inventory.append(item)

    def use_item(self, item: str):
        if item in self.inventory:
            print(f"{self.name} uses {item}.")
            if item == "Vibranium Shield":
                self.health += 30  # Heals for 30 HP
                print(f"{self.name} heals for 30 HP with Vibranium Shield!")
            self.inventory.remove(item)

    def show_inventory(self):
        return self.inventory


class Character:
    def __init__(self, name: str):
        self.name = name
        # Adding Marvel heroes and their stats
        if name == "Iron Man":
            self.strength = Statistic("Strength", "Genius", health=100, attack_power=15)
            self.intelligence = Statistic("Intelligence", "Genius", health=100, attack_power=25)
        elif name == "Captain America":
            self.strength = Statistic("Strength", "Super Soldier", health=120, attack_power=20)
            self.endurance = Statistic("Endurance", "Super Soldier", health=120, attack_power=15)
        elif name == "Thor":
            self.strength = Statistic("Strength", "Asgardian", health=150, attack_power=30)
            self.magic = Statistic("Magic", "Asgardian", health=150, attack_power=25)
        else:
            # Default character if the name doesn't match
            self.strength = Statistic("Strength", "Hero", health=100, attack_power=10)
            self.intelligence = Statistic("Intelligence", "Hero", health=100, attack_power=10)

    def __str__(self):
        return f"Character: {self.name}, Strength: {self.strength}, Intelligence: {self.intelligence}"

    def get_stats(self):
        # Depending on the hero, there might be different stats
        if self.name == "Captain America":
            return [self.strength, self.endurance]
        elif self.name == "Thor":
            return [self.strength, self.magic]
        else:
            return [self.strength, self.intelligence]


class Enemy(Statistic):
    def __init__(self, name: str, health: int, attack_power: int):
        super().__init__(name, "Villain", health, attack_power)

    def attack(self, target: "Statistic"):
        success_chance = random.randint(1, 100)
        if success_chance <= 60:
            damage = random.randint(5, self.attack_power)
            target.health -= damage
            print(f"{self.name} attacks {target.name} for {damage} damage!")
        else:
            print(f"{self.name}'s attack missed!")


class Event:
    def __init__(self, data: dict):
        self.primary_attribute = data['primary_attribute']
        self.secondary_attribute = data['secondary_attribute']
        self.prompt_text = data['prompt_text']
        self.pass_message = data['pass']['message']
        self.fail_message = data['fail']['message']
        self.partial_pass_message = data['partial_pass']['message']
        self.status = EventStatus.UNKNOWN

    def execute(self, party: List[Character], parser):
        print(self.prompt_text)
        character = parser.select_party_member(party)
        chosen_stat = parser.select_stat(character)
        self.resolve_choice(character, chosen_stat)

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
            'prompt_text': 'Thanos has arrived! Can you stop him?',
            'pass': {'message': 'You defeat Thanos and save the universe!'},
            'fail': {'message': 'Thanos defeats you, and the universe falls into chaos!'},
            'partial_pass': {'message': 'You wound Thanos but he escapes for now.'}
        }) 


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

    def start(self):
        while self.continue_playing:
            location = random.choice(self.locations)
            event = location.get_event()
            event.execute(self.party, self.parser)
            if self.check_game_over():
                self.continue_playing = False
        print("Game Over.")

    def check_game_over(self):
    # Check if all party members are defeated
    if all(not member.is_alive() for member in self.party):
        print("Your party has been defeated. Game Over!")
        self.continue_playing = False
        return True  # Game over
    
    # If Thanos hasn't been defeated, trigger the final battle
    elif not self.defeated_thanos:
        print("Final Battle! Thanos has arrived!")
        thanos_battle = FinalBoss()
        thanos_battle.execute(self.party, self.parser)
        
        if thanos_battle.status == EventStatus.PASS:
            self.defeated_thanos = True
            print("Congratulations, you have defeated Thanos and won the game!")
            return True  # Game over with victory
        
        elif thanos_battle.status == EventStatus.FAIL:
            print("Thanos defeated your team. Game Over.")
            self.continue_playing = False
            return True  # Game over with defeat

    # Continue playing if none of the above conditions triggered a game over
    return False


class UserInputParser:
    def parse(self, prompt: str) -> str:
        return input(prompt)

    def select_party_member(self, party: List[Character]) -> Character:
        print("Choose a Marvel hero:")
        for idx, member in enumerate(party):
            print(f"{idx + 1}. {member.name}")
        choice = int(self.parse("Enter the number of the chosen hero: ")) - 1
        return party[choice]

    def select_stat(self, character: Character) -> Statistic:
        print(f"Choose a stat for {character.name}:")
        stats = character.get_stats()
        for idx, stat in enumerate(stats):
            print(f"{idx + 1}. {stat.name} (HP: {stat.health}, AP: {stat.attack_power})")
        choice = int(self.parse("Enter the number of the stat to use: ")) - 1
        return stats[choice]


def load_events_from_json(file_path: str) -> List[Event]:
    with open(file_path, 'r') as file:
        data = json.load(file)
    return [Event(event_data) for event_data in data]


def start_game():
    parser = UserInputParser()
    characters = [Character("Iron Man"), Character("Captain America"), Character("Thor")]

    # Load events from the JSON file
    events = load_events_from_json('project_code/location_events/location_1.json')

    locations = [Location(events)]
    game = Game(parser, characters, locations)
    game.start()


if __name__ == '__main__':
    start_game()
