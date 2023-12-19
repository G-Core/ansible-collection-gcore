from enum import Enum

from ansible_collections.gcore.cloud.plugins.module_utils.clients.base import (
    BaseResourceClient,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.secret import (
    CreateSecret,
    SecretId,
)


class SecretManageAction(str, Enum):
    CREATE = "create"
    DELETE = "delete"


class SecretkGetAction(str, Enum):
    GET_LIST = "get_list"
    GET_BY_ID = "get_by_id"


class CloudSecretClient(BaseResourceClient):
    RESOURCE = "secret"

    ACTION_CONFIG = {
        SecretkGetAction.GET_LIST: {
            "method": "get",
        },
        SecretkGetAction.GET_BY_ID: {
            "method": "get",
            "path": "{secret_id}",
            "schemas": {
                "path_params": SecretId,
            },
        },
        SecretManageAction.CREATE: {
            "method": "post",
            "as_task": True,
            "timeout": 1000,
            "schemas": {
                "data": CreateSecret,
            },
        },
        SecretManageAction.DELETE: {
            "method": "delete",
            "path": "{secret_id}",
            "as_task": True,
            "timeout": 1200,
            "schemas": {
                "path_params": SecretId,
            },
        },
    }
