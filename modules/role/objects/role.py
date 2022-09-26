class Role:
    """ Object representing role
    """
    def __init__(self, role_id: int, const: str, description: str):
        """ Constructor for Role
        Args:
            role_id (int):              Role ID
            const (str):                Role constant
            description (str):          Role description
        """
        self.__id: int = role_id
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
