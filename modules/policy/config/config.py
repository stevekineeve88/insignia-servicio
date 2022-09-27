from typing import Dict
from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface
from modules.policy.data.factories.role_group_policy_data_factory import RoleGroupPolicyDataFactory
from modules.policy.data.role_group_policy_data import RoleGroupPolicyData
from modules.policy.managers.factories.role_group_policy_manager_factory import RoleGroupPolicyManagerFactory
from modules.policy.managers.role_group_policy_manager import RoleGroupPolicyManager


class PolicyConfig:

    @classmethod
    def get(cls) -> Dict[str, FactoryInterface]:
        return {
            RoleGroupPolicyData.__name__: RoleGroupPolicyDataFactory(),
            RoleGroupPolicyManager.__name__: RoleGroupPolicyManagerFactory()
        }
