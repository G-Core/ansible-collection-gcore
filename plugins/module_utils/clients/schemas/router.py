from dataclasses import dataclass
from typing import List, Optional

from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.base import (
    BaseSchema,
)


@dataclass
class CreateRouter(BaseSchema):
    name: str
    external_gateway_info: Optional[dict] = None
    interfaces: Optional[List[dict]] = None
    routes: Optional[List[dict]] = None


@dataclass
class UpdateRouter(BaseSchema):
    name: str
    external_gateway_info: Optional[dict] = None
    routes: Optional[List[dict]] = None


@dataclass
class AttachRouter(BaseSchema):
    subnet_id: str


@dataclass
class DetachRouter(BaseSchema):
    subnet_id: str


@dataclass
class GetRouterList(BaseSchema):
    limit: Optional[int] = None
    offset: Optional[int] = None


@dataclass
class RouterId(BaseSchema):
    router_id: str
