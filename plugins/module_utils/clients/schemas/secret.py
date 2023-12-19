from dataclasses import dataclass
from enum import Enum
from typing import Optional

from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.base import (
    BaseSchema,
)


class SecretType(str, Enum):
    symmetric = "symmetric"
    public = "public"
    private = "private"
    passphrase = "passphrase"
    certificate = "certificate"
    opaque = "opaque"


@dataclass
class CreateSecret(BaseSchema):
    name: str
    payload: str
    payload_content_encoding: str
    payload_content_type: str
    secret_type: SecretType
    algorithm: Optional[str] = None
    bit_length: Optional[int] = None
    expiration: Optional[str] = None
    mode: Optional[str] = None


@dataclass
class SecretId(BaseSchema):
    secret_id: str
