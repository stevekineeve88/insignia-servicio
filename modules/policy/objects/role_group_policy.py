from typing import List, Dict
from sk88_http_response.modules.http.interfaces.http_dict import HTTPDict
from modules.action.objects.action import Action
from modules.policy.objects.action_policy import ActionPolicy
from modules.policy.objects.role_policy import RolePolicy
from modules.role.objects.role import Role
from modules.role.objects.role_group import RoleGroup


class RoleGroupPolicy(HTTPDict):
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

    def get_http_dict(self) -> Dict[str, any]:
        """ Get HTTP dict representation of a role group policy
        Returns:
            Dict[str, any]
        """
        role_policies = []
        role_policy_objects = self.get_role_policies()
        for role_policy in role_policy_objects:
            role_policy_dict = {
                "id": role_policy.get_id(),
                "uuid": role_policy.get_uuid(),
                "role": {
                    "id": role_policy.get_role().get_id(),
                    "const": role_policy.get_role().get_const(),
                    "description": role_policy.get_role().get_description()
                },
                "action_policies": []
            }
            action_policies = role_policy.get_action_policies()
            for action_policy in action_policies:
                role_policy_dict["action_policies"].append({
                    "id": action_policy.get_id(),
                    "uuid": action_policy.get_uuid(),
                    "action": {
                        "id": action_policy.get_action().get_id(),
                        "const": action_policy.get_action().get_const(),
                        "description": action_policy.get_action().get_description()
                    }
                })
            role_policies.append(role_policy_dict)
        return {
            "role_group": {
                "id": self.get_role_group().get_id(),
                "uuid": self.get_role_group().get_uuid(),
                "const": self.get_role_group().get_const(),
                "description": self.get_role_group().get_description()
            },
            "role_policies": role_policies
        }
