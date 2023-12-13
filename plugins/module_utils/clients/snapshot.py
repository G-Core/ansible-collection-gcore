from enum import Enum

from ansible_collections.gcore.cloud.plugins.module_utils.clients.base import (
    BaseResourceClient,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.snapshot import (
    CreateSnapshot,
    GetSnapshotList,
    SnapshotId,
)


class SnapshotManageAction(str, Enum):
    CREATE = "create"
    DELETE = "delete"


class SnapshotGetAction(str, Enum):
    GET_LIST = "get_list"
    GET_BY_ID = "get_by_id"


class CloudSnapshotClient(BaseResourceClient):
    RESOURCE = "snapshot"

    ACTION_CONFIG = {
        SnapshotGetAction.GET_LIST: {
            "method": "get",
            "schemas": {
                "query_params": GetSnapshotList,
            },
        },
        SnapshotGetAction.GET_BY_ID: {
            "method": "get",
            "path": "{snapshot_id}",
            "schemas": {
                "path_params": SnapshotId,
            },
        },
        SnapshotManageAction.CREATE: {
            "method": "post",
            "as_task": True,
            "timeout": 1200,
            "schemas": {
                "data": CreateSnapshot,
            },
        },
        SnapshotManageAction.DELETE: {
            "method": "delete",
            "as_task": True,
            "timeout": 1200,
            "path": "{snapshot_id}",
            "schemas": {
                "path_params": SnapshotId,
            },
        },
    }
