from typing import Dict
from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface
from modules.action.data.action_data import ActionData
from modules.action.data.factories.action_data_factory import ActionDataFactory
from modules.action.managers.action_manager import ActionManager
from modules.action.managers.factories.action_manager_factory import ActionManagerFactory


class ActionConfig:

    @classmethod
    def get(cls) -> Dict[str, FactoryInterface]:
        return {
            ActionData.__name__: ActionDataFactory(),
            ActionManager.__name__: ActionManagerFactory()
        }
