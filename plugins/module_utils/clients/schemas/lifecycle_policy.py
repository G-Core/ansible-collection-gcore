from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.base import (
    BaseSchema,
)


class LifecyclePolicyAction(str, Enum):
    VOLUME_SNAPSHOT = "volume_snapshot"


class LifecyclePolicyStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"


@dataclass
class CreateLifecyclePolicy(BaseSchema):
    name: str
    action: LifecyclePolicyAction
    volume_ids: Optional[List[str]] = None
    schedules: Optional[List[dict]] = None
    status: Optional[LifecyclePolicyStatus] = None


@dataclass
class UpdateLifecyclePolicy(BaseSchema):
    name: Optional[str] = None
    status: Optional[LifecyclePolicyStatus] = None


@dataclass
class AddSchedules(BaseSchema):
    schedules: List[dict]


@dataclass
class RemoveSchedule(BaseSchema):
    schedule_ids: List[str]


@dataclass
class AddVolumes(BaseSchema):
    volume_ids: List[str]


@dataclass
class RemoveVolumes(BaseSchema):
    volume_ids: List[str]


@dataclass
class GetLifecyclePolicyList(BaseSchema):
    need_volumes: Optional[bool] = None


@dataclass
class LifecyclePolicyId(BaseSchema):
    lifecycle_policy_id: str
