from enum import Enum

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.gcore.cloud.plugins.module_utils.clients.base import (
    BaseResourceClient,
)


class InstanceAction(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    START = "start"
    STOP = "stop"
    POWERCYCLE = "powercycle"
    REBOOT = "reboot"
    SUSPEND = "suspend"
    RESUME = "resume"


class GCoreInstanceClient(BaseResourceClient):
    ACTION_CONFIG = {
        InstanceAction.CREATE: {
            "url": "v2/instances/",
            "method": "post",
            "path": "",
            "required_params": ["flavor", "interfaces", "volumes"],
        },
        InstanceAction.UPDATE: {
            "method": "patch",
            "path": "{instance_id}",
            "required_params": ["instance_id", "name"],
        },
        InstanceAction.DELETE: {
            "method": "delete",
            "path": "{instance_id}",
            "required_params": ["instance_id"],
        },
        InstanceAction.START: {
            "method": "post",
            "path": "{instance_id}/start",
            "required_params": ["instance_id"],
        },
        InstanceAction.STOP: {
            "method": "post",
            "path": "{instance_id}/stop",
            "required_params": ["instance_id"],
        },
        InstanceAction.POWERCYCLE: {
            "method": "post",
            "path": "{instance_id}/powercycle",
            "required_params": ["instance_id"],
        },
        InstanceAction.REBOOT: {
            "method": "post",
            "path": "{instance_id}/reboot",
            "required_params": ["instance_id"],
        },
        InstanceAction.SUSPEND: {
            "method": "post",
            "path": "{instance_id}/suspend",
            "required_params": ["instance_id"],
        },
        InstanceAction.RESUME: {
            "method": "post",
            "path": "{instance_id}/resume",
            "required_params": ["instance_id"],
        },
    }
