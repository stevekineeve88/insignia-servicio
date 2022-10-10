from typing import Dict

from sk88_http_response.modules.http.interfaces.http_dict import HTTPDict


class RoleGroup(HTTPDict):
    """ Object representing role group
    """
    def __init__(self, **kwargs):
        """ Constructor for RoleGroup
        Args:
            kwargs:            Role group info
        """
        self.__id: int = kwargs.get("id")
        self.__uuid: str = kwargs.get("uuid")
        self.__const: str = kwargs.get("const")
        self.__description: str = kwargs.get("description")

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

    def get_const(self) -> str:
        """ Get constant
        Returns:
            str
        """
        return self.__const

    def get_description(self) -> str:
        """ Get description
        Returns:
            str
        """
        return self.__description

    def get_http_dict(self) -> Dict[str, any]:
        """ Get HTTP dict representation of role group
        Returns:
            Dict[str, any]
        """
        return {
            "id": self.get_id(),
            "uuid": self.get_uuid(),
            "const": self.get_const(),
            "description": self.get_description()
        }
