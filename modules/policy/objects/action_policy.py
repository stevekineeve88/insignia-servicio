from typing import Dict
from sk88_http_response.modules.http.interfaces.http_dict import HTTPDict
from modules.action.objects.action import Action


class ActionPolicy(HTTPDict):
    """ Object representing an action policy part of a role group policy
    """
    def __init__(self, action: Action, **kwargs):
        """ Constructor for ActionPolicy
        Args:
            action (Action):            Action object
            **kwargs:                   Action policy info
                id (int)                    - Action policy ID
                uuid (str)                  - Action policy UUID
        """
        self.__id: int = kwargs.get("id")
        self.__uuid: str = kwargs.get("uuid")
        self.__action: Action = action

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

    def get_action(self) -> Action:
        """ Get action
        Returns:
            Action
        """
        return self.__action

    def get_http_dict(self) -> Dict[str, any]:
        """ Get HTTP dict representation of action policy
        Returns:
            Dict[str, any]
        """
        return {
            "id": self.get_id(),
            "uuid": self.get_uuid(),
            "action": self.get_action().get_http_dict()
        }
