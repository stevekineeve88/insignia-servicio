from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from mysql_data_manager.modules.connection.objects.result import Result


class ActionData:
    """ Data layer for action data
    """
    def __init__(self, **kwargs):
        """ Constructor for ActionData
        Args:
            **kwargs:       Dependencies
                connection_manager (ConnectionManager)      - Connection manager
        """
        self.__connection_manager: ConnectionManager = kwargs.get("connection_manager")

    def insert(self, const: str, description: str) -> Result:
        """ Insert action
        Args:
            const (str):            Action const
            description (str):      Action description
        Returns:
            Result
        """
        return self.__connection_manager.insert(f"""
            INSERT INTO action (const, description)
            VALUES (%(const)s, %(description)s)
        """, {
            "const": const,
            "description": description
        })

    def delete(self, action_id: int) -> Result:
        """ Delete action
        Args:
            action_id (int):            Action ID
        Returns:
            Result
        """
        return self.__connection_manager.query(f"""
            DELETE FROM action WHERE id = %(id)s
        """, {
            "id": action_id
        })

    def search(self, **kwargs) -> Result:
        """ Search actions
        Args:
            **kwargs:       Search params
                search (str)                - Search string
                limit (int)                 - Limit of search
                offset (int)                - Offset of search
        Returns:
            Result
        """
        return self.__connection_manager.select(f"""
            SELECT
                action.id,
                action.const,
                action.description
            FROM action
            {self.__build_search_query()}
            ORDER BY action.const ASC
            LIMIT %(limit)s OFFSET %(offset)s
        """, {
            "search": f"%{kwargs.get('search')}%",
            "limit": kwargs.get("limit"),
            "offset": kwargs.get("offset")
        })

    def search_count(self, search: str) -> Result:
        """ Get search count for action search
        Args:
            search (str):        Search string
        Returns:
            Result
        """
        return self.__connection_manager.select(f"""
            SELECT
                COUNT(*) AS count
            FROM action
            {self.__build_search_query()}
        """, {
            "search": f"%{search}%"
        })

    @classmethod
    def __build_search_query(cls) -> str:
        """ Build search query for actions
        Returns:
            str
        """
        return f"""
            WHERE action.const LIKE %(search)s
                OR action.description LIKE %(search)s
        """
