from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from mysql_data_manager.modules.connection.objects.result import Result


class RoleGroupPolicyData:
    """ Data layer for role group policy database operations
    """
    def __init__(self, **kwargs):
        """ Constructor for RoleGroupPolicyData
        Args:
            **kwargs:           Dependencies
                connection_manager (ConnectionManager)      - Connection manager
        """
        self.__connection_manager: ConnectionManager = kwargs.get("connection_manager")

    def add_role(self, role_group_id: int, role_id: int) -> Result:
        """ Add role to role group policy
        Args:
            role_group_id (int):            Role group ID
            role_id (int):                  Role ID
        Returns:
            Result
        """
        return self.__connection_manager.insert(f"""
            INSERT INTO role_group_role (role_group_id, role_id)
            VALUES (%(role_group_id)s, %(role_id)s)
        """, {
            "role_group_id": role_group_id,
            "role_id": role_id
        })

    def delete_role(self, role_group_role_id: int) -> Result:
        """ Delete role from role group policy
        Args:
            role_group_role_id (int):           Role group role ID
        Returns:
            Result
        """
        return self.__connection_manager.query(f"""
            DELETE FROM role_group_role WHERE id = %(id)s
        """, {
            "id": role_group_role_id
        })

    def add_action(self, role_group_role_id: int, action_id: int) -> Result:
        """ Add action to role in role group policy
        Args:
            role_group_role_id (int):               Role group role ID
            action_id (int):                        Action ID
        Returns:
            Result
        """
        return self.__connection_manager.insert(f"""
            INSERT INTO role_group_role_action (role_group_role_id, action_id)
            VALUES (%(role_group_role_id)s, %(action_id)s)
        """, {
            "role_group_role_id": role_group_role_id,
            "action_id": action_id
        })

    def delete_action(self, role_group_role_action_id: int) -> Result:
        """ Delete action from role in role group policy
        Args:
            role_group_role_action_id (int):            Role group role action ID
        Returns:
            Result
        """
        return self.__connection_manager.query(f"""
            DELETE FROM role_group_role_action WHERE id = %(id)s
        """, {
            "id": role_group_role_action_id
        })

    def load_by_role_group_id(self, role_group_id) -> Result:
        """ Load role group policy by role group ID
        Args:
            role_group_id:      Role group ID
        Returns:
            Result
        """
        return self.__connection_manager.select(f"""
            SELECT
                role_group.id AS role_group_id,
                role_group.const AS role_group_const,
                role_group.description AS role_group_description,
                bin_to_uuid(role_group.uuid) AS role_group_uuid,
                role_group_role.id AS role_group_role_id,
                bin_to_uuid(role_group_role.uuid) AS role_group_role_uuid,
                role.id AS role_id,
                role.const AS role_const,
                role.description AS role_description,
                role_group_role_action.id AS role_group_role_action_id,
                bin_to_uuid(role_group_role_action.uuid) AS role_group_role_action_uuid,
                action.id AS action_id,
                action.const AS action_const,
                action.description AS action_description
            FROM role_group
            INNER JOIN role_group_role ON role_group.id = role_group_role.role_group_id
            INNER JOIN role ON role.id = role_group_role.role_id
            LEFT JOIN role_group_role_action ON role_group_role.id = role_group_role_action.role_group_role_id
            LEFT JOIN action ON action.id = role_group_role_action.action_id
            WHERE role_group.id = %(id)s
        """, {
            "id": role_group_id
        })
