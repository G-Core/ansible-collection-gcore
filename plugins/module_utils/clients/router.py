from enum import Enum

from ansible_collections.gcore.cloud.plugins.module_utils.clients.base import (
    BaseResourceClient,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.router import (
    AttachRouter,
    CreateRouter,
    DetachRouter,
    GetRouterList,
    RouterId,
    UpdateRouter,
)


class RouterManageAction(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    ATTACH = "attach"
    DETACH = "detach"
    DELETE = "delete"


class RouterkGetAction(str, Enum):
    GET_LIST = "get_list"
    GET_BY_ID = "get_by_id"


class CloudRouterClient(BaseResourceClient):
    RESOURCE = "router"

    ACTION_CONFIG = {
        RouterkGetAction.GET_LIST: {
            "method": "get",
            "schemas": {
                "query_params": GetRouterList,
            },
        },
        RouterkGetAction.GET_BY_ID: {
            "method": "get",
            "path": "{router_id}",
            "schemas": {
                "path_params": RouterId,
            },
        },
        RouterManageAction.CREATE: {
            "method": "post",
            "as_task": True,
            "timeout": 1000,
            "schemas": {
                "data": CreateRouter,
            },
        },
        RouterManageAction.UPDATE: {
            "method": "patch",
            "path": "{router_id}",
            "schemas": {
                "path_params": RouterId,
                "data": UpdateRouter,
            },
        },
        RouterManageAction.DELETE: {
            "method": "delete",
            "path": "{router_id}",
            "as_task": True,
            "timeout": 1200,
            "schemas": {
                "path_params": RouterId,
            },
        },
        RouterManageAction.ATTACH: {
            "method": "post",
            "path": "{router_id}/attach",
            "schemas": {
                "path_params": RouterId,
                "data": AttachRouter,
            },
        },
        RouterManageAction.DETACH: {
            "method": "post",
            "path": "{router_id}/detach",
            "schemas": {
                "path_params": RouterId,
                "data": DetachRouter,
            },
        },
    }
