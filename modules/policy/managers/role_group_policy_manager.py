from modules.action.objects.action import Action
from modules.policy.data.role_group_policy_data import RoleGroupPolicyData
from modules.policy.exceptions.action_policy_fetch_exception import ActionPolicyFetchException
from modules.policy.exceptions.role_group_policy_add_action_exception import RoleGroupPolicyAddActionException
from modules.policy.exceptions.role_group_policy_add_role_exception import RoleGroupPolicyAddRoleException
from modules.policy.exceptions.role_group_policy_delete_action_exception import RoleGroupPolicyDeleteActionException
from modules.policy.exceptions.role_group_policy_delete_role_exception import RoleGroupPolicyDeleteRoleException
from modules.policy.exceptions.role_group_policy_fetch_exception import RoleGroupPolicyFetchException
from modules.policy.exceptions.role_policy_fetch_exception import RolePolicyFetchException
from modules.policy.objects.action_policy import ActionPolicy
from modules.policy.objects.role_group_policy import RoleGroupPolicy
from modules.policy.objects.role_policy import RolePolicy
from modules.role.objects.role import Role


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

    def add_role(self, role_group_uuid: str, role_uuid: str) -> RolePolicy:
        """ Add role to role group policy returning ID
        Args:
            role_group_uuid (str):            Role group UUID
            role_uuid (str):                  Role UUID
        Returns:
            int
        """
        result = self.__role_group_policy_data.add_role(role_group_uuid, role_uuid)
        if not result.get_status():
            raise RoleGroupPolicyAddRoleException("Could not add role to role group policy")
        return self.get_role_policy_by_id(result.get_last_insert_id())

    def get_role_policy_by_id(self, role_group_role_id: int) -> RolePolicy:
        """ Get role policy by ID
        Args:
            role_group_role_id (int):
        Returns:
            RolePolicy
        """
        result = self.__role_group_policy_data.load_role_policy_by_id(role_group_role_id)
        if result.get_affected_rows() == 0:
            raise RolePolicyFetchException(f"Could not fetch role policy with ID {role_group_role_id}")
        data = result.get_data()[0]
        return RolePolicy(Role(
            id=data["role_id"],
            uuid=data["role_uuid"],
            const=data["role_const"],
            description=data["role_description"]
        ), [], id=data["role_group_role_id"], uuid=data["role_group_role_uuid"])

    def add_action(self, role_group_role_uuid: str, action_uuid: str) -> ActionPolicy:
        """ Add action to role in role group policy returning ID
        Args:
            role_group_role_uuid (str):           Role group role UUID
            action_uuid (str):                    Action UUID
        Returns:
            int
        """
        result = self.__role_group_policy_data.add_action(role_group_role_uuid, action_uuid)
        if not result.get_status():
            raise RoleGroupPolicyAddActionException("Could not add action to role group role policy")
        return self.get_action_policy_by_id(result.get_last_insert_id())

    def get_action_policy_by_id(self, role_group_role_action_id: int) -> ActionPolicy:
        """ Get action policy by ID
        Args:
            role_group_role_action_id (int):
        Returns:
            ActionPolicy
        """
        result = self.__role_group_policy_data.load_action_policy_by_id(role_group_role_action_id)
        if result.get_affected_rows() == 0:
            raise ActionPolicyFetchException(f"Could not fetch action policy with ID {role_group_role_action_id}")
        data = result.get_data()[0]
        return ActionPolicy(Action(
            id=data["action_id"],
            uuid=data["action_uuid"],
            const=data["action_const"],
            description=data["action_description"]
        ), id=data["role_group_role_action_id"], uuid=data["role_group_role_action_uuid"])

    def delete_role(self, role_group_role_uuid: str):
        """ Delete role from role group policy
        Args:
            role_group_role_uuid (str):           Role group role UUID
        """
        result = self.__role_group_policy_data.delete_role(role_group_role_uuid)
        if result.get_affected_rows() == 0:
            raise RoleGroupPolicyDeleteRoleException("Could not delete role from role group policy")

    def delete_action(self, role_group_role_action_uuid: str):
        """ Delete action from role of role group policy
        Args:
            role_group_role_action_uuid (str):            Role group role action UUID
        """
        result = self.__role_group_policy_data.delete_action(role_group_role_action_uuid)
        if result.get_affected_rows() == 0:
            raise RoleGroupPolicyDeleteActionException("Could not delete action from role group role policy")

    def get_role_group_policy(self, role_group_uuid: str) -> RoleGroupPolicy:
        """ Get role group policy by role group UUID
        Args:
            role_group_uuid (str):        Role group UUID
        Returns:
            RoleGroupPolicy
        """
        result = self.__role_group_policy_data.load_by_role_group_uuid(role_group_uuid)
        if result.get_affected_rows() == 0:
            raise RoleGroupPolicyFetchException("Could not fetch role group policy")
        return RoleGroupPolicy(result.get_data())
