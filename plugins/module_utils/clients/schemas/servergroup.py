from dataclasses import dataclass
from enum import Enum

from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.base import (
    BaseSchema,
)


class ServerGroupPolicy(str, Enum):
    affinity = "affinity"
    anti_affinity = "anti-affinity"
    soft_anti_affinity = "soft-anti-affinity"


@dataclass
class CreateServerGroup(BaseSchema):
    name: str
    policy: ServerGroupPolicy


@dataclass
class ServerGroupId(BaseSchema):
    servergroup_id: str
