from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from mysql_data_manager.modules.connection.objects.result import Result


class RoleData:
    """ Data layer for role database operations
    """
    def __init__(self, **kwargs):
        """ Constructor for RoleData
        Args:
            **kwargs:       Dependencies
                connection_manager (ConnectionManager)          - Connection manager
        """
        self.__connection_manager: ConnectionManager = kwargs.get("connection_manager")

    def insert(self, const: str, description: str) -> Result:
        """ Insert role
        Args:
            const (str):            Role const
            description (str):      Role description
        Returns:
            Result
        """
        return self.__connection_manager.insert(f"""
            INSERT INTO role (const, description)
            VALUES (%(const)s, %(description)s)
        """, {
            "const": const,
            "description": description
        })

    def load_by_id(self, role_id: int) -> Result:
        """ Load role by ID
        Args:
            role_id (int):
        Returns:
            Result
        """
        return self.__connection_manager.select(f"""
            SELECT
                role.id,
                bin_to_uuid(role.uuid) as uuid,
                role.const,
                role.description
            FROM role
            WHERE role.id = %(id)s
        """, {
            "id": role_id
        })

    def delete(self, role_uuid: str) -> Result:
        """ Delete role
        Args:
            role_uuid (str):            Role UUID
        Returns:
            Result
        """
        return self.__connection_manager.query(f"""
            DELETE FROM role WHERE bin_to_uuid(uuid) = %(uuid)s
        """, {
            "uuid": role_uuid
        })

    def search(self, **kwargs) -> Result:
        """ Search roles
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
                role.id,
                bin_to_uuid(role.uuid) as uuid,
                role.const,
                role.description
            FROM role
            {self.__build_search_query()}
            ORDER BY role.const ASC
            LIMIT %(limit)s OFFSET %(offset)s
        """, {
            "search": f"%{kwargs.get('search')}%",
            "limit": kwargs.get("limit"),
            "offset": kwargs.get("offset")
        })

    def search_count(self, search: str) -> Result:
        """ Get search count for role search
        Args:
            search (str):        Search string
        Returns:
            Result
        """
        return self.__connection_manager.select(f"""
            SELECT
                COUNT(*) AS count
            FROM role
            {self.__build_search_query()}
        """, {
            "search": f"%{search}%"
        })

    @classmethod
    def __build_search_query(cls) -> str:
        """ Build search query for roles
        Returns:
            str
        """
        return f"""
            WHERE role.const LIKE %(search)s
                OR role.description LIKE %(search)s
        """
