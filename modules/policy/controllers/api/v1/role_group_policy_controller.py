from http import HTTPStatus
from flask import Blueprint
from sk88_http_response.modules.http.objects.http_response import HTTPResponse
from modules.policy.exceptions.role_group_policy_fetch_exception import RoleGroupPolicyFetchException
from modules.policy.managers.role_group_policy_manager import RoleGroupPolicyManager
from service_locator import get_service_manager

role_group_policy_v1_api = Blueprint("role_group_policy_v1_api", __name__)
ROOT = "/v1/role-group-policy"


@role_group_policy_v1_api.route(f"{ROOT}/<role_group_id>", methods=["GET"])
def get_role_group_policy_by_role_group_id(role_group_id: str):
    """ GET role group policy by role group ID
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    role_group_policy_manager: RoleGroupPolicyManager = service_locator.get(RoleGroupPolicyManager.__name__)
    try:
        role_group_policy = role_group_policy_manager.get_role_group_policy(int(role_group_id))
        return HTTPResponse(HTTPStatus.OK, "", [role_group_policy]).get_response()
    except RoleGroupPolicyFetchException as e:
        return HTTPResponse(HTTPStatus.NOT_FOUND, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()
