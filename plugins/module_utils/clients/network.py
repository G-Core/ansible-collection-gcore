from enum import Enum

from ansible_collections.gcore.cloud.plugins.module_utils.clients.base import (
    BaseResourceClient,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.network import (
    CreateNetwork,
    GetNetworkList,
    NetworkId,
    UpdateNetwork,
)


class NetworkManageAction(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class NetworkGetAction(str, Enum):
    GET_LIST = "get_list"
    GET_BY_ID = "get_by_id"


class CloudNetworkClient(BaseResourceClient):
    RESOURCE = "network"

    ACTION_CONFIG = {
        NetworkGetAction.GET_LIST: {
            "method": "get",
            "schemas": {
                "query_params": GetNetworkList,
            },
        },
        NetworkGetAction.GET_BY_ID: {
            "method": "get",
            "path": "{network_id}",
            "schemas": {
                "path_params": NetworkId,
            },
        },
        NetworkManageAction.CREATE: {
            "method": "post",
            "as_task": True,
            "timeout": 1000,
            "schemas": {
                "data": CreateNetwork,
            },
        },
        NetworkManageAction.UPDATE: {
            "method": "patch",
            "path": "{network_id}",
            "schemas": {
                "path_params": NetworkId,
                "data": UpdateNetwork,
            },
        },
        NetworkManageAction.DELETE: {
            "method": "delete",
            "path": "{network_id}",
            "as_task": True,
            "timeout": 1200,
            "schemas": {
                "path_params": NetworkId,
            },
        },
    }
