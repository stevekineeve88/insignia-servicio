import json
from http import HTTPStatus
from flask import Blueprint, request
from sk88_http_response.modules.http.objects.http_response import HTTPResponse
from modules.role.exceptions.role_group_create_exception import RoleGroupCreateException
from modules.role.exceptions.role_group_delete_exception import RoleGroupDeleteException
from modules.role.exceptions.role_group_fetch_exception import RoleGroupFetchException
from modules.role.managers.role_group_manager import RoleGroupManager
from service_locator import get_service_manager

role_group_v1_api = Blueprint("role_group_v1_api", __name__)
ROOT = "/v1/role-group"


@role_group_v1_api.route(f"{ROOT}", methods=["POST"])
def create_role_group():
    """ POST role group
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    role_group_manager: RoleGroupManager = service_locator.get(RoleGroupManager.__name__)
    try:
        data = json.loads(request.get_data().decode())
        role_group = role_group_manager.create(data["const"], data["description"])
        return HTTPResponse(HTTPStatus.CREATED, "", [role_group]).get_response()
    except RoleGroupCreateException as e:
        return HTTPResponse(HTTPStatus.CONFLICT, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()


@role_group_v1_api.route(f"{ROOT}", methods=["GET"])
def search_role_groups():
    """ GET role groups
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    role_group_manager: RoleGroupManager = service_locator.get(RoleGroupManager.__name__)
    try:
        query_params = request.args.to_dict()
        search_query = query_params.get("search") or ""
        limit = query_params.get("limit") or 10
        offset = query_params.get("offset") or 0

        result = role_group_manager.search(search=search_query, limit=int(limit), offset=int(offset))
        http_response = HTTPResponse(HTTPStatus.OK, "", result.get_role_groups())
        http_response.set_meta({
            "total_count": result.get_total_count(),
            "search": search_query,
            "limit": limit,
            "offset": offset
        })
        return http_response.get_response()
    except RoleGroupFetchException as e:
        return HTTPResponse(HTTPStatus.NOT_FOUND, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()


@role_group_v1_api.route(f"{ROOT}/<role_group_uuid>", methods=["DELETE"])
def delete_role_by_uuid(role_group_uuid: str):
    """ DELETE role group
    Args:
        role_group_uuid (str):
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    role_group_manager: RoleGroupManager = service_locator.get(RoleGroupManager.__name__)
    try:
        role_group_manager.delete(role_group_uuid)
        return HTTPResponse(HTTPStatus.OK, "").get_response()
    except RoleGroupDeleteException as e:
        return HTTPResponse(HTTPStatus.CONFLICT, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()
