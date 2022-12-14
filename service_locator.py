from sk88_service_locator.modules.service.managers.service_manager import ServiceManager
from modules.action.config.config import ActionConfig
from modules.policy.config.config import PolicyConfig
from modules.role.config.config import RoleConfig
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
        service_locator.add(RoleConfig().get())
        service_locator.add(PolicyConfig().get())

    return service_locator
