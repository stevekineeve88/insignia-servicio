from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface
from modules.role.data.role_group_data import RoleGroupData
from modules.role.managers.role_group_manager import RoleGroupManager


class RoleGroupManagerFactory(FactoryInterface):
    """ Factory for creating role group manager object
    """
    def invoke(self, service_manager):
        return RoleGroupManager(
            role_group_data=service_manager.get(RoleGroupData.__name__)
        )
