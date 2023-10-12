from typing import Any, Optional
from urllib.parse import urlencode, urljoin

from ansible.module_utils.basic import AnsibleModule, json
from ansible.module_utils.urls import fetch_url, to_text


class GCoreAPIClient:
    def __init__(self, module: AnsibleModule) -> None:
        self.module = module
        self.api_token = module.params["api_token"]
        self.api_timeout = module.params["api_timeout"]
        self.project_id = module.params["project_id"]
        self.region_id = module.params["region_id"]
        self.api_endpoint = self._set_api_endpoint()

    def get(self, url: str, **kwargs) -> Optional[str]:
        return self._request(method="GET", url=url, data=None, **kwargs)

    def post(self, url: str, data: Any, **kwargs) -> Optional[str]:
        return self._request(method="POST", url=url, data=data, **kwargs)

    def patch(self, url: str, data: Any, **kwargs) -> Optional[str]:
        return self._request(method="PATCH", url=url, data=data, **kwargs)

    def delete(self, url: str, **kwargs) -> Optional[str]:
        return self._request(method="DELETE", url=url, data=None, **kwargs)

    def _set_api_endpoint(self) -> str:
        api_endpoint = self.module.params["api_endpoint"]
        return api_endpoint + "/" if not api_endpoint.endswith("/") else api_endpoint

    def _get_headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_token}",
        }

    def _build_url(self, url: str, **kwargs) -> str:
        handler = f"{self.api_endpoint}{url}{self.project_id}/{self.region_id}"
        path = kwargs.get("path")
        query = kwargs.get("query")
        if path:
            handler = urljoin(handler + "/", path)
        if query:
            query_str = urlencode(query)
            handler = f"{handler}?{query_str}"
        return handler

    def _parse_response(self, response: Any, info: dict) -> Optional[str]:
        """Parse the API response based on the HTTP status code"""
        status_code = info["status"]
        if status_code == 200:
            response = self._parse_successful_response(response)
        elif status_code == 204:
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
        self.module.fail_json(msg=error_message, request_info=info)

    def _request(self, method: str, url: str, data: Optional[Any] = None, **kwargs) -> Optional[str]:
        if data:
            data = self.module.jsonify(data)
        response, info = fetch_url(
            module=self.module,
            url=self._build_url(url, **kwargs),
            method=method,
            headers=self._get_headers(),
            data=data,
            timeout=self.api_timeout,
        )
        return self._parse_response(response, info)
