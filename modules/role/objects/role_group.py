class RoleGroup:
    """ Object representing role group
    """
    def __init__(self, role_group_id: int, const: str, description: str):
        """ Constructor for RoleGroup
        Args:
            role_group_id (int):            Role group ID
            const (str):                    Role group constant
            description (str):              Role group description
        """
        self.__id: int = role_group_id
        self.__const: str = const
        self.__description: str = description

    def get_id(self) -> int:
        """ Get ID
        Returns:
            int
        """
        return self.__id

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
