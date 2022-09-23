from sk88_service_locator.modules.service.managers.service_manager import ServiceManager
from modules.action.config.config import ActionConfig
from modules.util.config.config import UtilConfig


service_locator: ServiceManager or None = None


def get_service_manager() -> ServiceManager:
    """ Get service manager
    Returns:
        ServiceManager
    """
    global service_locator

    if service_locator is None:
        service_locator = ServiceManager()
        service_locator.add(UtilConfig().get())
        service_locator.add(ActionConfig().get())

    return service_locator
