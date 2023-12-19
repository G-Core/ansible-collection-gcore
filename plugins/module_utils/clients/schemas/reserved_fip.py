from dataclasses import dataclass
from enum import Enum
from typing import Optional

from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.base import (
    BaseSchema,
)


class ReservedFipType(str, Enum):
    EXTERNAL = "external"
    SUBNET = "subnet"
    ANY_SUBNET = "any_subnet"
    IP_ADDRESS = "ip_address"


@dataclass
class CreateReservedFip(BaseSchema):
    type: ReservedFipType
    is_vip: Optional[bool] = None


@dataclass(kw_only=True)
class CreateExternalReservedFip(BaseSchema):
    type: ReservedFipType = ReservedFipType.EXTERNAL


@dataclass(kw_only=True)
class CreateSubnetReservedFip(BaseSchema):
    subnet_id: str
    type: ReservedFipType = ReservedFipType.SUBNET


@dataclass(kw_only=True)
class CreateAnySubnetReservedFip(BaseSchema):
    network_id: str
    type: ReservedFipType = ReservedFipType.ANY_SUBNET


@dataclass(kw_only=True)
class CreateIpAddrReservedFip(BaseSchema):
    network_id: str
    ip_address: str
    type: ReservedFipType = ReservedFipType.IP_ADDRESS


@dataclass
class UpdateReservedFip(BaseSchema):
    is_vip: Optional[bool] = None


@dataclass
class GetReservedFipList(BaseSchema):
    external_only: Optional[bool] = None
    internal_only: Optional[bool] = None
    available_only: Optional[bool] = None
    vip_only: Optional[bool] = None
    device_id: Optional[str] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    order_by: Optional[str] = None
    ip_address: Optional[str] = None


@dataclass
class ReservedFipId(BaseSchema):
    port_id: str
