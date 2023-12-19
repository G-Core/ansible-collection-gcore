from enum import Enum

from ansible_collections.gcore.cloud.plugins.module_utils.clients.base import (
    BaseResourceClient,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.securitygroup import (
    SecurityGroupId,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.securitygroup_rule import (
    CreateSecurityGroupRule,
    SecurityGroupRuleId,
)


class SecurityGroupRuleManageAction(str, Enum):
    CREATE = "create"
    DELETE = "delete"


class CloudSecurityGroupRuleClient(BaseResourceClient):
    RESOURCE = "securitygroup_rule"

    ACTION_CONFIG = {
        SecurityGroupRuleManageAction.CREATE: {
            "method": "post",
            "path": "{securitygroup_id}/rules",
            "schemas": {
                "path_params": SecurityGroupId,
                "data": CreateSecurityGroupRule,
            },
        },
        SecurityGroupRuleManageAction.DELETE: {
            "method": "delete",
            "url": "v1/securitygrouprules/",
            "path": "{securitygroup_rule_id}",
            "schemas": {
                "path_params": SecurityGroupRuleId,
            },
        },
    }
