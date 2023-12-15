from dataclasses import dataclass, field
from typing import List, Optional

from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.base import (
    BaseSchema,
)


@dataclass
class CreateInstance(BaseSchema):
    flavor: str
    interfaces: List[dict]
    volumes: List[dict]
    security_groups: Optional[List[dict]] = None
    configuration: Optional[dict] = None
    allow_app_ports: Optional[bool] = None
    names: Optional[List[str]] = None
    name_templates: Optional[List[str]] = None
    keypair_name: Optional[str] = None
    servergroup_id: Optional[str] = None
    user_data: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    metadata: Optional[dict] = None


@dataclass
class GetInstanceList(BaseSchema):
    name: Optional[str] = None
    flavor_id: Optional[str] = None
    flavor_prefix: Optional[str] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    status: Optional[str] = None
    changes_since: Optional[str] = field(default=None, metadata={"alias": "changes-since"})
    changes_before: Optional[str] = field(default=None, metadata={"alias": "changes-before"})
    ip: Optional[str] = None
    uuid: Optional[str] = None
    metadata_kv: Optional[str] = None
    metadata_v: Optional[str] = None
    order_by: Optional[str] = None
    include_ai: Optional[bool] = None
    exclude_secgroup: Optional[str] = None
    include_baremetal: Optional[bool] = None
    available_floating: Optional[str] = None
    include_k8s: Optional[bool] = None


@dataclass
class InstanceId(BaseSchema):
    instance_id: str


@dataclass
class UpdateInstance(BaseSchema):
    name: str


@dataclass
class DeleteInstance(BaseSchema):
    volumes_to_delete: Optional[str] = field(default=None, metadata={"alias": "volumes"})
    delete_floatings: Optional[bool] = None
    floatings: Optional[str] = None
    reserved_fixed_ips: Optional[str] = None


@dataclass
class StartInstance(BaseSchema):
    activate_profile: Optional[bool] = None


@dataclass
class GetInstanceQuota(BaseSchema):
    flavor: str
    volumes: List[dict]
    names: Optional[List[str]] = None
    name_templates: Optional[List[str]] = None
    interfaces: Optional[List[dict]] = None


@dataclass
class AddToServergroup(BaseSchema):
    servergroup_id: str
