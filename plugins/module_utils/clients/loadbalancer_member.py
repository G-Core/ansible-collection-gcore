from enum import Enum

from ansible_collections.gcore.cloud.plugins.module_utils.clients.base import (
    BaseResourceClient,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.loadbalancer_member import (
    CreateLbPoolMember,
    DeleteLbPoolMember,
    LbPoolId,
)


class LbPoolMemeberManageAction(str, Enum):
    CREATE = "create"
    DELETE = "delete"


class CloudLbPoolMemberClient(BaseResourceClient):
    RESOURCE = "member"

    ACTION_CONFIG = {
        LbPoolMemeberManageAction.CREATE: {
            "method": "post",
            "path": "{loadbalancer_pool_id}/member",
            "as_task": True,
            "timeout": 2400,
            "schemas": {
                "path_params": LbPoolId,
                "data": CreateLbPoolMember,
            },
        },
        LbPoolMemeberManageAction.DELETE: {
            "method": "delete",
            "path": "{loadbalancer_pool_id}/member/{loadbalancer_pool_member_id}",
            "as_task": True,
            "timeout": 1200,
            "schemas": {
                "path_params": DeleteLbPoolMember,
            },
        },
    }
