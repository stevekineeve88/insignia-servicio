from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface

from modules.role.data.role_data import RoleData


class RoleDataFactory(FactoryInterface):
    """ Factory for creating role data object
    """
    def invoke(self, service_manager):
        return RoleData(
            connection_manager=service_manager.get(ConnectionManager.__name__)
        )
