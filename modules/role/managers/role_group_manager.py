from typing import List, Dict
from modules.role.data.role_group_data import RoleGroupData
from modules.role.exceptions.role_group_const_syntax_exception import RoleGroupConstSyntaxException
from modules.role.exceptions.role_group_create_exception import RoleGroupCreateException
from modules.role.exceptions.role_group_delete_exception import RoleGroupDeleteException
from modules.role.exceptions.role_group_fetch_exception import RoleGroupFetchException
from modules.role.objects.role_group import RoleGroup
from modules.role.objects.role_group_search_result import RoleGroupSearchResult


class RoleGroupManager:
    """ Manager for role group objects
    """
    def __init__(self, **kwargs):
        """ Constructor for RoleGroupManager
        Args:
            **kwargs:           Dependencies
                role_group_data (RoleGroupData)         - Role group data layer
        """
        self.__role_group_data: RoleGroupData = kwargs.get("role_group_data")

    def create(self, const: str, description: str) -> RoleGroup:
        """ Create role group
        Args:
            const (str):        Role group constant
            description (str):  Role group description
        Returns:
            RoleGroup
        """
        self.__check_const(const)
        result = self.__role_group_data.insert(const, description)
        if not result.get_status():
            raise RoleGroupCreateException(f"Could not create role group: {result.get_message()}")
        return self.get_by_id(result.get_last_insert_id())

    def get_by_id(self, role_group_id: int) -> RoleGroup:
        """ Get by ID
        Args:
            role_group_id (int):            Role group ID
        Returns:
            RoleGroup
        """
        result = self.__role_group_data.load_by_id(role_group_id)
        if result.get_affected_rows() == 0:
            raise RoleGroupFetchException(f"Could not fetch role group with ID {role_group_id}")
        return RoleGroup(**result.get_data()[0])

    def delete(self, role_group_id: int):
        """ Delete role group
        Args:
            role_group_id (int):        Role group ID
        """
        result = self.__role_group_data.delete(role_group_id)
        if result.get_affected_rows() == 0:
            raise RoleGroupDeleteException(f"Could not delete role group with ID {role_group_id}")

    def search(self, **kwargs) -> RoleGroupSearchResult:
        """ Search role groups
        Args:
            **kwargs:       Search arguments
                search (str)        - [OPTIONAL] search string
                limit (int)         - [OPTIONAL] limit of result
                offset (int)        - [OPTIONAL] offset of result
        Returns:
            RoleGroupSearchResult
        """
        limit = kwargs.get("limit") or 100
        limit = limit if 100 >= limit > 0 else 10

        offset = kwargs.get("offset") or 0
        offset = offset if offset >= 0 else 0

        search = kwargs.get("search") or ""

        result = self.__role_group_data.search(
            search=search,
            limit=limit,
            offset=offset
        )
        if not result.get_status():
            raise RoleGroupFetchException(f"Could not search role groups: {result.get_message()}")

        data = result.get_data()
        role_groups: List[RoleGroup] = []
        for datum in data:
            role_groups.append(RoleGroup(**datum))

        result = self.__role_group_data.search_count(search)
        if not result.get_status():
            raise RoleGroupFetchException(f"Could not fetch role group count: {result.get_message()}")
        return RoleGroupSearchResult(role_groups, result.get_data()[0]["count"])

    @classmethod
    def __check_const(cls, const: str):
        """ Check role group constant for standard
        Args:
            const (str):        Constant to check
        """
        pieces = const.split("_")
        for piece in pieces:
            if not piece.isalpha() or piece.upper() != piece:
                raise RoleGroupConstSyntaxException(
                    "Constant definition must be capital snake case"
                )
