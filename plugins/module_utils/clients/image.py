from enum import Enum

from ansible_collections.gcore.cloud.plugins.module_utils.clients.base import (
    BaseResourceClient,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.image import (
    CreateImageFromVolume,
    DownloadImage,
    GetImageList,
    ImageId,
    UpdateImage,
)


class ImageManageAction(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DOWNLOAD = "download"
    DELETE = "delete"


class ImageGetAction(str, Enum):
    GET_LIST = "get_list"
    GET_BY_ID = "get_by_id"
    GET_LIST_FOR_PROJECT = "get_list_for_project"


class CloudImageClient(BaseResourceClient):
    RESOURCE = "image"

    ACTION_CONFIG = {
        ImageGetAction.GET_LIST: {
            "method": "get",
            "schemas": {
                "query_params": GetImageList,
            },
        },
        ImageGetAction.GET_BY_ID: {
            "method": "get",
            "path": "{image_id}",
            "schemas": {
                "path_params": ImageId,
            },
        },
        ImageGetAction.GET_LIST_FOR_PROJECT: {
            "method": "get",
            "url": "v1/projectimages/",
            "schemas": {
                "query_params": GetImageList,
            },
        },
        ImageManageAction.CREATE: {
            "method": "post",
            "as_task": True,
            "timeout": 1200,
            "schemas": {
                "data": CreateImageFromVolume,
            },
        },
        ImageManageAction.UPDATE: {
            "method": "patch",
            "path": "{image_id}",
            "schemas": {
                "path_params": ImageId,
                "data": UpdateImage,
            },
        },
        ImageManageAction.DOWNLOAD: {
            "method": "post",
            "url": "v1/downloadimage/",
            "as_task": True,
            "timeout": 7200,
            "schemas": {
                "data": DownloadImage,
            },
        },
        ImageManageAction.DELETE: {
            "method": "delete",
            "path": "{image_id}",
            "as_task": True,
            "timeout": 2400,
            "schemas": {
                "path_params": ImageId,
            },
        },
    }
