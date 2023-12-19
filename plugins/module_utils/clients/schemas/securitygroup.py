from dataclasses import dataclass
from typing import List, Optional

from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.base import (
    BaseSchema,
)


@dataclass
class CreateSecurityGroup(BaseSchema):
    security_group: dict
    instances: Optional[List[str]] = None


@dataclass
class UpdateSecurityGroup(BaseSchema):
    name: Optional[str] = None
    changed_rules: Optional[List[dict]] = None


@dataclass
class CopySecurityGroup(BaseSchema):
    name: str


@dataclass
class GetSecurityGroupList(BaseSchema):
    metadata_kv: Optional[str] = None
    metadata_v: Optional[str] = None


@dataclass
class SecurityGroupId(BaseSchema):
    securitygroup_id: str
