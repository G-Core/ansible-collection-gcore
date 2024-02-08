# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: subnet_info
author:
    - GCore (@GCore)
short_description: Gather infos about all GCore subnets.
description:
    - Gather infos about all GCore subnets.

options:
    subnet_id:
        description:
            - The ID of the subnet you want to get.
            - The module will fail if the provided ID is invalid.
        type: str
        required: false
    network_id:
        description:
            - Only list subnets of this network.
        type: str
        required: false
    metadata_kv:
        description:
            - Filter by metadata key-value pairs.
            - Must be a valid JSON string.
        type: str
        required: false
    metadata_k:
        description:
            - Filter by metadata keys. Must be a valid JSON string
        type: str
        required: false
    limit:
        description:
            - Limit the number of returned items
        type: int
        required: false
    offset:
        description:
            - Offset value is used to exclude the first set of records from the result
        type: int
        required: false
extends_documentation_fragment:
    - gcore.cloud.cloud.documentation
"""

EXAMPLES = """
- name: Gather gcore subnets info
  gcore.cloud.subnet_info:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"

- name: Gather gcore specific subnet info
  gcore.cloud.subnet_info:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    subnet_id: "{{ subnet_id }}"
"""

RETURN = """
subnet_info:
    description:
        - When I(subnet_id) is passed, it is a dict of resource.
        - Otherwise it is a list of dictionaries.
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

from ansible_collections.gcore.cloud.plugins.module_utils.cloud import (
    AnsibleCloudClient,
)


def manage(module: AnsibleModule):
    api = AnsibleCloudClient(module)
    subnet_id = module.params.get("subnet_id")
    command = "get_by_id" if subnet_id else "get_list"
    result = api.subnets.execute_command(command=command)
    module.exit_json(**result)


def main():
    module_spec = dict(
        subnet_id=dict(
            type="str",
            required=False,
        ),
        network_id=dict(
            type="str",
            required=False,
        ),
        metadata_k=dict(
            type="str",
            required=False,
        ),
        metadata_kv=dict(
            type="str",
            required=False,
        ),
        limit=dict(
            type="int",
            required=False,
        ),
        offset=dict(
            type="int",
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
