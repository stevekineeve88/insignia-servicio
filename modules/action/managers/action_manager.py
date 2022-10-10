from typing import List
from modules.action.data.action_data import ActionData
from modules.action.exceptions.action_const_syntax_exception import ActionConstSyntaxException
from modules.action.exceptions.action_create_exception import ActionCreateException
from modules.action.exceptions.action_delete_exception import ActionDeleteException
from modules.action.exceptions.action_fetch_exception import ActionFetchException
from modules.action.objects.action import Action
from modules.action.objects.action_search_result import ActionSearchResult


class ActionManager:
    """ Manager for action objects
    """
    def __init__(self, **kwargs):
        """ Constructor for ActionManager
        Args:
            **kwargs:       Dependencies
                action_data (ActionData)            - Action data layer
        """
        self.__action_data: ActionData = kwargs.get("action_data")

    def create(self, const: str, description: str) -> Action:
        """ Create action
        Args:
            const (str):        Action constant
            description (str):  Action description
        Returns:
            Action
        """
        self.__check_const(const)
        result = self.__action_data.insert(const, description)
        if not result.get_status():
            raise ActionCreateException(f"Could not create action: {result.get_message()}")
        return self.get_by_id(result.get_last_insert_id())

    def get_by_id(self, action_id: int) -> Action:
        """ Get action by ID
        Args:
            action_id (int):
        Returns:
            Action
        """
        result = self.__action_data.load_by_id(action_id)
        if result.get_affected_rows() == 0:
            raise ActionFetchException(f"Could not fetch action with ID {action_id}")
        return Action(**result.get_data()[0])

    def delete(self, action_uuid: str):
        """ Delete action
        Args:
            action_uuid (int):        Action ID
        """
        result = self.__action_data.delete(action_uuid)
        if result.get_affected_rows() == 0:
            raise ActionDeleteException(f"Could not delete action with UUID {action_uuid}")

    def search(self, **kwargs) -> ActionSearchResult:
        """ Search actions
        Args:
            **kwargs:       Search arguments
                search (str)        - [OPTIONAL] search string
                limit (int)         - [OPTIONAL] limit of result
                offset (int)        - [OPTIONAL] offset of result
        Returns:
            ActionSearchResult
        """
        limit = kwargs.get("limit") or 100
        limit = limit if 100 >= limit > 0 else 10

        offset = kwargs.get("offset") or 0
        offset = offset if offset >= 0 else 0

        search = kwargs.get("search") or ""

        result = self.__action_data.search(
            search=search,
            limit=limit,
            offset=offset
        )
        if not result.get_status():
            raise ActionFetchException(f"Could not search actions: {result.get_message()}")

        data = result.get_data()
        actions: List[Action] = []
        for datum in data:
            actions.append(Action(**datum))

        result = self.__action_data.search_count(search)
        if not result.get_status():
            raise ActionFetchException(f"Could not fetch action count: {result.get_message()}")
        return ActionSearchResult(actions, result.get_data()[0]["count"])

    @classmethod
    def __check_const(cls, const: str):
        """ Check action constant for standard
            Must match ENTITY:ACTION with ENTITY and ACTION as snake case capitalized
        Args:
            const (str):        Constant to check
        """
        if const.find(":") == -1:
            raise ActionConstSyntaxException("Constant definition must contain :")
        pieces = const.split(":")
        if len(pieces) != 2:
            raise ActionConstSyntaxException("Constant definition must be ENTITY:ACTION format")
        for piece in pieces:
            piece_split = piece.split("_")
            for item in piece_split:
                if not item.isalpha() or item.upper() != item:
                    raise ActionConstSyntaxException(
                        "Constant definition must be capital snake case for ENTITY and ACTION"
                    )
