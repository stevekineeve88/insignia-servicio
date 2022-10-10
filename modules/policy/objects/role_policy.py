from typing import List, Dict
from sk88_http_response.modules.http.interfaces.http_dict import HTTPDict
from modules.policy.objects.action_policy import ActionPolicy
from modules.role.objects.role import Role


class RolePolicy(HTTPDict):
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

    def get_http_dict(self) -> Dict[str, any]:
        """ Get HTTP dict representation of role policy
        Returns:
            Dict[str, any]
        """
        return {
            "id": self.get_id(),
            "uuid": self.get_uuid(),
            "role": self.get_role().get_http_dict(),
            "action_policies": [policy.get_http_dict() for policy in self.get_action_policies()]
        }
