from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface
from modules.role.data.role_data import RoleData
from modules.role.managers.role_manager import RoleManager


class RoleManagerFactory(FactoryInterface):
    """ Factory for creating role manager object
    """
    def invoke(self, service_manager):
        return RoleManager(
            role_data=service_manager.get(RoleData.__name__)
        )
