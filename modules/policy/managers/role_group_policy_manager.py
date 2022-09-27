from modules.policy.data.role_group_policy_data import RoleGroupPolicyData
from modules.policy.exceptions.role_group_policy_add_action_exception import RoleGroupPolicyAddActionException
from modules.policy.exceptions.role_group_policy_add_role_exception import RoleGroupPolicyAddRoleException
from modules.policy.exceptions.role_group_policy_delete_action_exception import RoleGroupPolicyDeleteActionException
from modules.policy.exceptions.role_group_policy_delete_role_exception import RoleGroupPolicyDeleteRoleException
from modules.policy.exceptions.role_group_policy_fetch_exception import RoleGroupPolicyFetchException
from modules.policy.objects.role_group_policy import RoleGroupPolicy


class RoleGroupPolicyManager:
    """ Manager for role group policy CRUD operations
    """
    def __init__(self, **kwargs):
        """ Constructor for RoleGroupPolicyManager
        Args:
            **kwargs:       Dependencies
                role_group_policy_data (RoleGroupPolicyData)            - Role group policy data layer
        """
        self.__role_group_policy_data: RoleGroupPolicyData = kwargs.get("role_group_policy_data")

    def add_role(self, role_group_id: int, role_id: int) -> int:
        """ Add role to role group policy returning ID
        Args:
            role_group_id (int):            Role group ID
            role_id (int):                  Role ID
        Returns:
            int
        """
        result = self.__role_group_policy_data.add_role(role_group_id, role_id)
        if not result.get_status():
            raise RoleGroupPolicyAddRoleException("Could not add role to role group policy")
        return result.get_last_insert_id()

    def add_action(self, role_group_role_id: int, action_id: int) -> int:
        """ Add action to role in role group policy returning ID
        Args:
            role_group_role_id (int):           Role group role ID
            action_id (int):                    Action ID
        Returns:
            int
        """
        result = self.__role_group_policy_data.add_action(role_group_role_id, action_id)
        if not result.get_status():
            raise RoleGroupPolicyAddActionException("Could not add action to role group role policy")
        return result.get_last_insert_id()

    def delete_role(self, role_group_role_id: int):
        """ Delete role from role group policy
        Args:
            role_group_role_id (int):           Role group role ID
        """
        result = self.__role_group_policy_data.delete_role(role_group_role_id)
        if result.get_affected_rows() == 0:
            raise RoleGroupPolicyDeleteRoleException("Could not delete role from role group policy")

    def delete_action(self, role_group_role_action_id: int):
        """ Delete action from role of role group policy
        Args:
            role_group_role_action_id (int):            Role group role action ID
        """
        result = self.__role_group_policy_data.delete_action(role_group_role_action_id)
        if result.get_affected_rows() == 0:
            raise RoleGroupPolicyDeleteActionException("Could not delete action from role group role policy")

    def get_role_group_policy(self, role_group_id: int) -> RoleGroupPolicy:
        """ Get role group policy by role group ID
        Args:
            role_group_id (int):        Role group ID
        Returns:
            RoleGroupPolicy
        """
        result = self.__role_group_policy_data.load_by_role_group_id(role_group_id)
        if result.get_affected_rows() == 0:
            raise RoleGroupPolicyFetchException("Could not fetch role group policy")
        return RoleGroupPolicy(result.get_data())
