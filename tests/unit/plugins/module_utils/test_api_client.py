import unittest

from ansible_collections.community.gcore.plugins.module_utils.api import GCoreAPIClient
from mock import MagicMock


def mock_module(params: dict):
    module = MagicMock()
    module.params = params
    return module


class TestApiClient(unittest.TestCase):
    def setUp(self) -> None:
        self.api_endpoint = "https://api.test.com"
        self.project_id = 100
        self.region_id = 10
        params = {
            "api_token": "test_api_token",
            "api_timeout": 60,
            "project_id": self.project_id,
            "region_id": self.region_id,
            "api_endpoint": self.api_endpoint,
        }
        self.module = mock_module(params)
        self.api_client = GCoreAPIClient(self.module)

    def test_module_params(self):
        self.assertEqual(self.api_client.api_token, "test_api_token")
        self.assertEqual(self.api_client.api_timeout, 60)
        self.assertEqual(self.api_client.project_id, self.project_id)
        self.assertEqual(self.api_client.region_id, self.region_id)
        self.assertEqual(self.api_client.api_endpoint, f"{self.api_endpoint}/")

    def test_build_url(self):
        path = "v1/some/path"
        url = self.api_client._build_url(path)
        self.assertEqual(url, f"{self.api_endpoint}/{path}/{self.project_id}/{self.region_id}")

        # with resource
        resource_id = "fdc2d326-b542-4b73-9257-27222a452307"
        url = self.api_client._build_url(path, resource_id=resource_id)
        self.assertEqual(url, f"{self.api_endpoint}/{path}/{self.project_id}/{self.region_id}/{resource_id}")

        # with query
        query = {"metadata_k": ["key"]}
        url = self.api_client._build_url(path, query=query)
        self.assertEqual(url, f'{self.api_endpoint}/{path}/{self.project_id}/{self.region_id}?metadata_k=["key"]')
