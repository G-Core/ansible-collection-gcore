from dataclasses import dataclass
from typing import List, Optional

from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.base import (
    BaseSchema,
)


@dataclass
class CreateSubnet(BaseSchema):
    name: str
    network_id: str
    cidr: str
    enable_dhcp: Optional[bool] = None
    connect_to_network_router: Optional[bool] = None
    dns_nameservers: Optional[List[str]] = None
    host_routes: Optional[List[dict]] = None
    gateway_ip: Optional[str] = None
    metadata: Optional[dict] = None


@dataclass
class UpdateSubnet(BaseSchema):
    name: Optional[str] = None
    dns_nameservers: Optional[List[str]] = None
    enable_dhcp: Optional[bool] = None
    gateway_ip: Optional[str] = None
    host_routes: Optional[List[dict]] = None


@dataclass
class GetSubnetList(BaseSchema):
    network_id: Optional[str] = None
    metadata_kv: Optional[str] = None
    metadata_k: Optional[str] = None
    limit: Optional[int] = None
    offset: Optional[int] = None


@dataclass
class SubnetId(BaseSchema):
    subnet_id: str
