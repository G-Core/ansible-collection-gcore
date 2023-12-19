from enum import Enum

from ansible_collections.gcore.cloud.plugins.module_utils.clients.base import (
    BaseResourceClient,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.loadbalancer import (
    CreateLoadbalancer,
    GetLoadbalancer,
    GetLoadbalancerList,
    LoadbalancerId,
    UpdateLoadbalancer,
)


class LoadbalancerManageAction(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class LoadbalancerGetAction(str, Enum):
    GET_LIST = "get_list"
    GET_BY_ID = "get_by_id"


class CloudLoadbalancerClient(BaseResourceClient):
    RESOURCE = "loadbalancer"

    ACTION_CONFIG = {
        LoadbalancerGetAction.GET_LIST: {
            "method": "get",
            "schemas": {
                "query_params": GetLoadbalancerList,
            },
        },
        LoadbalancerGetAction.GET_BY_ID: {
            "method": "get",
            "path": "{loadbalancer_id}",
            "schemas": {
                "path_params": LoadbalancerId,
                "query_params": GetLoadbalancer,
            },
        },
        LoadbalancerManageAction.CREATE: {
            "method": "post",
            "as_task": True,
            "timeout": 2400,
            "schemas": {
                "data": CreateLoadbalancer,
            },
        },
        LoadbalancerManageAction.UPDATE: {
            "method": "patch",
            "path": "{loadbalancer_id}",
            "schemas": {
                "path_params": LoadbalancerId,
                "data": UpdateLoadbalancer,
            },
        },
        LoadbalancerManageAction.DELETE: {
            "method": "delete",
            "path": "{loadbalancer_id}",
            "as_task": True,
            "timeout": 1200,
            "schemas": {
                "path_params": LoadbalancerId,
            },
        },
    }
