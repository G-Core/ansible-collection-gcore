from dataclasses import dataclass
from enum import Enum
from typing import Optional

from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.base import (
    BaseSchema,
)


class NetworkType(str, Enum):
    VLAN = "vlan"
    VXLAN = "vxlan"


@dataclass
class CreateNetwork(BaseSchema):
    name: str
    create_router: Optional[bool] = None
    type: Optional[NetworkType] = None
    metadata: Optional[dict] = None


@dataclass
class UpdateNetwork(BaseSchema):
    name: str


@dataclass
class NetworkId(BaseSchema):
    network_id: str


@dataclass
class GetNetworkList(BaseSchema):
    order_by: Optional[str] = None
    offset: Optional[int] = None
    limit: Optional[int] = None
    metadata_kv: Optional[str] = None
    metadata_k: Optional[str] = None
