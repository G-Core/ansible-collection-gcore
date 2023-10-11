from ansible.module_utils.basic import AnsibleModule, env_fallback

from .api import GCoreAPIClient


class AnsibleGCore:
    def __init__(self, module: AnsibleModule, resource: str) -> None:
        self.module = module
        self.resource = resource
        self.client = GCoreAPIClient(module)

    @staticmethod
    def get_api_spec() -> dict:
        return dict(
            api_token=dict(
                type="str",
                fallback=(env_fallback, ["GCORE_API_TOKEN"]),
                no_log=True,
                required=True,
            ),
            api_endpoint=dict(
                type="str",
                fallback=(env_fallback, ["GCORE_API_ENDPOINT"]),
                default="https://api.gcore.com/cloud/",
            ),
            api_timeout=dict(
                type="int",
                fallback=(env_fallback, ["GCORE_API_TIMEOUT"]),
                default=5,
            ),
            project_id=dict(
                type="int",
                required=True,
                fallback=(env_fallback, ["GCORE_PROJECT_ID"]),
            ),
            region_id=dict(
                type="int",
                required=True,
                fallback=(env_fallback, ["GCORE_REGION_ID"]),
            ),
        )
