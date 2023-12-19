from enum import Enum

from ansible_collections.gcore.cloud.plugins.module_utils.clients.base import (
    BaseResourceClient,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.securitygroup import (
    CopySecurityGroup,
    CreateSecurityGroup,
    GetSecurityGroupList,
    SecurityGroupId,
    UpdateSecurityGroup,
)


class SecurityGroupManageAction(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    COPY = "copy"


class SecurityGroupGetAction(str, Enum):
    GET_LIST = "get_list"
    GET_BY_ID = "get_by_id"


class CloudSecurityGroupClient(BaseResourceClient):
    RESOURCE = "securitygroup"

    ACTION_CONFIG = {
        SecurityGroupGetAction.GET_LIST: {
            "method": "get",
            "schemas": {
                "query_params": GetSecurityGroupList,
            },
        },
        SecurityGroupGetAction.GET_BY_ID: {
            "method": "get",
            "path": "{securitygroup_id}",
            "schemas": {
                "path_params": SecurityGroupId,
            },
        },
        SecurityGroupManageAction.CREATE: {
            "method": "post",
            "schemas": {
                "data": CreateSecurityGroup,
            },
        },
        SecurityGroupManageAction.UPDATE: {
            "method": "patch",
            "path": "{securitygroup_id}",
            "schemas": {
                "path_params": SecurityGroupId,
                "data": UpdateSecurityGroup,
            },
        },
        SecurityGroupManageAction.DELETE: {
            "method": "delete",
            "path": "{securitygroup_id}",
            "schemas": {
                "path_params": SecurityGroupId,
            },
        },
        SecurityGroupManageAction.COPY: {
            "method": "post",
            "path": "{securitygroup_id}/copy",
            "schemas": {
                "path_params": SecurityGroupId,
                "data": CopySecurityGroup,
            },
        },
    }
