from string import Formatter

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.gcore.cloud.plugins.module_utils.api import GCoreAPIClient

GLOBAL_PARAMS = ["api_host", "api_token", "api_timeout", "project_id", "region_id"]


class BaseResourceClient:
    ACTION_CONFIG = {}

    def __init__(self, module: AnsibleModule, url: str) -> None:
        self.module = module
        self.url = url
        self.api_client = GCoreAPIClient(module)

    def get_by_id(self, resource_id: str, **kwargs) -> dict:
        return self.api_client.get(self.url, path=resource_id, **kwargs)

    def get_list(self, **kwargs) -> list:
        kwargs["query"] = self._clear_params(kwargs)
        return self.api_client.get(self.url, **kwargs)

    def execute_command(self, command: str, params: dict):
        config = self.ACTION_CONFIG.get(command)
        if not config:
            self.module.fail_json(msg=f"Unknown command {command}")
        self.module.fail_on_missing_params(required_params=config.get("required_params", []))
        data = self._clear_params(params)
        path = self._prepare_path(config["path"], data)
        method = getattr(self.api_client, config["method"])
        url = config.get("url") or self.url
        return method(url=url, path=path, data=data)

    def _prepare_path(self, path: str, data: dict) -> str:
        path_params = [f for _, f, _, _ in Formatter().parse(path) if f is not None]
        params = {k: data.pop(k) for k in path_params}
        return path.format(**params)

    def _clear_params(self, params: dict) -> dict:
        return {k: v for k, v in params.items() if k not in GLOBAL_PARAMS and v is not None}
