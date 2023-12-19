from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.base import (
    BaseSchema,
)


class LbListenerProtocol(str, Enum):
    HTTP = "HTTP"
    HTTPS = "HTTPS"
    TCP = "TCP"
    UDP = "UDP"
    TERMINATED_HTTPS = "TERMINATED_HTTPS"
    PROMETHEUS = "PROMETHEUS"


@dataclass
class CreateLbListener(BaseSchema):
    name: str
    protocol: LbListenerProtocol
    protocol_port: int
    loadbalancer_id: str
    insert_x_forwarded: Optional[bool] = None
    secret_id: Optional[str] = None
    sni_secret_id: Optional[List[str]] = None
    allowed_cidrs: Optional[List[str]] = None


@dataclass
class UpdateLbListener(BaseSchema):
    name: Optional[str] = None
    secret_id: Optional[str] = None
    sni_secret_id: Optional[str] = None
    allowed_cidrs: Optional[List[str]] = None


@dataclass
class GetLbListener(BaseSchema):
    show_stats: Optional[bool] = None


@dataclass
class GetLbListenerList(GetLbListener):
    loadbalancer_id: Optional[str] = None


@dataclass
class LbListenerId(BaseSchema):
    loadbalancer_listener_id: str
