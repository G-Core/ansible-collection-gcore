from enum import Enum

from ansible_collections.gcore.cloud.plugins.module_utils.clients.base import (
    BaseResourceClient,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.instance import (
    AddToServergroup,
    CreateInstance,
    DeleteInstance,
    GetInstanceList,
    GetInstanceQuota,
    InstanceId,
    StartInstance,
    UpdateInstance,
)


class InstanceManageAction(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    START = "start"
    STOP = "stop"
    POWERCYCLE = "powercycle"
    REBOOT = "reboot"
    SUSPEND = "suspend"
    RESUME = "resume"
    ADD_TO_SERVERGROUP = "add_to_servergroup"
    REMOVE_FROM_SERVERGROUP = "remove_from_servergroup"


class InstanceGetAction(str, Enum):
    GET_LIST = "get_list"
    GET_BY_ID = "get_by_id"
    GET_QUOTA = "get_quota"


class CloudInstanceClient(BaseResourceClient):
    RESOURCE = "instance"

    ACTION_CONFIG = {
        InstanceGetAction.GET_LIST: {
            "method": "get",
            "schemas": {
                "query_params": GetInstanceList,
            },
        },
        InstanceGetAction.GET_BY_ID: {
            "method": "get",
            "path": "{instance_id}",
            "schemas": {
                "path_params": InstanceId,
            },
        },
        InstanceGetAction.GET_QUOTA: {
            "method": "post",
            "url": "v2/instances/",
            "path": "check_limits",
            "schemas": {
                "data": GetInstanceQuota,
            },
        },
        InstanceManageAction.CREATE: {
            "url": "v2/instances/",
            "method": "post",
            "as_task": True,
            "timeout": 3000,
            "schemas": {
                "data": CreateInstance,
            },
        },
        InstanceManageAction.UPDATE: {
            "method": "patch",
            "path": "{instance_id}",
            "schemas": {
                "path_params": InstanceId,
                "data": UpdateInstance,
            },
        },
        InstanceManageAction.DELETE: {
            "method": "delete",
            "path": "{instance_id}",
            "as_task": True,
            "timeout": 1200,
            "schemas": {
                "path_params": InstanceId,
                "query_params": DeleteInstance,
            },
        },
        InstanceManageAction.START: {
            "method": "post",
            "path": "{instance_id}/start",
            "schemas": {
                "path_params": InstanceId,
                "data": StartInstance,
            },
        },
        InstanceManageAction.STOP: {
            "method": "post",
            "path": "{instance_id}/stop",
            "schemas": {
                "path_params": InstanceId,
            },
        },
        InstanceManageAction.POWERCYCLE: {
            "method": "post",
            "path": "{instance_id}/powercycle",
            "schemas": {
                "path_params": InstanceId,
            },
        },
        InstanceManageAction.REBOOT: {
            "method": "post",
            "path": "{instance_id}/reboot",
            "schemas": {
                "path_params": InstanceId,
            },
        },
        InstanceManageAction.SUSPEND: {
            "method": "post",
            "path": "{instance_id}/suspend",
            "schemas": {
                "path_params": InstanceId,
            },
        },
        InstanceManageAction.RESUME: {
            "method": "post",
            "path": "{instance_id}/resume",
            "schemas": {
                "path_params": InstanceId,
            },
        },
        InstanceManageAction.ADD_TO_SERVERGROUP: {
            "method": "post",
            "path": "{instance_id}/put_into_servergroup",
            "schemas": {
                "path_params": InstanceId,
                "data": AddToServergroup,
            },
        },
        InstanceManageAction.REMOVE_FROM_SERVERGROUP: {
            "method": "post",
            "path": "{instance_id}/remove_from_servergroup",
            "schemas": {
                "path_params": InstanceId,
            },
        },
    }
