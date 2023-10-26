from ansible.module_utils.basic import AnsibleModule
from ansible_collections.gcore.cloud.plugins.module_utils.clients.base import (
    BaseResourceClient,
)


class GCoreImageClient(BaseResourceClient):
    ...
