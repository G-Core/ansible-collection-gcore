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
    GetVolumeList,
    RetypeVolume,
    UpdateVolume,
    VolumeId,
    VolumeInstanceAction,
)


class VolumeManageAction(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    ATTACH = "attach"
    DETACH = "detach"
    EXTEND = "extend"
    RETYPE = "retype"
    REVERT = "revert"


class VolumeGetAction(str, Enum):
    GET_LIST = "get_list"
    GET_BY_ID = "get_by_id"


class CloudVolumeClient(BaseResourceClient):
    RESOURCE = "volume"

    ACTION_CONFIG = {
        VolumeGetAction.GET_LIST: {
            "method": "get",
            "schemas": {
                "query_params": GetVolumeList,
            },
        },
        VolumeGetAction.GET_BY_ID: {
            "method": "get",
            "path": "{volume_id}",
            "schemas": {
                "path_params": VolumeId,
            },
        },
        VolumeManageAction.CREATE: {
            "method": "post",
            "as_task": True,
            "timeout": 1200,
            "schemas": {
                "new-volume": {"data": CreateVolume},
                "image": {"data": CreateVolumeFromImage},
                "snapshot": {"data": CreateVolumeFromSnapshot},
                "default": {"data": CreateVolume},
            },
        },
        VolumeManageAction.UPDATE: {
            "method": "patch",
            "path": "{volume_id}",
            "schemas": {"path_params": VolumeId, "data": UpdateVolume},
        },
        VolumeManageAction.DELETE: {
            "method": "delete",
            "as_task": True,
            "timeout": 1200,
            "path": "{volume_id}",
            "schemas": {
                "path_params": VolumeId,
                "query_params": DeleteVolume,
            },
        },
        VolumeManageAction.ATTACH: {
            "url": "v2/volumes/",
            "method": "post",
            "as_task": True,
            "timeout": 600,
            "path": "{volume_id}/attach",
            "schemas": {
                "path_params": VolumeId,
                "data": VolumeInstanceAction,
            },
        },
        VolumeManageAction.DETACH: {
            "url": "v2/volumes/",
            "method": "post",
            "as_task": True,
            "timeout": 600,
            "path": "{volume_id}/detach",
            "schemas": {
                "path_params": VolumeId,
                "data": VolumeInstanceAction,
            },
        },
        VolumeManageAction.EXTEND: {
            "method": "post",
            "as_task": True,
            "timeout": 1200,
            "path": "{volume_id}/extend",
            "schemas": {
                "path_params": VolumeId,
                "data": ExtendVolume,
            },
        },
        VolumeManageAction.RETYPE: {
            "method": "post",
            "path": "{volume_id}/retype",
            "schemas": {
                "path_params": VolumeId,
                "data": RetypeVolume,
            },
        },
        VolumeManageAction.REVERT: {
            "method": "post",
            "path": "{volume_id}/revert",
            "as_task": True,
            "timeout": 1200,
            "schemas": {
                "path_params": VolumeId,
            },
        },
    }
