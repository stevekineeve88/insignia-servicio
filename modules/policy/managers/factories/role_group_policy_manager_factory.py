from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface
from modules.policy.data.role_group_policy_data import RoleGroupPolicyData
from modules.policy.managers.role_group_policy_manager import RoleGroupPolicyManager


class RoleGroupPolicyManagerFactory(FactoryInterface):
    """ Factory for role group policy manager object
    """
    def invoke(self, service_manager):
        return RoleGroupPolicyManager(
            role_group_policy_data=service_manager.get(RoleGroupPolicyData.__name__)
        )
