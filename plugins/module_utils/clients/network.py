from enum import Enum

from ansible_collections.gcore.cloud.plugins.module_utils.clients.base import (
    BaseResourceClient,
)


class NetworkAction(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class GCoreNetworkClient(BaseResourceClient):
    ACTION_CONFIG = {
        NetworkAction.CREATE: {
            "method": "post",
            "required_params": ["name"],
        },
        NetworkAction.UPDATE: {
            "method": "patch",
            "path": "{network_id}",
            "required_params": ["network_id", "name"],
        },
        NetworkAction.DELETE: {
            "method": "delete",
            "path": "{network_id}",
            "required_params": ["network_id"],
        },
    }
