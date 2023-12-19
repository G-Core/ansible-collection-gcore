from dataclasses import dataclass
from typing import Optional

from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.base import (
    BaseSchema,
)


@dataclass
class CreateKeypair(BaseSchema):
    sshkey_name: str
    public_key: Optional[str] = None
    shared_in_project: Optional[bool] = None


@dataclass
class ShareKeypair(BaseSchema):
    shared_in_project: bool


@dataclass
class KeypairId(BaseSchema):
    keypair_id: str
