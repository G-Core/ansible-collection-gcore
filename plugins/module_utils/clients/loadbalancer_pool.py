from enum import Enum

from ansible_collections.gcore.cloud.plugins.module_utils.clients.base import (
    BaseResourceClient,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.loadbalancer_pool import (
    CreateLbPool,
    GetLbPoolList,
    LbPoolId,
    UpdateLbPool,
)


class LbPoolManageAction(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class LbPoolGetAction(str, Enum):
    GET_LIST = "get_list"
    GET_BY_ID = "get_by_id"


class CloudLbPoolClient(BaseResourceClient):
    RESOURCE = "pool"

    ACTION_CONFIG = {
        LbPoolGetAction.GET_LIST: {
            "method": "get",
            "schemas": {
                "query_params": GetLbPoolList,
            },
        },
        LbPoolGetAction.GET_BY_ID: {
            "method": "get",
            "path": "{loadbalancer_pool_id}",
            "schemas": {
                "path_params": LbPoolId,
            },
        },
        LbPoolManageAction.CREATE: {
            "method": "post",
            "as_task": True,
            "timeout": 2400,
            "schemas": {
                "data": CreateLbPool,
            },
        },
        LbPoolManageAction.UPDATE: {
            "method": "patch",
            "path": "{loadbalancer_pool_id}",
            "schemas": {
                "path_params": LbPoolId,
                "data": UpdateLbPool,
            },
        },
        LbPoolManageAction.DELETE: {
            "method": "delete",
            "path": "{loadbalancer_pool_id}",
            "as_task": True,
            "timeout": 1200,
            "schemas": {
                "path_params": LbPoolId,
            },
        },
    }
