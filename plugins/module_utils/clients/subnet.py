from enum import Enum

from ansible_collections.gcore.cloud.plugins.module_utils.clients.base import (
    BaseResourceClient,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.subnet import (
    CreateSubnet,
    GetSubnetList,
    SubnetId,
    UpdateSubnet,
)


class SubnetManageAction(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class SubnetGetAction(str, Enum):
    GET_LIST = "get_list"
    GET_BY_ID = "get_by_id"


class CloudSubnetClient(BaseResourceClient):
    RESOURCE = "subnet"

    ACTION_CONFIG = {
        SubnetGetAction.GET_LIST: {
            "method": "get",
            "schemas": {
                "query_params": GetSubnetList,
            },
        },
        SubnetGetAction.GET_BY_ID: {
            "method": "get",
            "path": "{subnet_id}",
            "schemas": {
                "path_params": SubnetId,
            },
        },
        SubnetManageAction.CREATE: {
            "method": "post",
            "as_task": True,
            "timeout": 1000,
            "allow_none": ["gateway_ip"],
            "schemas": {
                "data": CreateSubnet,
            },
        },
        SubnetManageAction.UPDATE: {
            "method": "patch",
            "path": "{subnet_id}",
            "allow_none": ["gateway_ip"],
            "schemas": {
                "path_params": SubnetId,
                "data": UpdateSubnet,
            },
        },
        SubnetManageAction.DELETE: {
            "method": "delete",
            "path": "{subnet_id}",
            "as_task": True,
            "timeout": 1200,
            "schemas": {
                "path_params": SubnetId,
            },
        },
    }
