from typing import Optional

from ansible.module_utils.basic import AnsibleModule

from ..api import GCoreAPIClient


class BaseResourceClient:
    def __init__(self, module: AnsibleModule, url: str) -> None:
        self.module = module
        self.url = url
        self.api_client = GCoreAPIClient(module)
        self.changed = False

    def get_by_id(self, resource_id: str, **kwargs) -> dict:
        pass

    def get_list(self, **kwargs) -> list:
        pass

    def get_first_by_filters(self, **kwargs) -> Optional[dict]:
        pass

    def get_by_name(self, name: str) -> Optional[dict]:
        pass