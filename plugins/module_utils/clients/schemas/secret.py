from dataclasses import dataclass
from typing import Optional

from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.base import (
    BaseSchema,
)


@dataclass
class CreateSecret(BaseSchema):
    name: str
    payload: dict
    expiration: Optional[str] = None


@dataclass
class SecretId(BaseSchema):
    secret_id: str
