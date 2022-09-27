from typing import List, Dict
from modules.action.objects.action import Action
from modules.policy.objects.action_policy import ActionPolicy
from modules.policy.objects.role_policy import RolePolicy
from modules.role.objects.role import Role
from modules.role.objects.role_group import RoleGroup


class RoleGroupPolicy:
    """ Object representing a role group policy with roles and actions
    """
    def __init__(self, data: List[Dict[str, any]]):
        """ Constructor for RoleGroupPolicy
        Args:
            data (List[Dict[str, any]]):          Role group role/action information
                role_group_id (int)
                role_group_uuid (str)
                role_group_const (str)
                role_group_description (str)
                role_id (int)
                role_const (str)
                role_description (str)
                role_group_role_id (int)
                role_group_role_uuid (str)
                action_id (int)
                action_const (str)
                action_description (str)
                role_group_role_action_id (int)
                role_group_role_action_uuid (str)
        """
        if len(data) == 0:
            return
        self.__role_group: RoleGroup = RoleGroup(
            id=data[0]["role_group_id"],
            uuid=data[0]["role_group_uuid"],
            const=data[0]["role_group_const"],
            description=data[0]["role_group_description"]
        )

        self.__role_policies: Dict[str, RolePolicy] = {}
        for datum in data:
            role_group_role_uuid = datum["role_group_role_uuid"]
            if role_group_role_uuid not in self.__role_policies:
                self.__role_policies[role_group_role_uuid] = RolePolicy(
                    Role(datum["role_id"], datum["role_const"], datum["role_description"]),
                    [],
                    id=datum["role_group_role_id"],
                    uuid=role_group_role_uuid
                )
            role_policy = self.__role_policies[role_group_role_uuid]
            role_group_role_action_id = datum["role_group_role_action_id"]
            if role_group_role_action_id is not None:
                role_policy.add_action_policy(ActionPolicy(
                    Action(datum["action_id"], datum["action_const"], datum["action_description"]),
                    id=role_group_role_action_id,
                    uuid=datum["role_group_role_action_uuid"]
                ))

    def get_role_group(self) -> RoleGroup:
        """ Get role group
        Returns:
            RoleGroup
        """
        return self.__role_group

    def get_role_policies(self) -> List[RolePolicy]:
        """ Get role policies for role group policy
        Returns:
            List[RolePolicy]
        """
        return list(self.__role_policies.values())
