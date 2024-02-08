# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: network
author:
    - GCore (@GCore)
short_description: Manages networks
description:
    - Create/update or delete network

options:
    command:
        description:
            - Operation to perform.
        choices: [create, update, delete]
        required: true
        type: str
    network_id:
        description:
            - The ID of network
            - Required if I(command) is update or delete
        type: str
        required: false
    name:
        description:
            - Network name.
            - Required if I(command) is create or update
        type: str
        required: false
    create_router:
        description:
            - Defaults to True.
            - Used if I(command) is create.
        type: bool
        required: false
    type:
        description:
            - vlan or vxlan network type is allowed. Default value is vxlan.
            - Used if I(command) is create.
        type: str
        choices: [vlan, vxlan]
        required: false
    metadata:
        description:
            - Network metadata
            - Used if I(command) is create.
        type: dict
        required: false
extends_documentation_fragment:
    - gcore.cloud.cloud.documentation
"""

EXAMPLES = """
- name: Create new network
  gcore.cloud.network:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: create
    name: "test-network"

- name: Rename network
  gcore.cloud.network:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: update
    network_id: "{{ network_id }}"
    name: "new-name"

- name: Delete network
  gcore.cloud.network:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: delete
    network_id: "{{ network_id }}"
"""

RETURN = """
network:
    description:
        - Response depends of I(command).
        - If I(command) is create or update then response will be a dict of resource.
        - If I(command) is delete then response will be a dict of resource ID.
    returned: always
    type: complex
    contains:
        project_id:
            description: Project ID
            returned: always
            type: int
            sample: 1
        region:
            description: Region name
            returned: always
            type: str
            sample: Luxembourg 1
        region_id:
            description: Region ID
            returned: always
            type: int
            sample: 1
        id:
            description: Network ID
            returned: always
            type: str
            sample: 726ecfcc-7fd0-4e30-a86e-7892524aa483
        name:
            description: Network name
            returned: always
            type: str
            sample: 123
        mtu:
            description: Maximum transmission unit
            returned: always
            type: int
            sample: 1450
        created_at:
            description: Datetime when the network was created
            returned: always
            type: str
            sample: 2019-06-18T11:56:16+0000
        updated_at:
            description: Datetime when the network was last updated
            returned: if available
            type: str
            sample: 2019-06-19T11:56:16+0000
        type:
            description: Network type (vlan, vxlan)
            returned: always
            type: str
            sample: vlan
        segmentation_id:
            description: Id of network segment
            returned: if available
            type: int
            sample: 9
        external:
            description: True if the network has router:external attribute
            returned: always
            type: bool
            sample: true
        default:
            description: True if the network has is_default attribute
            returned: if available
            type: bool
            sample: true
        shared:
            description: True when the network is shared with your project by external owner
            returned: always
            type: bool
            sample: false
        subnets:
            description: List of subnetworks
            returned: always
            type: list
            elements: str
            sample: ['f00624ab-41bc-4d54-a723-1673ce32d997', '41e0f698-4d39-483b-b77a-18eb070e4c09']
        creator_task_id:
            description: Task that created this entity
            returned: always
            type: str
            sample: fd50fdd1-0482-4c9b-b847-fc9924665af6
        task_id:
            description: Active task. If None, action has been performed immediately in the request itself
            returned: if available
            type: str
            sample: f00624ab-41bc-4d54-a723-1673ce32d997
        metadata:
            description: Network metadata
            returned: if available
            type: list
            sample: [{'key': 'key1', 'value': 'value1', 'read_only': False}]
"""

from traceback import format_exc

from ansible.module_utils.basic import AnsibleModule, to_native

from ansible_collections.gcore.cloud.plugins.module_utils.clients.network import (
    NetworkManageAction,
)
from ansible_collections.gcore.cloud.plugins.module_utils.cloud import (
    AnsibleCloudClient,
)


def manage(module: AnsibleModule):
    api = AnsibleCloudClient(module)
    command = module.params.pop("command")
    result = api.networks.execute_command(command=command)
    module.exit_json(**result)


def main():
    module_spec = dict(
        command=dict(type="str", choices=list(NetworkManageAction), required=True),
        network_id=dict(type="str", required=False),
        name=dict(type="str", required=False),
        create_router=dict(type="bool", required=False),
        type=dict(type="str", choices=["vlan", "vxlan"], required=False),
        metadata=dict(type="dict", required=False),
    )
    spec = AnsibleCloudClient.get_api_spec()
    spec.update(module_spec)
    module = AnsibleModule(
        argument_spec=spec,
        mutually_exclusive=[
            ("project_id", "project_name"),
            ("region_id", "region_name"),
        ],
        required_one_of=[
            ("project_id", "project_name"),
            ("region_id", "region_name"),
        ],
        supports_check_mode=True,
    )
    try:
        manage(module)
    except Exception as exc:
        module.fail_json(msg=to_native(exc), exception=format_exc())


if __name__ == "__main__":
    main()
