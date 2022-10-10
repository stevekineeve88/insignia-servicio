from http import HTTPStatus
from flask import Blueprint
from sk88_http_response.modules.http.objects.http_response import HTTPResponse

from modules.policy.exceptions.role_group_policy_add_action_exception import RoleGroupPolicyAddActionException
from modules.policy.exceptions.role_group_policy_add_role_exception import RoleGroupPolicyAddRoleException
from modules.policy.exceptions.role_group_policy_delete_action_exception import RoleGroupPolicyDeleteActionException
from modules.policy.exceptions.role_group_policy_delete_role_exception import RoleGroupPolicyDeleteRoleException
from modules.policy.exceptions.role_group_policy_fetch_exception import RoleGroupPolicyFetchException
from modules.policy.managers.role_group_policy_manager import RoleGroupPolicyManager
from service_locator import get_service_manager

role_group_policy_v1_api = Blueprint("role_group_policy_v1_api", __name__)
ROOT = "/v1/role-group-policy"


@role_group_policy_v1_api.route(f"{ROOT}/<role_group_uuid>/add/role/<role_uuid>", methods=["PATCH"])
def create_role_policy(role_group_uuid: str, role_uuid: str):
    """ PATCH add role to role group policy
    Args:
        role_group_uuid (str):
        role_uuid (str):
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    role_group_policy_manager: RoleGroupPolicyManager = service_locator.get(RoleGroupPolicyManager.__name__)
    try:
        role_policy = role_group_policy_manager.add_role(role_group_uuid, role_uuid)
        return HTTPResponse(HTTPStatus.CREATED, "", [role_policy]).get_response()
    except RoleGroupPolicyAddRoleException as e:
        return HTTPResponse(HTTPStatus.CONFLICT, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()


@role_group_policy_v1_api.route(f"{ROOT}/role/<role_group_role_uuid>", methods=["DELETE"])
def delete_role_policy(role_group_role_uuid: str):
    """ DELETE role policy
    Args:
        role_group_role_uuid (str):
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    role_group_policy_manager: RoleGroupPolicyManager = service_locator.get(RoleGroupPolicyManager.__name__)
    try:
        role_group_policy_manager.delete_role(role_group_role_uuid)
        return HTTPResponse(HTTPStatus.OK, "").get_response()
    except RoleGroupPolicyDeleteRoleException as e:
        return HTTPResponse(HTTPStatus.CONFLICT, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()


@role_group_policy_v1_api.route(f"{ROOT}/<role_group_role_uuid>/add/action/<action_uuid>", methods=["PATCH"])
def create_action_policy(role_group_role_uuid: str, action_uuid: str):
    """ PATCH add action to role policy
    Args:
        role_group_role_uuid (str):
        action_uuid (str):
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    role_group_policy_manager: RoleGroupPolicyManager = service_locator.get(RoleGroupPolicyManager.__name__)
    try:
        action_policy = role_group_policy_manager.add_action(role_group_role_uuid, action_uuid)
        return HTTPResponse(HTTPStatus.CREATED, "", [action_policy]).get_response()
    except RoleGroupPolicyAddActionException as e:
        return HTTPResponse(HTTPStatus.CONFLICT, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()


@role_group_policy_v1_api.route(f"{ROOT}/action/<role_group_role_action_uuid>", methods=["DELETE"])
def delete_action_policy(role_group_role_action_uuid: str):
    """ DELETE action policy
    Args:
        role_group_role_action_uuid (str):
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    role_group_policy_manager: RoleGroupPolicyManager = service_locator.get(RoleGroupPolicyManager.__name__)
    try:
        role_group_policy_manager.delete_action(role_group_role_action_uuid)
        return HTTPResponse(HTTPStatus.OK, "").get_response()
    except RoleGroupPolicyDeleteActionException as e:
        return HTTPResponse(HTTPStatus.CONFLICT, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()


@role_group_policy_v1_api.route(f"{ROOT}/<role_group_uuid>", methods=["GET"])
def get_role_group_policy_by_role_group_id(role_group_uuid: str):
    """ GET role group policy by role group UUID
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    role_group_policy_manager: RoleGroupPolicyManager = service_locator.get(RoleGroupPolicyManager.__name__)
    try:
        role_group_policy = role_group_policy_manager.get_role_group_policy(role_group_uuid)
        return HTTPResponse(HTTPStatus.OK, "", [role_group_policy]).get_response()
    except RoleGroupPolicyFetchException as e:
        return HTTPResponse(HTTPStatus.NOT_FOUND, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()
