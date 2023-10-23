from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from .base import BaseResource


class VolumeSourceEnum(str, Enum):
    NEW_VOLUME = "new-volume"
    IMAGE = "image"
    SNAPSHOT = "snapshot"


@dataclass
class CreateVolume(BaseResource):
    # required
    name: str
    size: int

    source: str = VolumeSourceEnum.NEW_VOLUME.value
    type_name: str = "standard"

    # optional
    instance_id_to_attach_to: Optional[str] = None
    attachment_tag: Optional[str] = None
    lifecycle_policy_ids: Optional[List[int]] = None
    metadata: Optional[dict] = None


class CreateVolumeFromImage(CreateVolume):
    image_id: str
    source: str = VolumeSourceEnum.IMAGE.value


class CreateVolumeFromSnapshot(CreateVolume):
    snapshot_id: str
    source: str = VolumeSourceEnum.SNAPSHOT.value


@dataclass
class UpdateVolume(BaseResource):
    volume_id: str
    name: str


@dataclass
class DeleteVolume(BaseResource):
    volume_id: str


@dataclass
class AttachVolume(BaseResource):
    volume_id: str
    instance_id: str


@dataclass
class DetachVolume(BaseResource):
    volume_id: str
    instance_id: str


@dataclass
class ExtendVolume(BaseResource):
    volume_id: str
    size: int


@dataclass
class RetypeVolume(BaseResource):
    volume_type: str
