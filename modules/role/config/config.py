from typing import Dict
from sk88_service_locator.modules.service.interfaces.factory_interface import FactoryInterface
from modules.role.data.factories.role_data_factory import RoleDataFactory
from modules.role.data.factories.role_group_data_factory import RoleGroupDataFactory
from modules.role.data.role_data import RoleData
from modules.role.data.role_group_data import RoleGroupData
from modules.role.managers.factories.role_group_manager_factory import RoleGroupManagerFactory
from modules.role.managers.factories.role_manager_factory import RoleManagerFactory
from modules.role.managers.role_group_manager import RoleGroupManager
from modules.role.managers.role_manager import RoleManager


class RoleConfig:

    @classmethod
    def get(cls) -> Dict[str, FactoryInterface]:
        return {
            RoleData.__name__: RoleDataFactory(),
            RoleGroupData.__name__: RoleGroupDataFactory(),
            RoleManager.__name__: RoleManagerFactory(),
            RoleGroupManager.__name__: RoleGroupManagerFactory()
        }
