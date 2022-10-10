import json
from http import HTTPStatus
from flask import Blueprint, request
from sk88_http_response.modules.http.objects.http_response import HTTPResponse
from modules.role.exceptions.role_create_exception import RoleCreateException
from modules.role.exceptions.role_delete_exception import RoleDeleteException
from modules.role.exceptions.role_fetch_exception import RoleFetchException
from modules.role.managers.role_manager import RoleManager
from service_locator import get_service_manager

role_v1_api = Blueprint("role_v1_api", __name__)
ROOT = "/v1/role"


@role_v1_api.route(f"{ROOT}", methods=["POST"])
def create_role():
    """ POST role
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    role_manager: RoleManager = service_locator.get(RoleManager.__name__)
    try:
        data = json.loads(request.get_data().decode())
        role = role_manager.create(data["const"], data["description"])
        return HTTPResponse(HTTPStatus.CREATED, "", [role]).get_response()
    except RoleCreateException as e:
        return HTTPResponse(HTTPStatus.CONFLICT, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()


@role_v1_api.route(f"{ROOT}", methods=["GET"])
def search_roles():
    """ GET roles
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    role_manager: RoleManager = service_locator.get(RoleManager.__name__)
    try:
        query_params = request.args.to_dict()
        search_query = query_params.get("search") or ""
        limit = query_params.get("limit") or 10
        offset = query_params.get("offset") or 0

        result = role_manager.search(search=search_query, limit=int(limit), offset=int(offset))
        http_response = HTTPResponse(HTTPStatus.OK, "", result.get_roles())
        http_response.set_meta({
            "total_count": result.get_total_count(),
            "search": search_query,
            "limit": limit,
            "offset": offset
        })
        return http_response.get_response()
    except RoleFetchException as e:
        return HTTPResponse(HTTPStatus.NOT_FOUND, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()


@role_v1_api.route(f"{ROOT}/<role_uuid>", methods=["DELETE"])
def delete_role_by_uuid(role_uuid: str):
    """ DELETE role
    Args:
        role_uuid (str):
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    role_manager: RoleManager = service_locator.get(RoleManager.__name__)
    try:
        role_manager.delete(role_uuid)
        return HTTPResponse(HTTPStatus.OK, "").get_response()
    except RoleDeleteException as e:
        return HTTPResponse(HTTPStatus.CONFLICT, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()
