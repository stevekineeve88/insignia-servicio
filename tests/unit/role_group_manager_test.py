import unittest
from unittest.mock import patch, MagicMock
from mysql_data_manager.modules.connection.objects.result import Result
from modules.role.data.role_group_data import RoleGroupData
from modules.role.exceptions.role_group_const_syntax_exception import RoleGroupConstSyntaxException
from modules.role.exceptions.role_group_create_exception import RoleGroupCreateException
from modules.role.managers.role_group_manager import RoleGroupManager


class RoleGroupManagerTest(unittest.TestCase):
    @patch("modules.role.data.role_group_data.RoleGroupData")
    def setUp(self, role_group_data: RoleGroupData) -> None:
        self.role_group_data = role_group_data
        self.role_group_manager: RoleGroupManager = RoleGroupManager(
            role_group_data=self.role_group_data
        )

    def test_create_fails_on_invalid_symbol(self):
        self.role_group_data.insert = MagicMock(return_value=Result(True))
        with self.assertRaises(RoleGroupConstSyntaxException):
            self.role_group_manager.create("ROLE_GROUP_$%$ET", "Description")
            self.fail("Did not fail on invalid symbols in const for creating role group")
        self.role_group_data.insert.assert_not_called()

    def test_create_fails_on_lowercase_letters(self):
        self.role_group_data.insert = MagicMock(return_value=Result(True))
        with self.assertRaises(RoleGroupConstSyntaxException):
            self.role_group_manager.create("RoLE", "Description")
            self.fail("Did not fail on lower case letters in const for creating role group")
        self.role_group_data.insert.assert_not_called()

    def test_create_fails_on_create_exception(self):
        self.role_group_data.insert = MagicMock(return_value=Result(False))
        with self.assertRaises(RoleGroupCreateException):
            self.role_group_manager.create("ROLE_GROUP", "Description")
            self.fail("Did not fail create exception for creating role group")
        self.role_group_data.insert.assert_called_once()

    def test_search_defaults_limit_if_over_100(self):
        self.role_group_data.search = MagicMock(return_value=Result(True))

        params = {
            "search": "something",
            "limit": 101,
            "offset": 0
        }

        self.role_group_manager.search(**params)
        self.role_group_data.search.assert_called_once_with(
            search=params["search"],
            limit=10,
            offset=params["offset"]
        )

    def test_search_defaults_limit_if_under_0(self):
        self.role_group_data.search = MagicMock(return_value=Result(True))

        params = {
            "search": "something",
            "limit": -1,
            "offset": 0
        }

        self.role_group_manager.search(**params)
        self.role_group_data.search.assert_called_once_with(
            search=params["search"],
            limit=10,
            offset=params["offset"]
        )

    def test_search_defaults_offset_if_under_0(self):
        self.role_group_data.search = MagicMock(return_value=Result(True))

        params = {
            "search": "something",
            "limit": 20,
            "offset": -1
        }

        self.role_group_manager.search(**params)
        self.role_group_data.search.assert_called_once_with(
            search=params["search"],
            limit=params["limit"],
            offset=0
        )
