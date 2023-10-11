from typing import Any, Optional

from ansible.module_utils.basic import AnsibleModule, jsonify
from ansible.module_utils.urls import fetch_url, to_text


class GCoreAPIClient:
    def __init__(self, module: AnsibleModule) -> None:
        self.module = module
        self.api_token = module.params["api_token"]
        self.api_timeout = module.params["api_timeout"]
        self.project_id = module.params["project_id"]
        self.region_id = module.params["region_id"]
        self.api_endpoint = self._set_api_endpoint()

    def get(self, url: str, **kwargs):
        return self._request(method="GET", url=url, data=None, **kwargs)

    def post(self, url: str, data: Any, **kwargs):
        return self._request(method="POST", url=url, data=data, **kwargs)

    def patch(self, url: str, data: Any, **kwargs):
        return self._request(method="PATCH", url=url, data=data, **kwargs)

    def delete(self, url: str, **kwargs):
        return self._request(method="DELETE", url=url, data=None, **kwargs)

    def _set_api_endpoint(self) -> str:
        api_endpoint = self.module.params["api_endpoint"]
        return api_endpoint + "/" if not api_endpoint.endswith("/") else api_endpoint

    def _get_headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_token}",
        }

    def _dump_query(self, query: dict):
        res = ""
        for key, value in query.items():
            if isinstance(
                value,
                (
                    list,
                    dict,
                ),
            ):
                res += f"{key}={jsonify(value)}&"
            else:
                res += f"{key}={value}&"
        res = res.removesuffix("&")
        return res

    def _build_url(self, url: str, **kwargs) -> str:
        url = url.removeprefix("/")
        if not url.endswith("/"):
            url += "/"
        handler = f"{self.api_endpoint}{url}{self.project_id}/{self.region_id}"
        resource_id = kwargs.get("resource_id")
        if resource_id:
            handler += f"/{resource_id}"
        query = kwargs.get("query")
        if query:
            query_str = self._dump_query(query)
            handler += f"?{query_str}"
        return handler

    def _parse_response(self, response, info: dict):
        status_code = info["status"]
        if status_code == 200:
            # https://docs.ansible.com/ansible/latest/reference_appendices/module_utils.html
            response = self.module.from_json(to_text(response.read(), errors="surrogate_or_strict"))
        elif status_code == 204:
            response = None
        else:
            self.module.fail_json(msg=f"Failed to request API {self.api_endpoint}", request_info=info)
        return response

    def _request(self, method: str, url: str, data: Optional[Any] = None, **kwargs):
        response, info = fetch_url(
            module=self.module,
            url=self._build_url(url, **kwargs),
            method=method,
            headers=self._get_headers(),
            data=data,
            timeout=self.api_timeout,
        )
        return self._parse_response(response, info)
