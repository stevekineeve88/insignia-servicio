from typing import List
from modules.role.data.role_data import RoleData
from modules.role.exceptions.role_const_syntax_exception import RoleConstSyntaxException
from modules.role.exceptions.role_create_exception import RoleCreateException
from modules.role.exceptions.role_delete_exception import RoleDeleteException
from modules.role.exceptions.role_fetch_exception import RoleFetchException
from modules.role.objects.role import Role
from modules.role.objects.role_search_result import RoleSearchResult


class RoleManager:
    """ Manager for role objects
    """
    def __init__(self, **kwargs):
        """ Constructor for RoleManager
        Args:
            **kwargs:           Dependencies
                role_data (RoleData)            - Role data layer
        """
        self.__role_data: RoleData = kwargs.get("role_data")

    def create(self, const: str, description: str) -> Role:
        """ Create role
        Args:
            const (str):        Role constant
            description (str):  Role description
        Returns:
            Role
        """
        self.__check_const(const)
        result = self.__role_data.insert(const, description)
        if not result.get_status():
            raise RoleCreateException(f"Could not create role: {result.get_message()}")
        return Role(result.get_last_insert_id(), const, description)

    def delete(self, role_id: int):
        """ Delete role
        Args:
            role_id (int):        Role ID
        """
        result = self.__role_data.delete(role_id)
        if result.get_affected_rows() == 0:
            raise RoleDeleteException(f"Could not delete role with ID {role_id}")

    def search(self, **kwargs) -> RoleSearchResult:
        """ Search roles
        Args:
            **kwargs:       Search arguments
                search (str)        - [OPTIONAL] search string
                limit (int)         - [OPTIONAL] limit of result
                offset (int)        - [OPTIONAL] offset of result
        Returns:
            RoleSearchResult
        """
        limit = kwargs.get("limit") or 100
        limit = limit if 100 >= limit > 0 else 10

        offset = kwargs.get("offset") or 0
        offset = offset if offset >= 0 else 0

        search = kwargs.get("search") or ""

        result = self.__role_data.search(
            search=search,
            limit=limit,
            offset=offset
        )
        if not result.get_status():
            raise RoleFetchException(f"Could not search roles: {result.get_message()}")

        data = result.get_data()
        roles: List[Role] = []
        for datum in data:
            roles.append(Role(datum["id"], datum["const"], datum["description"]))

        result = self.__role_data.search_count(search)
        if not result.get_status():
            raise RoleFetchException(f"Could not fetch role count: {result.get_message()}")
        return RoleSearchResult(roles, result.get_data()[0]["count"])

    @classmethod
    def __check_const(cls, const: str):
        """ Check role constant for standard
        Args:
            const (str):        Constant to check
        """
        pieces = const.split("_")
        for piece in pieces:
            if not piece.isalpha() or piece.upper() != piece:
                raise RoleConstSyntaxException(
                    "Constant definition must be capital snake case"
                )
