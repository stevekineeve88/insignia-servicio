class Action:
    """ Object representing an action
    """
    def __init__(self, action_id: int, const: str, description: str):
        """ Constructor for Action
        Args:
            action_id (int):            Action ID
            const (str):                Action constant
            description (str):          Action description
        """
        self.__id: int = action_id
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
