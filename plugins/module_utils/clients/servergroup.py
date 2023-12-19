from enum import Enum

from ansible_collections.gcore.cloud.plugins.module_utils.clients.base import (
    BaseResourceClient,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.servergroup import (
    CreateServerGroup,
    ServerGroupId,
)


class ServerGroupManageAction(str, Enum):
    CREATE = "create"
    DELETE = "delete"


class ServerGroupGetAction(str, Enum):
    GET_LIST = "get_list"
    GET_BY_ID = "get_by_id"


class CloudServerGroupClient(BaseResourceClient):
    RESOURCE = "servergroup"

    ACTION_CONFIG = {
        ServerGroupGetAction.GET_LIST: {"method": "get"},
        ServerGroupGetAction.GET_BY_ID: {
            "method": "get",
            "path": "{servergroup_id}",
            "schemas": {
                "path_params": ServerGroupId,
            },
        },
        ServerGroupManageAction.CREATE: {
            "method": "post",
            "schemas": {
                "data": CreateServerGroup,
            },
        },
        ServerGroupManageAction.DELETE: {
            "method": "delete",
            "path": "{servergroup_id}",
            "as_task": True,
            "timeout": 1200,
            "schemas": {
                "path_params": ServerGroupId,
            },
        },
    }
