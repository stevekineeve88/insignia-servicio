from typing import List
from modules.role.objects.role_group import RoleGroup


class RoleGroupSearchResult:
    """ Object for representing role group search result
    """
    def __init__(self, role_groups: List[RoleGroup], total_count: int):
        """ Constructor for RoleGroupSearchResult
        Args:
            role_groups (List[RoleGroup]):         Role group search list
            total_count (int):                     Total count
        """
        self.__role_groups: List[RoleGroup] = role_groups
        self.__total_count: int = total_count

    def get_role_groups(self) -> List[RoleGroup]:
        """ Get role groups
        Returns:
            List[RoleGroup]
        """
        return self.__role_groups

    def get_total_count(self) -> int:
        """ Get total count
        Returns:
            int
        """
        return self.__total_count
