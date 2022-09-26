from typing import List
from modules.action.objects.action import Action


class ActionSearchResult:
    """ Object for representing action search result
    """
    def __init__(self, actions: List[Action], total_count: int):
        """ Constructor for ActionSearchResult
        Args:
            actions (List[Action]):         Action search list
            total_count (int):              Total count
        """
        self.__actions: List[Action] = actions
        self.__total_count: int = total_count

    def get_actions(self) -> List[Action]:
        """ Get actions
        Returns:
            List[Action]
        """
        return self.__actions

    def get_total_count(self) -> int:
        """ Get total count
        Returns:
            int
        """
        return self.__total_count
