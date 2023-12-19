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
        self._set_project_and_region()

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

    def put(self, url: str, **kwargs) -> Optional[str]:
        return self._request(method="PUT", url=url, **kwargs)

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
        url = self._construct_url(
            url,
            path_params,
            query_params,
            include_project_region=kwargs.get("include_project_region", True),
        )
        data = self._prepare_data(data)
        response, info = fetch_url(
            module=self.module,
            url=url,
            method=method,
            data=data,
            headers=self._get_headers(),
            timeout=self.api_timeout,
        )
        return self._parse_response(response, info)

    def _construct_url(
        self,
        url: str,
        path_params: Optional[str] = None,
        query_params: Optional[dict] = None,
        include_project_region: bool = True,
    ) -> str:
        url = f"{self.api_host}{url}"
        if include_project_region:
            url += f"{self.project_id}/{self.region_id}"
        if query_params:
            query_str = urlencode(query_params)
            url = f"{url}?{query_str}"
        if path_params:
            url = urljoin(url + "/", path_params)
        return url

    def _prepare_data(self, data: Optional[dict]) -> Optional[str]:
        return self.module.jsonify(data) if data else None

    def _set_project_and_region(self):
        params = [("project", "name"), ("region", "display_name")]
        for type_, name_key in params:
            self._set_entity_id(type_, name_key)

    def _set_entity_id(self, entity_type: str, name_key: str):
        entity_id = f"{entity_type}_id"
        if self.module.params.get(entity_id):
            setattr(self, entity_id, self.module.params[entity_id])
        else:
            name = self.module.params.get(f"{entity_type}_name")
            url = f"{self.api_host}v1/{entity_type}s"
            response, info = fetch_url(self.module, url=url, method="GET", headers=self._get_headers())
            entity = next((item for item in self._parse_response(response, info) if item[name_key] == name), None)
            if entity:
                setattr(self, entity_id, entity["id"])
            else:
                self.module.fail_json(
                    msg=f"{entity_type.upper()} '{name}' not found in the fetched {entity_type.capitalize()}s"
                )

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
            return json.dumps(self._get_response_json(response_text), ensure_ascii=False)
        return None

    def _get_response_json(self, response_text: str) -> dict:
        response = json.loads(to_text(response_text))
        return response.get("results", response)

    def _handle_failed_response(self, info: dict) -> None:
        """Handle a failed API request by reporting an error"""
        url = info.get("url")
        body = json.loads(info.get("body", "{}"))
        message_error = body.get("message", "")
        self.module.fail_json(msg="Failed to perfom operation", url=url, message_error=message_error)
