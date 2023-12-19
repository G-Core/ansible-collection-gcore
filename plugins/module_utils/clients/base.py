from string import Formatter
from time import sleep
from typing import Optional

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.gcore.cloud.plugins.module_utils.api import CloudAPIClient
from ansible_collections.gcore.cloud.plugins.module_utils.exceptions import (
    ValidationError,
)

GLOBAL_PARAMS = [
    "api_host",
    "api_key",
    "api_timeout",
    "project_id",
    "region_id",
    "project_name",
    "region_name",
]


class BaseResourceClient:
    ACTION_CONFIG = {}
    RESOURCE: str

    def __init__(self, module: AnsibleModule, url: str) -> None:
        self.module = module
        self.url = url
        self.api_client = CloudAPIClient(module)
        self.response = {"changed": False, "data": None}

    def get_by_id(self, resource_id: str, **kwargs):
        return self.api_client.get(self.url, path_params=resource_id, **kwargs)

    def execute_command(self, command: str):
        config = self.ACTION_CONFIG[command]
        kwargs = self._prepare_command_kwargs(config)
        http_method = getattr(self.api_client, config["method"])
        kwargs["url"] = self.ACTION_CONFIG[command].get("url") or self.url

        response = http_method(**kwargs)

        if config.get("as_task"):
            response = self._parse_response_as_task(response, command)

        if http_method in (
            "post",
            "put",
            "patch",
            "delete",
        ):
            self.response["changed"] = True

        self.response["data"] = response
        return self.response

    def _prepare_command_kwargs(self, config: dict):
        kwargs = {}
        params = self._clear_params(self.module.params)

        schemas = config.get("schemas")
        if schemas:
            first_key = next(iter(schemas))
            if isinstance(schemas[first_key], dict):
                key = "type" if self.RESOURCE == "port" else "source"
                schemas = schemas.get(params.get(key, "default"))
            allow_none = config.get("allow_none")

            if schemas.get("query_params"):
                kwargs["query_params"] = self._init_schema(schemas.get("query_params"), params)

            path_params = {}
            if schemas.get("path_params"):
                path_params = self._init_schema(schemas.get("path_params"), params)
            kwargs["path_params"] = self._prepare_path(config.get("path"), path_params)

            if schemas.get("data"):
                kwargs["data"] = self._init_schema(
                    schemas.get("data"),
                    params,
                    allow_none=allow_none,
                )

        return kwargs

    def _parse_response_as_task(self, response: dict, command: str):
        tasks_id = self._get_task_id_from_response(response)
        task_info = self._wait_from_task(tasks_id)
        resource_id = None
        if command in ("delete",):
            postfix = "uuid" if self.RESOURCE in ("instance",) else "id"
            resource_id = task_info["data"][f"{self.RESOURCE}_{postfix}"]
            return {f"{self.RESOURCE}_id": resource_id}
        if command in (
            "create",
            "download",
        ):
            resource_id = task_info["created_resources"][f"{self.RESOURCE}s"][0]
        elif command in ("extend", "revert", "attach", "detach"):
            resource_id = task_info["data"][f"{self.RESOURCE}_id"]
        if resource_id:
            return self.get_by_id(resource_id=resource_id)

    def _init_schema(self, schema, params, allow_none: Optional[list] = None):
        self._check_requierd_params(required_params=schema.get_required())
        try:
            return schema.init_as_dict(**params, allow_none=allow_none)
        except ValidationError as exc:
            self.module.fail_json(msg=exc.message)

    def _check_requierd_params(self, required_params):
        missing = [param for param in required_params if self.module.params.get(param) is None]
        if missing:
            self.module.fail_json(msg=f"missing required arguments: {', '.join(missing)}")

    def _get_task_id_from_response(self, response: dict):
        tasks = response.get("tasks")
        if not tasks:
            self.module.fail_json(msg="Failed to get task from response operation.")
        return tasks[0]

    def _wait_from_task(self, task_id: str, expected_status: str = "FINISHED", timeout: int = 180):
        for _ in range(0, timeout, 2):  # pylint: disable=C0104
            response = self.api_client.get(url=f"v1/tasks/{task_id}", include_project_region=False)
            if response["state"] in ("NEW", "RUNNING"):
                sleep(2)
                continue
            if response["state"] != expected_status:
                self.module.fail_json(
                    msg=f"Task {response['task_type']} in state: {response['state']}. Reason={response['error']}"
                )
            return response
        self.module.fail_json(msg="The operation could not be completed within the allotted time.")

    def _prepare_path(self, path: Optional[str] = None, data: Optional[dict] = None) -> str:
        path = path or ""
        path_params = [f for _, f, _, _ in Formatter().parse(path) if f is not None]  # pylint: disable=C0104
        if path and not path_params:
            return path
        params = {k: data.pop(k) for k in path_params}
        return path.format(**params)

    def _clear_params(self, params: dict) -> dict:
        return {k: v for k, v in params.items() if k not in GLOBAL_PARAMS}
