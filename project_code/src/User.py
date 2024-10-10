# User.py
from Game import Game


class User:

    def __init__(self, input, username: str, password: str, legacy_points: int = 0):
        self.username = username
        self.password = password
        self.legacy_points = legacy_points
        self.current_game = self._get_retrieve_saved_game_state_or_create_new_game()
        self.input = input

    def _get_retrieve_saved_game_state_or_create_new_game(self) -> Game:
        new_game = Game(self.input)
        return new_game

    def save_game(self):
        pass
