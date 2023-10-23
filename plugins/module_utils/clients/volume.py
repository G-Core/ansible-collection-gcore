from enum import Enum

from ansible_collections.gcore.cloud.plugins.module_utils.clients.base import (
    BaseResourceClient,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.volume import (
    CreateVolume,
    CreateVolumeFromImage,
    CreateVolumeFromSnapshot,
    DeleteVolume,
    ExtendVolume,
    RetypeVolume,
    UpdateVolume,
    VolumeInstanceAction,
)


class VolumeAction(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    ATTACH = "attach"
    DETACH = "detach"
    EXTEND = "extend"
    RETYPE = "retype"


class GCoreVolumeClient(BaseResourceClient):
    ACTION_CONFIG = {
        VolumeAction.CREATE: {
            "method": "post",
            "path": "",
            "schema": {
                "new-volume": CreateVolume,
                "image": CreateVolumeFromImage,
                "snapshot": CreateVolumeFromSnapshot,
            },
        },
        VolumeAction.UPDATE: {"method": "patch", "path": "{volume_id}", "schema": UpdateVolume},
        VolumeAction.DELETE: {"method": "delete", "path": "{volume_id}", "schema": DeleteVolume},
        VolumeAction.ATTACH: {"method": "post", "path": "{volume_id}/attach", "schema": VolumeInstanceAction},
        VolumeAction.DETACH: {"method": "post", "path": "{volume_id}/detach", "schema": VolumeInstanceAction},
        VolumeAction.EXTEND: {"method": "post", "path": "{volume_id}/extend", "schema": ExtendVolume},
        VolumeAction.RETYPE: {"method": "post", "path": "{volume_id}/retype", "schema": RetypeVolume},
    }

    def execute_command(self, command: VolumeAction, params: dict):
        config = self.ACTION_CONFIG[command]
        schema = (
            config["schema"] if command != VolumeAction.CREATE.value else config["schema"].get(params.get("source"))
        )
        self.module.fail_on_missing_params(required_params=schema.get_required())

        data = schema.init_as_dict(params)
        volume_id = data.pop("volume_id", None) if command != VolumeAction.CREATE.value else data.get("volume_id")
        path = config["path"].format(volume_id=volume_id, **data)
        method = getattr(self.api_client, config["method"])
        return method(url=self.url, path=path, data=data)
