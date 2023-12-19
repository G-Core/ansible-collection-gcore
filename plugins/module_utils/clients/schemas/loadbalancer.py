from dataclasses import dataclass
from typing import List, Optional

from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.base import (
    BaseSchema,
)


@dataclass
class CreateLoadbalancer(BaseSchema):
    name: Optional[str] = None
    flavor: Optional[str] = None
    listeners: Optional[List[dict]] = None
    vip_network_id: Optional[str] = None
    vip_subnet_id: Optional[str] = None
    vip_port_id: Optional[str] = None
    floating_ip: Optional[dict] = None
    metadata: Optional[dict] = None
    tag: Optional[List[str]] = None
    logging: Optional[dict] = None
    name_template: Optional[str] = None


@dataclass
class UpdateLoadbalancer(BaseSchema):
    name: Optional[str] = None
    logging: Optional[dict] = None


@dataclass
class GetLoadbalancerList(BaseSchema):
    show_stats: Optional[bool] = None
    assigned_floating: Optional[bool] = None
    logging_enabled: Optional[bool] = None
    metadata_kv: Optional[str] = None
    metadata_k: Optional[str] = None
    offset: Optional[int] = None
    limit: Optional[int] = None


@dataclass
class LoadbalancerId(BaseSchema):
    loadbalancer_id: str


@dataclass
class GetLoadbalancer(LoadbalancerId):
    show_stats: Optional[bool] = None
