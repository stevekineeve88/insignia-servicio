from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from mysql_data_manager.modules.connection.objects.result import Result


class RoleGroupData:
    """ Data layer for role group database operations
    """
    def __init__(self, **kwargs):
        """ Constructor for RoleGroupData
        Args:
            **kwargs:       Dependencies
                connection_manager (ConnectionManager)          - Connection Manager
        """
        self.__connection_manager: ConnectionManager = kwargs.get("connection_manager")

    def insert(self, const: str, description: str) -> Result:
        """ Insert role group
        Args:
            const (str):            Role group const
            description (str):      Role group description
        Returns:
            Result
        """
        return self.__connection_manager.insert(f"""
            INSERT INTO role_group (const, description)
            VALUES (%(const)s, %(description)s)
        """, {
            "const": const,
            "description": description
        })

    def load_by_id(self, role_group_id: int) -> Result:
        """ Load by ID
        Args:
            role_group_id (int):            Role group ID
        Returns:
            Result
        """
        return self.__connection_manager.select(f"""
            SELECT
                role_group.id,
                bin_to_uuid(role_group.uuid) as uuid,
                role_group.const,
                role_group.description
            FROM role_group
            WHERE role_group.id = %(id)s
        """, {
            "id": role_group_id
        })

    def delete(self, role_group_id: int) -> Result:
        """ Delete role group
        Args:
            role_group_id (int):            Role group ID
        Returns:
            Result
        """
        return self.__connection_manager.query(f"""
            DELETE FROM role_group WHERE id = %(id)s
        """, {
            "id": role_group_id
        })

    def search(self, **kwargs) -> Result:
        """ Search role groups
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
                role_group.id,
                bin_to_uuid(role_group.uuid) as uuid,
                role_group.const,
                role_group.description
            FROM role_group
            {self.__build_search_query()}
            ORDER BY role_group.const ASC
            LIMIT %(limit)s OFFSET %(offset)s
        """, {
            "search": f"%{kwargs.get('search')}%",
            "limit": kwargs.get("limit"),
            "offset": kwargs.get("offset")
        })

    def search_count(self, search: str) -> Result:
        """ Get search count for role group search
        Args:
            search (str):        Search string
        Returns:
            Result
        """
        return self.__connection_manager.select(f"""
            SELECT
                COUNT(*) AS count
            FROM role_group
            {self.__build_search_query()}
        """, {
            "search": f"%{search}%"
        })

    @classmethod
    def __build_search_query(cls) -> str:
        """ Build search query for role group
        Returns:
            str
        """
        return f"""
            WHERE role_group.const LIKE %(search)s
                OR role_group.description LIKE %(search)s
        """
