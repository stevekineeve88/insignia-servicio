from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface
from modules.action.data.action_data import ActionData
from modules.action.managers.action_manager import ActionManager


class ActionManagerFactory(FactoryInterface):
    """ Factory for creating action manager object
    """
    def invoke(self, service_manager):
        return ActionManager(
            action_data=service_manager.get(ActionData.__name__)
        )
