from enum import Enum

from ansible_collections.gcore.cloud.plugins.module_utils.clients.base import (
    BaseResourceClient,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.lifecycle_policy import (
    AddSchedules,
    AddVolumes,
    CreateLifecyclePolicy,
    GetLifecyclePolicyList,
    LifecyclePolicyId,
    RemoveSchedule,
    RemoveVolumes,
    UpdateLifecyclePolicy,
)


class LifecyclePolicyManageAction(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    ADD_SCHEDULES = "add_schedules"
    REMOVE_SCHEDULES = "remove_schedules"
    ADD_VOLUMES = "add_volumes"
    REMOVE_VOLUMES = "remove_volumes"


class LifecyclePolicyGetAction(str, Enum):
    GET_LIST = "get_list"
    GET_BY_ID = "get_by_id"


class CloudLifecyclePolicyClient(BaseResourceClient):
    RESOURCE = "lifecycle_policy"

    ACTION_CONFIG = {
        LifecyclePolicyGetAction.GET_LIST: {
            "method": "get",
            "schemas": {
                "query_params": GetLifecyclePolicyList,
            },
        },
        LifecyclePolicyGetAction.GET_BY_ID: {
            "method": "get",
            "path": "{lifecycle_policy_id}",
            "schemas": {
                "path_params": LifecyclePolicyId,
                "query_params": GetLifecyclePolicyList,
            },
        },
        LifecyclePolicyManageAction.CREATE: {
            "method": "post",
            "schemas": {
                "data": CreateLifecyclePolicy,
            },
        },
        LifecyclePolicyManageAction.UPDATE: {
            "method": "patch",
            "path": "{lifecycle_policy_id}",
            "schemas": {
                "path_params": LifecyclePolicyId,
                "data": UpdateLifecyclePolicy,
            },
        },
        LifecyclePolicyManageAction.DELETE: {
            "method": "delete",
            "path": "{lifecycle_policy_id}",
            "schemas": {
                "path_params": LifecyclePolicyId,
            },
        },
        LifecyclePolicyManageAction.ADD_SCHEDULES: {
            "method": "post",
            "path": "{lifecycle_policy_id}/add_schedules",
            "schemas": {
                "path_params": LifecyclePolicyId,
                "data": AddSchedules,
            },
        },
        LifecyclePolicyManageAction.REMOVE_SCHEDULES: {
            "method": "post",
            "path": "{lifecycle_policy_id}/remove_schedules",
            "schemas": {
                "path_params": LifecyclePolicyId,
                "data": RemoveSchedule,
            },
        },
        LifecyclePolicyManageAction.ADD_VOLUMES: {
            "method": "put",
            "path": "{lifecycle_policy_id}/add_volumes_to_policy",
            "schemas": {
                "path_params": LifecyclePolicyId,
                "data": AddVolumes,
            },
        },
        LifecyclePolicyManageAction.REMOVE_VOLUMES: {
            "method": "put",
            "path": "{lifecycle_policy_id}/remove_volumes_from_policy",
            "schemas": {
                "path_params": LifecyclePolicyId,
                "data": RemoveVolumes,
            },
        },
    }
