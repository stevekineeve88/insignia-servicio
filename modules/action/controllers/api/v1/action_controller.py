import json
from http import HTTPStatus
from flask import Blueprint, request
from sk88_http_response.modules.http.objects.http_response import HTTPResponse
from modules.action.exceptions.action_create_exception import ActionCreateException
from modules.action.exceptions.action_delete_exception import ActionDeleteException
from modules.action.exceptions.action_fetch_exception import ActionFetchException
from modules.action.managers.action_manager import ActionManager
from service_locator import get_service_manager

action_v1_api = Blueprint("action_v1_api", __name__)
ROOT = "/v1/action"


@action_v1_api.route(f"{ROOT}", methods=["POST"])
def create_action():
    """ POST action
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    action_manager: ActionManager = service_locator.get(ActionManager.__name__)
    try:
        data = json.loads(request.get_data().decode())
        action = action_manager.create(data["const"], data["description"])
        return HTTPResponse(HTTPStatus.CREATED, "", [action]).get_response()
    except ActionCreateException as e:
        return HTTPResponse(HTTPStatus.CONFLICT, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()


@action_v1_api.route(f"{ROOT}", methods=["GET"])
def search_actions():
    """ GET actions
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    action_manager: ActionManager = service_locator.get(ActionManager.__name__)
    try:
        query_params = request.args.to_dict()
        search_query = query_params.get("search") or ""
        limit = query_params.get("limit") or 10
        offset = query_params.get("offset") or 0

        result = action_manager.search(search=search_query, limit=int(limit), offset=int(offset))
        http_response = HTTPResponse(HTTPStatus.OK, "", result.get_actions())
        http_response.set_meta({
            "total_count": result.get_total_count(),
            "search": search_query,
            "limit": limit,
            "offset": offset
        })
        return http_response.get_response()
    except ActionFetchException as e:
        return HTTPResponse(HTTPStatus.NOT_FOUND, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()


@action_v1_api.route(f"{ROOT}/<action_uuid>", methods=["DELETE"])
def delete_action_by_uuid(action_uuid: str):
    """ DELETE action
    Args:
        action_uuid (str):
    Returns:
        tuple
    """
    service_locator = get_service_manager()
    action_manager: ActionManager = service_locator.get(ActionManager.__name__)
    try:
        action_manager.delete(action_uuid)
        return HTTPResponse(HTTPStatus.OK, "").get_response()
    except ActionDeleteException as e:
        return HTTPResponse(HTTPStatus.CONFLICT, str(e)).get_response()
    except Exception as e:
        return HTTPResponse(HTTPStatus.INTERNAL_SERVER_ERROR, str(e)).get_response()
