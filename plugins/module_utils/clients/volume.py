from enum import Enum

from ansible.module_utils.basic import AnsibleModule

from .base import BaseResourceClient
from .schemas.volume import (
    AttachVolume,
    CreateVolume,
    CreateVolumeFromImage,
    CreateVolumeFromSnapshot,
    DeleteVolume,
    DetachVolume,
    ExtendVolume,
    RetypeVolume,
    UpdateVolume,
)


class VolumeActionEnum(str, Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    ATTACH = "attach"
    DETACH = "detach"
    EXTEND = "extend"
    RETYPE = "retype"


class GCoreVolumeClient(BaseResourceClient):
    def __init__(self, module: AnsibleModule, url: str) -> None:
        super().__init__(module, url)

    def get_list(self, **kwargs) -> list:
        return self.api_client.get(self.url, **kwargs)

    def get_by_id(self, resource_id: str, **kwargs) -> dict:
        return self.api_client.get(self.url, path=resource_id, **kwargs)

    def get_first_by_filters(self, **kwargs):
        resources = self.api_client.get(self.url, **kwargs)
        return resources["results"][0] if resources.get("count") else None

    def get_by_name(self, name: str):
        return self.get_first_by_filters(query={"part_name": name})

    def do_action(self, command: str, params: dict):
        action_method, schema = self._get_method_and_schema(command)
        if command == VolumeActionEnum.CREATE.value:
            schema = schema.get(params.get("source"))
        self.module.fail_on_missing_params(required_params=schema.get_required())
        data = schema.init_as_dict(params)
        return action_method(data)

    def _create(self, data: dict):
        return self.api_client.post(url=self.url, data=data)

    def _update(self, data: dict):
        volume_id = data.pop("volume_id")
        return self.api_client.patch(url=self.url, path=volume_id, data=data)

    def _delete(self, data: dict):
        volume_id = data.get("volume_id")
        return self.api_client.delete(url=self.url, path=volume_id)

    def _attach(self, data: dict):
        volume_id = data.pop("volume_id")
        return self.api_client.post(url=self.url, path=volume_id, data=data)

    def _detach(self, data: dict):
        volume_id = data.pop("volume_id")
        return self.api_client.post(url=self.url, path=volume_id, data=data)

    def _extend(self, data: dict):
        volume_id = data.pop("volume_id")
        return self.api_client.post(url=self.url, path=volume_id, data=data)

    def _retype(self, data: dict):
        volume_id = data.pop("volume_id")
        return self.api_client.post(url=self.url, path=volume_id, data=data)

    def _get_method_and_schema(self, command: str) -> tuple:
        mapping = {
            "create": {
                "method": self._create,
                "schema": {
                    "new-volume": CreateVolume,
                    "image": CreateVolumeFromImage,
                    "snapshot": CreateVolumeFromSnapshot,
                },
            },
            "update": {
                "method": self._update,
                "schema": UpdateVolume,
            },
            "delete": {
                "method": self._delete,
                "schema": DeleteVolume,
            },
            "attach": {
                "method": self._attach,
                "schema": AttachVolume,
            },
            "detach": {
                "method": self._detach,
                "schema": DetachVolume,
            },
            "extend": {
                "method": self._extend,
                "schema": ExtendVolume,
            },
            "retype": {
                "method": self._retype,
                "schema": RetypeVolume,
            },
        }
        mapped = mapping.get(command)
        return mapped["method"], mapped["schema"]
