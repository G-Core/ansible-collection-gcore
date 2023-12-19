from enum import Enum

from ansible_collections.gcore.cloud.plugins.module_utils.clients.base import (
    BaseResourceClient,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.loadbalancer_listener import (
    CreateLbListener,
    GetLbListener,
    GetLbListenerList,
    LbListenerId,
    UpdateLbListener,
)


class LbListenerManageAction(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class LbListenerGetAction(str, Enum):
    GET_LIST = "get_list"
    GET_BY_ID = "get_by_id"


class CloudLbListenerClient(BaseResourceClient):
    RESOURCE = "listener"

    ACTION_CONFIG = {
        LbListenerGetAction.GET_LIST: {
            "method": "get",
            "schemas": {
                "query_params": GetLbListenerList,
            },
        },
        LbListenerGetAction.GET_BY_ID: {
            "method": "get",
            "path": "{loadbalancer_listener_id}",
            "schemas": {
                "path_params": LbListenerId,
                "query_params": GetLbListener,
            },
        },
        LbListenerManageAction.CREATE: {
            "method": "post",
            "as_task": True,
            "timeout": 1400,
            "schemas": {
                "data": CreateLbListener,
            },
        },
        LbListenerManageAction.UPDATE: {
            "method": "patch",
            "path": "{loadbalancer_listener_id}",
            "schemas": {
                "path_params": LbListenerId,
                "data": UpdateLbListener,
            },
        },
        LbListenerManageAction.DELETE: {
            "method": "delete",
            "path": "{loadbalancer_listener_id}",
            "as_task": True,
            "timeout": 1200,
            "schemas": {
                "path_params": LbListenerId,
            },
        },
    }
