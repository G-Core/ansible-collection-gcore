from enum import Enum

from ansible_collections.gcore.cloud.plugins.module_utils.clients.base import (
    BaseResourceClient,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.reserved_fip import (
    CreateAnySubnetReservedFip,
    CreateExternalReservedFip,
    CreateIpAddrReservedFip,
    CreateSubnetReservedFip,
    GetReservedFipList,
    ReservedFipId,
    UpdateReservedFip,
)


class ReservedFipManageAction(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class ReservedFipGetAction(str, Enum):
    GET_LIST = "get_list"
    GET_BY_ID = "get_by_id"


class CloudReservedFipClient(BaseResourceClient):
    RESOURCE = "port"

    ACTION_CONFIG = {
        ReservedFipGetAction.GET_LIST: {
            "method": "get",
            "schemas": {
                "query_params": GetReservedFipList,
            },
        },
        ReservedFipGetAction.GET_BY_ID: {
            "method": "get",
            "path": "{port_id}",
            "schemas": {
                "path_params": ReservedFipId,
            },
        },
        ReservedFipManageAction.CREATE: {
            "method": "post",
            "as_task": True,
            "timeout": 1000,
            "expected_key": "type",
            "schemas": {
                "external": {"data": CreateExternalReservedFip},
                "subnet": {"data": CreateSubnetReservedFip},
                "any_subnet": {"data": CreateAnySubnetReservedFip},
                "ip_address": {"data": CreateIpAddrReservedFip},
                "default": {"data": CreateExternalReservedFip},
            },
        },
        ReservedFipManageAction.UPDATE: {
            "method": "patch",
            "path": "{port_id}",
            "schemas": {
                "path_params": ReservedFipId,
                "data": UpdateReservedFip,
            },
        },
        ReservedFipManageAction.DELETE: {
            "method": "delete",
            "path": "{port_id}",
            "as_task": True,
            "timeout": 1200,
            "schemas": {
                "path_params": ReservedFipId,
            },
        },
    }
