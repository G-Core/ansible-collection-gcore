import unittest

from ansible_collections.gcore.cloud.plugins.module_utils.api import CloudAPIClient
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
        self.api_client = CloudAPIClient(self.module)

    def test_module_params(self):
        self.assertEqual(self.api_client.api_key, "test_api_key")
        self.assertEqual(self.api_client.api_timeout, 60)
        self.assertEqual(self.api_client.project_id, self.project_id)
        self.assertEqual(self.api_client.region_id, self.region_id)
        self.assertEqual(self.api_client.api_host, f"{self.api_host}/")
