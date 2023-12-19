from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.base import (
    BaseSchema,
)


class LbPoolAlgorithm(str, Enum):
    ROUND_ROBIN = "ROUND_ROBIN"
    LEAST_CONNECTIONS = "LEAST_CONNECTIONS"
    SOURCE_IP = "SOURCE_IP"
    SOURCE_IP_PORT = "SOURCE_IP_PORT"


class LbPoolProtocol(str, Enum):
    HTTP = "HTTP"
    HTTPS = "HTTPS"
    PROXY = "PROXY"
    TCP = "TCP"
    UDP = "UDP"


@dataclass
class CreateLbPool(BaseSchema):
    name: str
    lb_algorithm: LbPoolAlgorithm
    protocol: LbPoolProtocol
    loadbalancer_id: Optional[str] = None
    listener_id: Optional[str] = None
    members: Optional[List[dict]] = None
    healthmonitor: Optional[dict] = None
    session_persistence: Optional[dict] = None
    timeout_client_data: Optional[int] = None
    timeout_member_connect: Optional[int] = None
    timeout_member_data: Optional[int] = None


@dataclass(kw_only=True)
class UpdateLbPool(CreateLbPool):
    id: Optional[str] = None
    name: Optional[str] = None
    protocol: Optional[LbPoolProtocol] = None


@dataclass
class GetLbPoolList(BaseSchema):
    loadbalancer_id: Optional[str] = None
    listener_id: Optional[str] = None
    details: Optional[bool] = None


@dataclass
class LbPoolId(BaseSchema):
    loadbalancer_pool_id: str
