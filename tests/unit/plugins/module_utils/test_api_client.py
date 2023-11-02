import unittest

from ansible_collections.gcore.cloud.plugins.module_utils.api import GCoreAPIClient
from mock import MagicMock


def mock_module(params: dict):
    module = MagicMock()
    module.params = params
    return module


class TestApiClient(unittest.TestCase):
    def setUp(self) -> None:
        self.api_host = "https://api.test.com"
        self.project_id = 100
        self.region_id = 10
        params = {
            "api_key": "test_api_key",
            "api_timeout": 60,
            "project_id": self.project_id,
            "region_id": self.region_id,
            "api_host": self.api_host,
        }
        self.module = mock_module(params)
        self.api_client = GCoreAPIClient(self.module)

    def test_module_params(self):
        self.assertEqual(self.api_client.api_key, "test_api_key")
        self.assertEqual(self.api_client.api_timeout, 60)
        self.assertEqual(self.api_client.project_id, self.project_id)
        self.assertEqual(self.api_client.region_id, self.region_id)
        self.assertEqual(self.api_client.api_host, f"{self.api_host}/")

    def test_build_url(self):
        path = "v1/some/path/"
        url = self.api_client._build_url(path)
        self.assertEqual(url, f"{self.api_host}/{path}{self.project_id}/{self.region_id}")

        # with resource
        resource_id = "fdc2d326-b542-4b73-9257-27222a452307"
        url = self.api_client._build_url(path, path=resource_id)
        self.assertEqual(url, f"{self.api_host}/{path}{self.project_id}/{self.region_id}/{resource_id}")

        # with query
        query = {"metadata_k": ["key"]}
        url = self.api_client._build_url(path, query=query)
        self.assertEqual(url, f"{self.api_host}/{path}{self.project_id}/{self.region_id}?metadata_k=%5B%27key%27%5D")

        # with resource and and some action
        action = "start"
        path = f"{resource_id}/{action}"
        url = self.api_client._build_url(path, path=path)
        self.assertEqual(url, f"{self.api_host}/{path}{self.project_id}/{self.region_id}/{resource_id}/{action}")
