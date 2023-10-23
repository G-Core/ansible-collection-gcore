from ansible.module_utils.basic import AnsibleModule

from ..api import GCoreAPIClient
from .base import BaseResourceClient


class GCoreImageClient(BaseResourceClient):
    def __init__(self, module: AnsibleModule, url: str) -> None:
        super().__init__(module, url)

    def get_list(self, **kwargs) -> list:
        return self.api_client.get(self.url, **kwargs)

    def get_by_id(self, resource_id: str, **kwargs) -> dict:
        return self.api_client.get(self.url, path=resource_id, **kwargs)
