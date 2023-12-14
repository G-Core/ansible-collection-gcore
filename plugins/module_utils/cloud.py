from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible_collections.gcore.cloud.plugins.module_utils.api import CloudAPIClient
from ansible_collections.gcore.cloud.plugins.module_utils.clients.image import (
    CloudImageClient,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.instance import (
    CloudInstanceClient,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.network import (
    CloudNetworkClient,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.router import (
    CloudRouterClient,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.snapshot import (
    CloudSnapshotClient,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.subnet import (
    CloudSubnetClient,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.volume import (
    CloudVolumeClient,
)


class AnsibleCloudClient:
    def __init__(self, module: AnsibleModule) -> None:
        self.module = module
        self.client = CloudAPIClient(module)

    @property
    def volumes(self) -> CloudVolumeClient:
        return CloudVolumeClient(self.module, "v1/volumes/")

    @property
    def images(self) -> CloudImageClient:
        return CloudImageClient(self.module, "v1/images/")

    @property
    def instances(self) -> CloudInstanceClient:
        return CloudInstanceClient(self.module, "v1/instances/")

    @property
    def networks(self) -> CloudNetworkClient:
        return CloudNetworkClient(self.module, "v1/networks/")

    @property
    def snapshots(self) -> CloudSnapshotClient:
        return CloudSnapshotClient(self.module, "v1/snapshots/")

    @property
    def routers(self) -> CloudRouterClient:
        return CloudRouterClient(self.module, "v1/routers/")

    @property
    def subnets(self) -> CloudSubnetClient:
        return CloudSubnetClient(self.module, "v1/subnets/")

    @staticmethod
    def get_api_spec() -> dict:
        return dict(
            api_key=dict(
                type="str",
                fallback=(env_fallback, ["CLOUD_API_KEY"]),
                no_log=True,
            ),
            api_host=dict(
                type="str",
                fallback=(env_fallback, ["CLOUD_API_HOST"]),
                default="https://api.gcore.com/cloud",
            ),
            api_timeout=dict(
                type="int",
                fallback=(env_fallback, ["API_TIMEOUT"]),
                default=30,
            ),
            project_id=dict(
                type="int",
                fallback=(env_fallback, ["CLOUD_PROJECT_ID"]),
            ),
            project_name=dict(
                type="str",
                fallback=(env_fallback, ["CLOUD_PROJECT_NAME"]),
            ),
            region_id=dict(
                type="int",
                fallback=(env_fallback, ["CLOUD_REGION_ID"]),
            ),
            region_name=dict(
                type="str",
                fallback=(env_fallback, ["CLOUD_REGION_NAME"]),
            ),
        )
