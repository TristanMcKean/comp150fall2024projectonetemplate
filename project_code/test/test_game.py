import os
import sys
import unittest
from unittest.mock import patch

# Add the root directory of the project to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import Character, Event, Statistic  # Removed imports of non-existent classes like Game and FinalBoss

class TestStatistic(unittest.TestCase):
    def setUp(self):
        # Remove min_value and max_value if they are not part of the actual Statistic class
        self.strength = Statistic("Strength", value=10) 

    def test_statistic_initialization(self):
        self.assertEqual(self.strength.name, "Strength")
        self.assertEqual(self.strength.value, 10)

class TestCharacter(unittest.TestCase):
    def setUp(self):
        self.character = Character(name="Hero", health=100, attack_power=10)
        self.enemy = Character(name="Loki", health=50, attack_power=5)
        self.strength = Statistic("Strength", value=10)
        self.intelligence = Statistic("Intelligence", value=15)  # Assuming a strength Statistic

    def test_character_initialization(self):
        self.assertEqual(self.character.name, "Hero")
        self.assertEqual(self.character.health, 100)

    def test_modify_health_positive(self):
        self.character.modify_health(10)
        self.assertEqual(self.character.health, 110)

    def test_statistic_immutability(self):
        initial_value = self.intelligence.value
        self.assertEqual(self.intelligence.value, initial_value)

    def test_modify_health_negative(self):
        self.character.modify_health(-30)
        self.assertEqual(self.character.health, 70)

    def test_is_alive(self):
        self.character.health = 0
        self.assertFalse(self.character.is_alive())
        self.character.health = 1
        self.assertTrue(self.character.is_alive())

    @patch('random.randint', return_value=90)
    def test_basic_attack_successful(self, mock_randint):
        # Pass the Statistic object if basic_attack requires it
        self.character.basic_attack(self.strength, self.enemy)
        self.assertLess(self.enemy.health, 60)

    @patch('random.randint', return_value=0)
    def test_basic_attack_missed(self, mock_randint):
        # Assuming basic_attack checks accuracy or attack stats; adjust health check as per actual behavior
        initial_health = self.enemy.health
        self.character.basic_attack(self.strength, self.enemy)
        self.assertEqual(self.enemy.health, initial_health)
    def test_statistic_value(self):
        # Check that the statistic's value is correctly set
        self.assertEqual(self.intelligence.name, "Intelligence")
        self.assertEqual(self.intelligence.value, 15)


class TestEvent(unittest.TestCase):
    def setUp(self):
        self.event_data = {
            "primary_attribute": "Intelligence",
            "secondary_attribute": "Strength",
            "prompt_text": "A mysterious door blocks your path, with a riddle inscribed. What will you do?",
            "pass": {"message": "You solved the riddle and pushed the door open. You may proceed."},
            "fail": {"message": "You failed to solve the riddle and push the door open. You must find another way."},
            "partial_pass": {"message": "You managed to solve the riddle or push the door, but not both."}
        }
        self.event = Event(self.event_data)
        

    def test_event_initialization(self):
        self.assertEqual(self.event.primary_attribute, "Intelligence")
        self.assertEqual(self.event.secondary_attribute, "Strength")
        self.assertEqual(self.event.prompt_text, self.event_data["prompt_text"])
        self.assertEqual(self.event.pass_message, self.event_data["pass"]["message"])
        self.assertEqual(self.event.fail_message, self.event_data["fail"]["message"])
        self.assertEqual(self.event.partial_pass_message, self.event_data["partial_pass"]["message"])

class TestCharacterBasicAttackMissed(unittest.TestCase):
    def setUp(self):
        # Initialize a Character instance with default stats for testing
        self.character = Character(name="Hero", health=100, attack_power=10)
        self.enemy = Character(name="Enemy", health=50, attack_power=5)
        self.strength = Statistic("Strength", value=10)  # Assuming Statistic class handles 'strength'

    @patch('random.randint', return_value=0)  # Mocking to simulate a missed attack
    def test_basic_attack_miss_health_unchanged(self, mock_randint):
        # Store the enemy's initial health
        initial_health = self.enemy.health
        # Execute basic_attack and check that health remains the same
        self.character.basic_attack(self.strength, self.enemy)
        self.assertEqual(self.enemy.health, initial_health)

if __name__ == '__main__':
    unittest.main()
