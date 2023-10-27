from enum import Enum

from ansible_collections.gcore.cloud.plugins.module_utils.clients.base import (
    BaseResourceClient,
)


class SnapshotAction(str, Enum):
    CREATE = "create"
    DELETE = "delete"


class GCoreSnapshotClient(BaseResourceClient):
    ACTION_CONFIG = {
        SnapshotAction.CREATE: {
            "method": "post",
            "path": "",
            "required_params": ["volume_id", "name"],
        },
        SnapshotAction.DELETE: {"method": "delete", "path": "{snapshot_id}"},
        "required_params": ["snapshot_id"],
    }
