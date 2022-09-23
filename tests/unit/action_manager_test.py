import unittest
from unittest.mock import patch, MagicMock
from mysql_data_manager.modules.connection.objects.result import Result
from modules.action.data.action_data import ActionData
from modules.action.exceptions.action_const_syntax_exception import ActionConstSyntaxException
from modules.action.exceptions.action_create_exception import ActionCreateException
from modules.action.managers.action_manager import ActionManager


class ActionManagerTest(unittest.TestCase):
    @patch("modules.action.data.action_data.ActionData")
    def setUp(self, action_data: ActionData) -> None:
        self.action_data = action_data
        self.action_manager: ActionManager = ActionManager(
            action_data=self.action_data
        )

    def test_create_fails_on_missing_colon(self):
        self.action_data.insert = MagicMock(return_value=Result(True))
        with self.assertRaises(ActionConstSyntaxException):
            self.action_manager.create("ENTITY_NO_COLON", "Description")
            self.fail("Did not fail on missing colon in const for creating action")
        self.action_data.insert.assert_not_called()

    def test_create_fails_on_multiple_colons(self):
        self.action_data.insert = MagicMock(return_value=Result(True))
        with self.assertRaises(ActionConstSyntaxException):
            self.action_manager.create("ENTITY:ACTION:EXTRA", "Description")
            self.fail("Did not fail on extra colon in const for creating action")
        self.action_data.insert.assert_not_called()

    def test_create_fails_on_invalid_symbol(self):
        self.action_data.insert = MagicMock(return_value=Result(True))
        with self.assertRaises(ActionConstSyntaxException):
            self.action_manager.create("ENTITY_$#$:ACTION", "Description")
            self.fail("Did not fail on invalid symbols in const for creating action")
        self.action_data.insert.assert_not_called()

    def test_create_fails_on_lowercase_letters(self):
        self.action_data.insert = MagicMock(return_value=Result(True))
        with self.assertRaises(ActionConstSyntaxException):
            self.action_manager.create("ENTITY:ACtION", "Description")
            self.fail("Did not fail on lower case letters in const for creating action")
        self.action_data.insert.assert_not_called()

    def test_create_fails_on_create_exception(self):
        self.action_data.insert = MagicMock(return_value=Result(False))
        with self.assertRaises(ActionCreateException):
            self.action_manager.create("ENTITY:ACTION", "Description")
            self.fail("Did not fail create exception for creating action")
        self.action_data.insert.assert_called_once()

    def test_search_defaults_limit_if_over_100(self):
        self.action_data.search = MagicMock(return_value=Result(True))

        params = {
            "search": "something",
            "limit": 101,
            "offset": 0
        }

        self.action_manager.search(**params)
        self.action_data.search.assert_called_once_with(
            search=params["search"],
            limit=10,
            offset=params["offset"]
        )

    def test_search_defaults_limit_if_under_0(self):
        self.action_data.search = MagicMock(return_value=Result(True))

        params = {
            "search": "something",
            "limit": -1,
            "offset": 0
        }

        self.action_manager.search(**params)
        self.action_data.search.assert_called_once_with(
            search=params["search"],
            limit=10,
            offset=params["offset"]
        )

    def test_search_defaults_offset_if_under_0(self):
        self.action_data.search = MagicMock(return_value=Result(True))

        params = {
            "search": "something",
            "limit": 20,
            "offset": -1
        }

        self.action_manager.search(**params)
        self.action_data.search.assert_called_once_with(
            search=params["search"],
            limit=params["limit"],
            offset=0
        )
