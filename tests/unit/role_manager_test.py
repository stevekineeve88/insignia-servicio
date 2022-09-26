import unittest
from unittest.mock import patch, MagicMock
from mysql_data_manager.modules.connection.objects.result import Result
from modules.role.data.role_data import RoleData
from modules.role.exceptions.role_const_syntax_exception import RoleConstSyntaxException
from modules.role.exceptions.role_create_exception import RoleCreateException
from modules.role.managers.role_manager import RoleManager


class RoleManagerTest(unittest.TestCase):
    @patch("modules.role.data.role_data.RoleData")
    def setUp(self, role_data: RoleData) -> None:
        self.role_data = role_data
        self.role_manager: RoleManager = RoleManager(
            role_data=self.role_data
        )

    def test_create_fails_on_invalid_symbol(self):
        self.role_data.insert = MagicMock(return_value=Result(True))
        with self.assertRaises(RoleConstSyntaxException):
            self.role_manager.create("ROLE_$#%DF", "Description")
            self.fail("Did not fail on invalid symbols in const for creating role")
        self.role_data.insert.assert_not_called()

    def test_create_fails_on_lowercase_letters(self):
        self.role_data.insert = MagicMock(return_value=Result(True))
        with self.assertRaises(RoleConstSyntaxException):
            self.role_manager.create("RoLE", "Description")
            self.fail("Did not fail on lower case letters in const for creating role")
        self.role_data.insert.assert_not_called()

    def test_create_fails_on_create_exception(self):
        self.role_data.insert = MagicMock(return_value=Result(False))
        with self.assertRaises(RoleCreateException):
            self.role_manager.create("ROLE", "Description")
            self.fail("Did not fail create exception for creating role")
        self.role_data.insert.assert_called_once()

    def test_search_defaults_limit_if_over_100(self):
        self.role_data.search = MagicMock(return_value=Result(True))

        params = {
            "search": "something",
            "limit": 101,
            "offset": 0
        }

        self.role_manager.search(**params)
        self.role_data.search.assert_called_once_with(
            search=params["search"],
            limit=10,
            offset=params["offset"]
        )

    def test_search_defaults_limit_if_under_0(self):
        self.role_data.search = MagicMock(return_value=Result(True))

        params = {
            "search": "something",
            "limit": -1,
            "offset": 0
        }

        self.role_manager.search(**params)
        self.role_data.search.assert_called_once_with(
            search=params["search"],
            limit=10,
            offset=params["offset"]
        )

    def test_search_defaults_offset_if_under_0(self):
        self.role_data.search = MagicMock(return_value=Result(True))

        params = {
            "search": "something",
            "limit": 20,
            "offset": -1
        }

        self.role_manager.search(**params)
        self.role_data.search.assert_called_once_with(
            search=params["search"],
            limit=params["limit"],
            offset=0
        )
