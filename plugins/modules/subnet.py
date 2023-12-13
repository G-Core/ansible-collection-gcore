# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: subnet
author:
    - GCore (@GCore)
short_description: Manages subnets
description:
    - Create/update or delete subnet

options:
    command:
        description:
            - Operation to perform.
        choices: [create, update, delete]
        required: true
        type: str
    subnet_id:
        description:
            - Subnet ID
            - Required if I(command) is update or delete
        type: str
        required: false
    name:
        description:
            - Subnet name.
            - Required if I(command) is create
            - Used if I(command) is update
        type: str
        required: false
    network_id:
        description:
            - Network ID.
            - Required if I(command) is create.
        type: str
        required: false
    enable_dhcp:
        description:
            - True if DHCP should be enabled.
            - Used if I(command) is create or update
        type: bool
        required: false
    cidr:
        description:
            - CIDR.
            - Required if I(command) is create
        type: str
        required: false
    connect_to_network_router:
        description:
            - True if the network's router should get a gateway in this subnet.
            - Must be explicitly false when gateway_ip is null.
            - Used if I(command) is create
        type: bool
        required: false
    dns_nameservers:
        description:
            - List IP addresses of DNS servers to advertise via DHCP.
            - Used if I(command) is create or update
        type: list
        elements: str
        required: false
    gateway_ip:
        description:
            - Default GW IPv4 address to advertise in DHCP routes in this subnet.
            - Omit this field to let the cloud backend allocate it automatically.
            - I(connect_to_network_router) must be false when gateway_ip is null.
            - Used if I(command) is create or update
        type: str
        required: false
    host_routes:
        description:
            - List of custom static routes to advertise via DHCP.
            - Used if I(command) is or update
        type: list
        elements: dict
        required: false
    metadata:
        description:
            - Create one or more metadata items for a subnet
            - Used if I(command) is create
        type: dict
        required: false
extends_documentation_fragment:
    - gcore.cloud.cloud.documentation
"""

EXAMPLES = """
- name: Create new subnet
  gcore.cloud.subnet:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: create
    name: "{{ subnet_name }}"
    network_id: "{{ network_id }}"
    cidr: "{{ cidr }}"

- name: Update subnet
  gcore.cloud.subnet:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: update
    subnet_id: "{{ subnet_id }}"
    name: "{{ new_subnet_name }}"
    dns_nameservers: "{{ dns_nameservers }}"
    enable_dhcp: true

- name: Update routes for subnet
  gcore.cloud.subnet:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: update
    subnet_id: "{{ subnet_id }}"
    host_routes: "{{ host_routes }}"

- name: Delete subnet
  gcore.cloud.subnet:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: delete
    subnet_id: "{{ subnet_id }}"
"""

RETURN = """
subnet:
    description:
        - Response depends of I(command).
        - Resource dictionary.
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
        name:
            description: Subnet name
            returned: always
            type: str
            sample: subnet_1
        id:
            description: Subnet ID
            returned: always
            type: str
            sample: b39792c3-3160-4356-912e-ba396c95cdcf
        network_id:
            description: Network ID
            returned: always
            type: str
            sample: b30d0de7-bca2-4c83-9c57-9e645bd2cc92
        ip_version:
            description: IP version
            returned: always
            type: int
            sample: 4
        enable_dhcp:
            description: True if DHCP should be enabled
            returned: always
            type: bool
            sample: true
        cidr:
            description: CIDR
            returned: always
            type: str
            sample: 192.168.13.0/24
        connect_to_network_router:
            description: Connecto to router
            returned: if available
            type: bool
            sample: true
        created_at:
            description: Datetime when the subnet was created
            returned: always
            type: str
            sample: 2020-08-17T12:39:02+0000
        updated_at:
            description: Datetime when the subnet was updated
            returned: always
            type: str
            sample: 2020-08-17T12:39:02+0000
        creator_task_id:
            description: Task that created this entity
            returned: if available
            type: str
            sample: 5cc890da-d031-4a23-ac31-625edfa22812
        task_id:
            description: Active task. If None, action has been performed immediately in the request itself
            returned: always
            type: str
            sample: 907a87b0-7b63-4fd5-beb3-5ab4ba445c93
        available_ips:
            description: Number of available ips in subnet
            returned: always
            type: int
            sample: 250
        total_ips:
            description: Total number of ips in subnet
            returned: always
            type: int
            sample: 253
        has_router:
            description: Subnet has router attached to it
            returned: if available
            type: bool
            sample: false
        dns_nameservers:
            description: List IP addresses of a DNS resolver reachable from the network
            returned: always
            type: list
            elements: str
            sample: ['8.8.8.8', '8.8.4.4']
        host_routes:
            description: List of custom static routes to advertise via DHCP
            returned: always
            type: list
            elements: dict
            sample: []
        gateway_ip:
            description:
                - Default GW IPv4 address, advertised in DHCP routes of this subnet.
                - If null, no gateway is advertised by this subnet
            returned: always
            type: str
            sample: 192.168.13.1
        metadata:
            description: Metadata
            returned: always
            type: list
            elements: dict
            sample: [{'key': 'key1', 'value': 'value1', 'read_only': False}]
"""

from traceback import format_exc

from ansible.module_utils.basic import AnsibleModule, to_native
from ansible_collections.gcore.cloud.plugins.module_utils.clients.subnet import (
    SubnetManageAction,
)
from ansible_collections.gcore.cloud.plugins.module_utils.cloud import (
    AnsibleCloudClient,
)


def manage(module: AnsibleModule):
    api = AnsibleCloudClient(module)
    command = module.params.pop("command")
    result = api.subnets.execute_command(command=command)
    module.exit_json(**result)


def main():
    module_spec = dict(
        command=dict(
            type="str",
            choices=list(SubnetManageAction),
            required=True,
        ),
        subnet_id=dict(
            type="str",
            required=False,
        ),
        name=dict(
            type="str",
            required=False,
        ),
        network_id=dict(
            type="str",
            required=False,
        ),
        enable_dhcp=dict(
            type="bool",
            required=False,
        ),
        cidr=dict(
            type="str",
            required=False,
        ),
        connect_to_network_router=dict(
            type="bool",
            required=False,
        ),
        dns_nameservers=dict(
            type="list",
            elements="str",
            required=False,
        ),
        gateway_ip=dict(
            type="str",
            required=False,
        ),
        host_routes=dict(
            type="list",
            elements="dict",
            required=False,
        ),
        metadata=dict(
            type="dict",
            required=False,
        ),
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
