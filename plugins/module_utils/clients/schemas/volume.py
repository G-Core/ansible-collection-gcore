from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.base import (
    BaseSchema,
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
    SSD_LOCAL = "ssd_local"
    SSD_LOWLATENCY = "ssd_lowlatency"


class RetypableVolumeType(str, Enum):
    STANDARD = "standard"
    SSD_HIIOPS = "ssd_hiiops"


@dataclass
class CreateVolume(BaseSchema):
    name: str
    size: int
    source: VolumeSource
    type_name: VolumeType = VolumeType.STANDARD
    instance_id_to_attach_to: Optional[str] = None
    attachment_tag: Optional[str] = None
    lifecycle_policy_ids: Optional[List[int]] = None
    metadata: Optional[dict] = None


@dataclass(kw_only=True)
class CreateVolumeFromImage(CreateVolume):
    image_id: str
    source: VolumeSource = VolumeSource.IMAGE


@dataclass(kw_only=True)
class CreateVolumeFromSnapshot(CreateVolume):
    snapshot_id: str
    source: VolumeSource = VolumeSource.SNAPSHOT


@dataclass
class VolumeId(BaseSchema):
    volume_id: str


@dataclass
class UpdateVolume(BaseSchema):
    name: str


@dataclass
class VolumeInstanceAction(BaseSchema):
    instance_id: str


@dataclass
class ExtendVolume(BaseSchema):
    size: int


@dataclass
class RetypeVolume(BaseSchema):
    volume_type: RetypableVolumeType


@dataclass
class GetVolumeList(BaseSchema):
    instance_id: Optional[str] = None
    cluster_id: Optional[str] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    bootable: Optional[bool] = None
    has_attachments: Optional[bool] = None
    id_part: Optional[str] = None
    name_part: Optional[str] = None
    metadata_kv: Optional[str] = None
    metadata_k: Optional[str] = None


@dataclass
class DeleteVolume(BaseSchema):
    snapshots: Optional[str] = None
