from ansible.module_utils.basic import AnsibleModule, env_fallback
from ansible_collections.gcore.cloud.plugins.module_utils.api import GCoreAPIClient
from ansible_collections.gcore.cloud.plugins.module_utils.clients.image import (
    GCoreImageClient,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.instance import (
    GCoreInstanceClient,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.network import (
    GCoreNetworkClient,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.snapshot import (
    GCoreSnapshotClient,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.volume import (
    GCoreVolumeClient,
)


class AnsibleGCore:
    def __init__(self, module: AnsibleModule) -> None:
        self.module = module
        self.client = GCoreAPIClient(module)

    @property
    def volumes(self) -> GCoreVolumeClient:
        return GCoreVolumeClient(self.module, "v1/volumes/")

    @property
    def images(self) -> GCoreImageClient:
        return GCoreImageClient(self.module, "v1/images/")

    @property
    def instances(self) -> GCoreInstanceClient:
        return GCoreInstanceClient(self.module, "v1/instances/")

    @property
    def networks(self) -> GCoreNetworkClient:
        return GCoreNetworkClient(self.module, "v1/networks/")

    @property
    def snapshots(self) -> GCoreSnapshotClient:
        return GCoreSnapshotClient(self.module, "v1/snapshots/")

    @staticmethod
    def get_api_spec() -> dict:
        return dict(
            api_key=dict(
                type="str",
                fallback=(env_fallback, ["GCORE_API_KEY"]),
                no_log=True,
                required=True,
            ),
            api_host=dict(
                type="str",
                fallback=(env_fallback, ["GCORE_API_HOST"]),
                default="https://api.gcore.com/cloud",
            ),
            api_timeout=dict(
                type="int",
                fallback=(env_fallback, ["GCORE_API_TIMEOUT"]),
                default=30,
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
