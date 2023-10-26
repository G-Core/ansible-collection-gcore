from typing import Optional

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.gcore.cloud.plugins.module_utils.api import GCoreAPIClient


class BaseResourceClient:
    def __init__(self, module: AnsibleModule, url: str) -> None:
        self.module = module
        self.url = url
        self.api_client = GCoreAPIClient(module)
        self.changed = False

    def get_by_id(self, resource_id: str, **kwargs) -> dict:
        return self.api_client.get(self.url, path=resource_id, **kwargs)

    def get_list(self, **kwargs) -> list:
        return self.api_client.get(self.url, **kwargs)
