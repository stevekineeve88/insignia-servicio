from typing import List
from modules.role.objects.role import Role


class RoleSearchResult:
    """ Object for representing role search result
    """
    def __init__(self, roles: List[Role], total_count: int):
        """ Constructor for RoleSearchResult
        Args:
            roles (List[Role]):         Role search list
            total_count (int):          Total count
        """
        self.__roles: List[Role] = roles
        self.__total_count: int = total_count

    def get_roles(self) -> List[Role]:
        """ Get roles
        Returns:
            List[Role]
        """
        return self.__roles

    def get_total_count(self) -> int:
        """ Get total count
        Returns:
            int
        """
        return self.__total_count
