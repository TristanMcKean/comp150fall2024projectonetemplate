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
        print(self.prompt_text)
        if self.enemy:
            print(f"An enemy {self.enemy.name} appears!")
            self.battle_with_enemy(party, parser)
        else:
            character = parser.select_party_member(party)
            chosen_stat = parser.select_stat(character)
            self.resolve_choice(character, chosen_stat)

    def battle_with_enemy(self, party: List[Character], parser):
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

class Game:
    def __init__(self, parser: UserInputParser, characters: List[Character], locations: List[Location]):
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
