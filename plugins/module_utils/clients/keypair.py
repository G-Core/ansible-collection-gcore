from enum import Enum

from ansible_collections.gcore.cloud.plugins.module_utils.clients.base import (
    BaseResourceClient,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.keypair import (
    CreateKeypair,
    KeypairId,
    ShareKeypair,
)


class KeypairManageAction(str, Enum):
    CREATE = "create"
    SHARE = "share"
    DELETE = "delete"


class KeypairGetAction(str, Enum):
    GET_LIST = "get_list"
    GET_BY_ID = "get_by_id"


class CloudKeypairClient(BaseResourceClient):
    RESOURCE = "keypair"

    ACTION_CONFIG = {
        KeypairGetAction.GET_LIST: {
            "method": "get",
        },
        KeypairGetAction.GET_BY_ID: {
            "method": "get",
            "path": "{keypair_id}",
            "schemas": {
                "path_params": KeypairId,
            },
        },
        KeypairManageAction.CREATE: {
            "method": "post",
            "schemas": {
                "data": CreateKeypair,
            },
        },
        KeypairManageAction.SHARE: {
            "method": "patch",
            "path": "{keypair_id}/share",
            "schemas": {
                "path_params": KeypairId,
                "data": ShareKeypair,
            },
        },
        KeypairManageAction.DELETE: {
            "method": "delete",
            "path": "{keypair_id}",
            "schemas": {
                "path_params": KeypairId,
            },
        },
    }
