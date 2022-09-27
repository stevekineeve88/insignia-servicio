from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface
from modules.policy.data.role_group_policy_data import RoleGroupPolicyData


class RoleGroupPolicyDataFactory(FactoryInterface):
    """ Factory for creating role group policy data object
    """
    def invoke(self, service_manager):
        return RoleGroupPolicyData(
            connection_manager=service_manager.get(ConnectionManager.__name__)
        )
