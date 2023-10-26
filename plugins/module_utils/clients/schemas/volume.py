from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.base import (
    BaseResource,
)


class VolumeSource(str, Enum):
    NEW_VOLUME = "new-volume"
    IMAGE = "image"
    SNAPSHOT = "snapshot"


class VolumeType(str, Enum):
    STANDARD = "standard"
    SSD_HIIOPS = "ssd_hiiops"
    COLD = "cold"
    ULTRA = "ultra"


@dataclass
class CreateVolume(BaseResource):
    name: str
    size: int
    source: VolumeSource = VolumeSource.NEW_VOLUME
    type_name: VolumeType = VolumeType.STANDARD
    instance_id_to_attach_to: Optional[str] = None
    attachment_tag: Optional[str] = None
    lifecycle_policy_ids: Optional[List[int]] = None
    metadata: Optional[dict] = None


class CreateVolumeFromImage(CreateVolume):
    image_id: str
    source: VolumeSource = VolumeSource.IMAGE


class CreateVolumeFromSnapshot(CreateVolume):
    snapshot_id: str
    source: VolumeSource = VolumeSource.SNAPSHOT


@dataclass
class UpdateVolume(BaseResource):
    volume_id: str
    name: str


@dataclass
class DeleteVolume(BaseResource):
    volume_id: str


@dataclass
class VolumeInstanceAction(BaseResource):
    volume_id: str
    instance_id: str


@dataclass
class ExtendVolume(BaseResource):
    volume_id: str
    size: int


@dataclass
class RetypeVolume(BaseResource):
    volume_id: str
    volume_type: str
