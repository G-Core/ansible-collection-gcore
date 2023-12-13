from dataclasses import dataclass
from enum import Enum
from typing import Optional

from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.base import (
    BaseSchema,
)


class SshKey(str, Enum):
    allow = "allow"
    deny = "deny"
    required = "required"


class ImageOsType(str, Enum):
    linux = "linux"
    windows = "windows"


class ImageHwFirmwareType(str, Enum):
    bios = "bios"
    uefi = "uefi"


class HwMachineType(str, Enum):
    i440 = "i440"
    q35 = "q35"


class ImageArchitectureType(str, Enum):
    aarch64 = "aarch64"
    x86_64 = "x86_64"


@dataclass
class BaseCreateImage(BaseSchema):
    name: str
    ssh_key: Optional[SshKey] = None
    is_baremetal: Optional[bool] = None
    os_type: Optional[ImageOsType] = None
    hw_firmware_type: Optional[ImageHwFirmwareType] = None
    hw_machine_type: Optional[HwMachineType] = None
    architecture: Optional[ImageArchitectureType] = None
    metadata: Optional[dict] = None


@dataclass(kw_only=True)
class CreateImageFromVolume(BaseCreateImage):
    volume_id: str


@dataclass(kw_only=True)
class DownloadImage(BaseCreateImage):
    url: str
    cow_format: Optional[bool] = None
    os_distro: Optional[str] = None
    os_version: Optional[str] = None


@dataclass
class UpdateImage(BaseSchema):
    name: Optional[str] = None
    ssh_key: Optional[SshKey] = None
    is_baremetal: Optional[bool] = None
    os_type: Optional[ImageOsType] = None
    hw_firmware_type: Optional[ImageHwFirmwareType] = None
    hw_machine_type: Optional[HwMachineType] = None
    metadata: Optional[dict] = None


@dataclass
class ImageId(BaseSchema):
    image_id: str


@dataclass
class GetImageList(BaseSchema):
    visibility: Optional[str] = None
    private: Optional[str] = None
    metadata_k: Optional[str] = None
    metadata_kv: Optional[str] = None
    include_prices: Optional[bool] = None
