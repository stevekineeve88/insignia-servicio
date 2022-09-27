from typing import List
from modules.policy.objects.action_policy import ActionPolicy
from modules.role.objects.role import Role


class RolePolicy:
    """ Object representing role policy attached to a role group policy
    """
    def __init__(self, role: Role, action_policies: List[ActionPolicy], **kwargs):
        """ Constructor for RolePolicy
        Args:
            role (Role):                                Role object
            action_policies (List[ActionPolicy]):       List of action policies
            **kwargs:                                   Role policy info
                id (int)                                    - Role policy ID
                uuid (str)                                  - Role policy UUID
        """
        self.__id: int = kwargs.get("id")
        self.__uuid: str = kwargs.get("uuid")
        self.__role: Role = role
        self.__action_policies: List[ActionPolicy] = action_policies

    def get_id(self) -> int:
        """ Get ID
        Returns:
            int
        """
        return self.__id

    def get_uuid(self) -> str:
        """ Get UUID
        Returns:
            str
        """
        return self.__uuid

    def get_role(self) -> Role:
        """ Get role
        Returns:
            Role
        """
        return self.__role

    def get_action_policies(self) -> List[ActionPolicy]:
        """ Get action policies
        Returns:
            List[ActionPolicy]
        """
        return self.__action_policies

    def add_action_policy(self, action_policy: ActionPolicy):
        """ Add action policy
        Args:
            action_policy (ActionPolicy):       Action policy
        """
        self.__action_policies.append(action_policy)
