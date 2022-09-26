from mysql_data_manager.modules.connection.managers.connection_manager import ConnectionManager
from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface

from modules.action.data.action_data import ActionData


class ActionDataFactory(FactoryInterface):
    """ Factory for creating action data object
    """
    def invoke(self, service_manager):
        return ActionData(
            connection_manager=service_manager.get(ConnectionManager.__name__)
        )
