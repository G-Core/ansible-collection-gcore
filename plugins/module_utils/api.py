from http import HTTPStatus
from typing import Any, Optional
from urllib.parse import urlencode, urljoin

from ansible.module_utils.basic import AnsibleModule, json
from ansible.module_utils.urls import fetch_url, to_text


class CloudAPIClient:
    def __init__(self, module: AnsibleModule) -> None:
        self.module = module
        self.api_key = module.params["api_key"]
        self.api_timeout = module.params["api_timeout"]
        self.api_host = self._set_api_host()
        self.project_id = self._set_project_id()
        self.region_id = self._set_region_id()

    def get(
        self,
        url: str,
        path_params: Optional[str] = None,
        query_params: Optional[dict] = None,
        **kwargs,
    ) -> Optional[str]:
        kwargs.pop("data", None)
        return self._request(url=url, path_params=path_params, query_params=query_params, data=None, **kwargs)

    def post(self, url: str, **kwargs) -> Optional[str]:
        return self._request(method="POST", url=url, **kwargs)

    def patch(self, url: str, **kwargs) -> Optional[str]:
        return self._request(method="PATCH", url=url, **kwargs)

    def delete(self, url: str, **kwargs) -> Optional[str]:
        kwargs.pop("data", None)
        return self._request(method="DELETE", url=url, data=None, **kwargs)

    def _request(
        self,
        url: str,
        method: str = "GET",
        path_params: Optional[str] = None,
        query_params: Optional[dict] = None,
        data: Optional[dict] = None,
        **kwargs,
    ):
        url = f"{self.api_host}{url}"
        if kwargs.get("include_project_region", True):
            url += f"{self.project_id}/{self.region_id}"
        data = self.module.jsonify(data) if data else None
        if path_params:
            url = urljoin(url + "/", path_params)
        if query_params:
            query_str = urlencode(query_params)
            url = f"{url}?{query_str}"
        response, info = fetch_url(
            module=self.module,
            url=url,
            method=method,
            data=data,
            headers=self._get_headers(),
            timeout=self.api_timeout,
        )
        return self._parse_response(response, info)

    def _set_project_id(self):
        project_id = self.module.params.get("project_id")
        if project_id:
            return project_id
        project_name = self.module.params["project_name"]
        response, info = fetch_url(
            self.module, url=f"{self.api_host}v1/projects", method="GET", headers=self._get_headers()
        )
        for project in self._parse_response(response, info):
            if project["name"] == project_name:
                return project["id"]
            self.module.fail_json(f"Project {project_name} not found")

    def _set_region_id(self):
        region_id = self.module.params.get("region_id")
        if region_id:
            return region_id
        region_name = self.module.params["region_name"]
        response, info = fetch_url(
            self.module, url=f"{self.api_host}v1/regions", method="GET", headers=self._get_headers()
        )
        for project in self._parse_response(response, info):
            if project["display_name"] == region_name:
                return project["id"]
        self.module.fail_json(f"Region {region_name} not found")

    def _set_project_and_region(self):
        params = [("project", "name"), ("region", "disply_name")]
        for param in params:
            type_, name_ = param
            if not self.module.params.get(f"{type_}_id"):
                name = self.module.params.get(f"{type_}_name")
                response = self.get(url=f"v1/{type_}s", build_url=False)
                for item in response:
                    if item[name_] == name:
                        return item["id"]
                self.module.fail_json(msg=f"{type_.upper()} '{name}' not found. {response}")

    def _set_api_host(self) -> str:
        api_host = self.module.params["api_host"]
        return api_host + "/" if not api_host.endswith("/") else api_host

    def _get_headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "Authorization": f"APIKey {self.api_key}",
        }

    def _parse_response(self, response: Any, info: dict) -> Optional[str]:
        """Parse the API response based on the HTTP status code"""
        status_code = info["status"]
        if status_code == HTTPStatus.OK:
            response = self._parse_successful_response(response)
        elif status_code == HTTPStatus.NO_CONTENT:
            return None
        else:
            self._handle_failed_response(info)
        return self.module.from_json(to_text(response, errors="surrogate_or_strict"))

    def _parse_successful_response(self, response: Any) -> Optional[str]:
        response_text = response.read()

        if response_text:
            response_json = self._get_response_json(response_text)
            return json.dumps(response_json, ensure_ascii=False)
        return None

    def _get_response_json(self, response_text: str) -> dict:
        response = json.loads(to_text(response_text))
        if "results" in response:
            return response["results"]
        return response

    def _handle_failed_response(self, info: dict) -> None:
        """Handle a failed API request by reporting an error"""
        error_message = f"Failed to request API {info.get('url')}"
        body = json.loads(info.get("body", "{}"))
        message_error = body.get("message", "")
        self.module.fail_json(msg=error_message, message_error=message_error)
