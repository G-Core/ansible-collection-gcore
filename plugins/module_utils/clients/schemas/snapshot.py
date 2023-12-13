from dataclasses import dataclass
from typing import Optional

from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.base import (
    BaseSchema,
)


@dataclass
class CreateSnapshot(BaseSchema):
    volume_id: str
    name: str
    description: Optional[str] = None
    metadata: Optional[dict] = None


@dataclass
class SnapshotId(BaseSchema):
    snapshot_id: str


@dataclass
class GetSnapshotList(BaseSchema):
    volume_id: Optional[str] = None
    instance_id: Optional[str] = None
    schedule_id: Optional[str] = None
    lifecycle_policy_id: Optional[str] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
