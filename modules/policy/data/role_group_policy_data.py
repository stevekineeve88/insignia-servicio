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

    def add_role(self, role_group_uuid: str, role_uuid: str) -> Result:
        """ Add role to role group policy
        Args:
            role_group_uuid (str):            Role group UUID
            role_uuid (str):                  Role UUID
        Returns:
            Result
        """
        return self.__connection_manager.insert(f"""
            INSERT INTO role_group_role (role_group_id, role_id)
            SELECT role_group.id, role.id FROM role_group, role
            WHERE bin_to_uuid(role_group.uuid) = %(role_group_uuid)s
            AND bin_to_uuid(role.uuid) = %(role_uuid)s
        """, {
            "role_group_uuid": role_group_uuid,
            "role_uuid": role_uuid
        })

    def load_role_policy_by_id(self, role_group_role_id: int) -> Result:
        """ Load role policy by ID
        Args:
            role_group_role_id (int):
        Returns:
            Result
        """
        return self.__connection_manager.select(f"""
            SELECT
                role_group_role.id AS role_group_role_id,
                bin_to_uuid(role_group_role.uuid) AS role_group_role_uuid,
                role_group_role.role_id AS role_id,
                bin_to_uuid(role.uuid) AS role_uuid,
                role.const AS role_const,
                role.description AS role_description
            FROM role_group_role
            INNER JOIN role ON role_group_role.role_id = role.id
            WHERE role_group_role.id = %(id)s
        """, {
            "id": role_group_role_id
        })

    def delete_role(self, role_group_role_uuid: str) -> Result:
        """ Delete role from role group policy
        Args:
            role_group_role_uuid (str):           Role group role UUID
        Returns:
            Result
        """
        return self.__connection_manager.query(f"""
            DELETE FROM role_group_role WHERE bin_to_uuid(role_group_role.uuid) = %(uuid)s
        """, {
            "uuid": role_group_role_uuid
        })

    def add_action(self, role_group_role_uuid: str, action_uuid: str) -> Result:
        """ Add action to role in role group policy
        Args:
            role_group_role_uuid (str):               Role group role UUID
            action_uuid (str):                        Action UUID
        Returns:
            Result
        """
        return self.__connection_manager.insert(f"""
            INSERT INTO role_group_role_action (role_group_role_id, action_id)
            SELECT role_group_role.id, action.id FROM role_group_role, action
            WHERE bin_to_uuid(role_group_role.uuid) = %(role_group_role_uuid)s
            AND bin_to_uuid(action.uuid) = %(action_uuid)s
        """, {
            "role_group_role_uuid": role_group_role_uuid,
            "action_uuid": action_uuid
        })

    def load_action_policy_by_id(self, role_group_role_action_id: int) -> Result:
        """ Load action policy by ID
        Args:
            role_group_role_action_id (int):
        Returns:
            Result
        """
        return self.__connection_manager.select(f"""
            SELECT
                role_group_role_action.id AS role_group_role_action_id,
                bin_to_uuid(role_group_role_action.uuid) AS role_group_role_action_uuid,
                role_group_role_action.action_id AS action_id,
                bin_to_uuid(action.uuid) AS action_uuid,
                action.const AS action_const,
                action.description AS action_description
            FROM role_group_role_action
            INNER JOIN action ON role_group_role_action.action_id = action.id
            WHERE role_group_role_action.id = %(id)s
        """, {
            "id": role_group_role_action_id
        })

    def delete_action(self, role_group_role_action_uuid: str) -> Result:
        """ Delete action from role in role group policy
        Args:
            role_group_role_action_uuid (str):            Role group role action UUID
        Returns:
            Result
        """
        return self.__connection_manager.query(f"""
            DELETE FROM role_group_role_action WHERE bin_to_uuid(role_group_role_action.uuid) = %(uuid)s
        """, {
            "uuid": role_group_role_action_uuid
        })

    def load_by_role_group_uuid(self, role_group_uuid: str) -> Result:
        """ Load role group policy by role group ID
        Args:
            role_group_uuid (str):      Role group UUID
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
                bin_to_uuid(role.uuid) AS role_uuid,
                role.const AS role_const,
                role.description AS role_description,
                role_group_role_action.id AS role_group_role_action_id,
                bin_to_uuid(role_group_role_action.uuid) AS role_group_role_action_uuid,
                action.id AS action_id,
                bin_to_uuid(action.uuid) AS action_uuid,
                action.const AS action_const,
                action.description AS action_description
            FROM role_group
            INNER JOIN role_group_role ON role_group.id = role_group_role.role_group_id
            INNER JOIN role ON role.id = role_group_role.role_id
            LEFT JOIN role_group_role_action ON role_group_role.id = role_group_role_action.role_group_role_id
            LEFT JOIN action ON action.id = role_group_role_action.action_id
            WHERE bin_to_uuid(role_group.uuid) = %(uuid)s
        """, {
            "uuid": role_group_uuid
        })
