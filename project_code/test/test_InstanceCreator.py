import unittest
from unittest.mock import MagicMock
from project_code.src.InstanceCreator import InstanceCreator
from project_code.src.UserFactory import UserFactory
from project_code.src.UserInputParser import UserInputParser
from project_code.src.User import User

class TestInstanceCreator(unittest.TestCase):
    def setUp(self):
        self.mock_user_factory = MagicMock(spec=UserFactory)
        self.mock_parser = MagicMock(spec=UserInputParser)
        self.instance_creator = InstanceCreator(self.mock_user_factory, self.mock_parser)

    def test_get_user_info_yes_creates_new_user(self):
        # Prepare the mock objects
        self.mock_parser.parse.return_value = "new"  # Simulate the response for creating a new user
        mock_user = MagicMock(spec=User)
        self.mock_user_factory.create_user.return_value = mock_user

        # Execute the method under test
        user = self.instance_creator.get_user_info("yes")

        # Verify the results
        self.mock_parser.parse.assert_called_once_with("Create a new username or login to an existing account?")
        self.mock_user_factory.create_user.assert_called_once_with(self.mock_parser)
        self.assertEqual(user, mock_user, "The method should return a new user object")

    def test_get_user_info_no_returns_none(self):
        # Execute the method under test with a response that should not create a user
        user = self.instance_creator.get_user_info("no")

        # Verify the results
        self.assertIsNone(user, "The method should return None for a 'no' response")

    # You can add more tests to cover other scenarios, such as handling login

if __name__ == '__main__':
    unittest.main()
