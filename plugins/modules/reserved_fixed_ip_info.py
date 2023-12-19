# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: reserved_fixed_ip_info
author:
    - GCore (@GCore)
short_description: Gather infos about all GCore reserved fixed ips.
description:
    - Gather infos about all GCore reserved fixed ips.

options:
    port_id:
        description:
            - The ID of reserved fixed IP (port) you want to get.
            - The module will fail if the provided ID is invalid.
        type: str
        required: false
    external_only:
        description:
            - Set to true if the response should only list public IP addresses
        type: bool
        required: false
    internal_only:
        description:
            - Set to true if the response should only list private IP addresses
        type: bool
        required: false
    available_only:
        description:
            - Set to true if the response should only list IP addresses
        type: bool
        required: false
    vip_only:
        description:
            - Set to true if the response should only list VIPs
        type: bool
        required: false
    device_id:
        description:
            - Filter IPs by device ID it is attached to
        type: str
        required: false
    limit:
        description:
            - Limit the number of returned IPs
        type: int
        required: false
    offset:
        description:
            - Offset value is used to exclude the first set of records from the result
        type: int
        required: false
    order_by:
        description:
            - Ordering reserved fixed IP list result 
        type: str
        required: false
    ip_address:
        description:
            - An IPv4 address to filter results by. Regular expression allowed
        type: str
        required: false
extends_documentation_fragment:
    - gcore.cloud.gcore.documentation
"""

EXAMPLES = """
- name: Gather gcore reserved fixed ip infos
  gcore.cloud.reserved_fixed_ip_info:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"

- name: Gather gcore specific reserved fixed ip info
  gcore.cloud.reserved_fixed_ip_info:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    port_id: "{{ port_id }}"
"""

RETURN = """
reserved_fixed_ip_info:
    description:
        - When I(reserved_fixed_ip) is passed, it is a dict of resource.
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
        port_id:
            description: ID of the port_id underlying the reserved fixed IP
            returned: always
            type: str
            sample: 817c8a3d-bb67-4b88-a0d1-aec980318ff1
        name:
            description: Reserved fixed IP name
            returned: always
            type: str
            sample: 'Reserved fixed ip 10.100.179.44'
        created_at:
            description: Datetime when the reserved fixed ip was created
            returned: always
            type: str
            sample: 2020-09-14T14:45:30+0000
        updated_at:
            description: Datetime when the reserved fixed ip was last updated
            returned: always
            type: str
            sample: 2020-09-14T14:45:30+0000
        status:
            description: Underlying port status
            returned: always
            type: str
            sample: DOWN
        fixed_ip_address:
            description: IP address of the reserved fixed IP
            returned: always
            type: str
            sample: 10.100.179.44
        subnet_id:
            description: ID of the subnet that owns the IP address
            returned: always
            type: str
            sample: 747db04a-2aac-4fda-9492-d9b85a798c09
        network_id:
            description: ID of the network the port is attached to
            returned: always
            type: str
            sample: eed97610-708d-43a5-a9a5-caebd2b7b4ee
        network:
            description: Network details
            returned: always
            type: dict
            sample: {
                'created_at': '2019-06-18T11:56:16+0000',
                'default': True,
                'external': True,
                'id': 'eed97610-708d-43a5-a9a5-caebd2b7b4ee',
                'mtu': 1500,
                'name': 'public',
                'project_id': 1,
                'region_id': 3,
                'subnets': ['747db04a-2aac-4fda-9492-d9b85a798c09'],
                'task_id': 'd1e1500b-e2be-40aa-9a4b-cc493fa1af30',
                'updated_at': '2019-06-18T11:57:00+0000',
            }
        creator_task_id:
            description: Task that created this entity
            returned: always
            type: str
            sample: f00624ab-41bc-4d54-a723-1673ce32d997
        task_id:
            description: Active task. If None, action has been performed immediately in the request itself
            returned: always
            type: str
            sample: fd50fdd1-0482-4c9b-b847-fc9924665af6
        is_external:
            description: Reserved fixed IP belongs to a public network
            returned: always
            type: bool
            sample: false
        is_vip:
            description: Reserved fixed IP is a VIP
            returned: always
            type: bool
            sample: false
        reservation:
            description: Reserved fixed IP status with resource type and ID it is attached to
            returned: always
            type: dict
            sample: {'resource_id': None, 'resource_type': None, 'status': 'available'}
        allowed_address_pairs:
            description: Group of subnet masks and/or IP addresses that share the current IP as VIP
            returned: always
            type: list
            elements: dict
            sample: [{"ip_address": "192.168.123.20", "mac_address": "00:16:3e:f2:87:16"}]
"""

from traceback import format_exc

from ansible.module_utils.basic import AnsibleModule, to_native
from ansible_collections.gcore.cloud.plugins.module_utils.cloud import (
    AnsibleCloudClient,
)


def manage(module: AnsibleModule):
    api = AnsibleCloudClient(module)
    port_id = module.params.get("port_id")
    command = "get_by_id" if port_id else "get_list"
    result = api.reserved_fips.execute_command(command=command)
    module.exit_json(changed=False, data=result)


def main():
    module_spec = dict(
        port_id=dict(type="str", required=False),
        external_only=dict(type="bool", required=False),
        internal_only=dict(type="bool", required=False),
        available_only=dict(type="bool", required=False),
        vip_only=dict(type="bool", required=False),
        device_id=dict(type="str", required=False),
        limit=dict(type="int", required=False),
        offset=dict(type="int", required=False),
        order_by=dict(type="str", required=False),
        ip_address=dict(type="str", required=False),
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
