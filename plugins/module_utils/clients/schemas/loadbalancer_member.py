from dataclasses import dataclass
from typing import Optional

from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.base import (
    BaseSchema,
)


@dataclass
class CreateLbPoolMember(BaseSchema):
    protocol_port: int
    address: str
    id: Optional[str] = None
    operating_status: Optional[str] = None
    subnet_id: Optional[str] = None
    instance_id: Optional[str] = None
    admin_state_up: Optional[bool] = None
    weight: Optional[int] = None
    monitor_address: Optional[str] = None
    monitor_port: Optional[int] = None


@dataclass
class LbPoolMemeberId(BaseSchema):
    loadbalancer_pool_member_id: str


@dataclass
class LbPoolId(BaseSchema):
    loadbalancer_pool_id: str


@dataclass
class DeleteLbPoolMember(LbPoolMemeberId, LbPoolId):
    pass
