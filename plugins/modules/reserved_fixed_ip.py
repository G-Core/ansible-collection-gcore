# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: reserved_fixed_ip
author:
    - GCore (@GCore)
short_description: Manages reserved fixed ip
description:
    - Created/update or delete reserved fixed ip

options:
    command:
        description:
            - Operation to perform.
        choices: [create, update, delete]
        required: true
        type: str
    port_id:
        description:
            - Reserved fixed ip ID (port)
            - Required if I(command) is update or delete
        required: false
        type: str
    type:
        description:
            - Type if reserved fixed ip
            - Required if I(command) is created
        choices: [external, subnet, any_subnet, ip_address]
        required: false
        type: str
    is_vip:
        description:
            - Reserved fixed IP is a VIP
            - Used if I(command) is created or update
        required: false
        type: bool
    subnet_id:
        description:
            - Reserved fixed IP will be allocated in this subnet
            - Required if I(command) is created and I(type) is subnet
        required: false
        type: str
    network_id:
        description:
            - Reserved fixed IP will be allocated in a subnet of this network
            - Required if I(command) is created and I(type) is any_subnet or ip_address
        required: false
        type: str
    ip_address:
        description:
            - Reserved fixed IP will be allocated the given IP address
            - Required if I(command) is created and I(type) is ip_address
        required: false
        type: str
extends_documentation_fragment:
    - gcore.cloud.cloud.documentation
"""

EXAMPLES = """
- name: Create new external reserved fixed ip
  gcore.cloud.reserved_fixed_ip:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: create
    type: external

- name: Create new subnet reserved fixed ip
  gcore.cloud.reserved_fixed_ip:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: create
    type: subnet
    subnet_id: "{{ subnet_id }}"

- name: Create new any subnet reserved fixed ip
  gcore.cloud.reserved_fixed_ip:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: create
    type: any_subnet
    network_id: "{{ network_id }}"

- name: Create new ip_address subnet reserved fixed ip
  gcore.cloud.reserved_fixed_ip:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: create
    type: ip_address
    network_id: "{{ network_id }}"
    ip_address: "{{ ip_address }}"

- name: Update reserved fixed ip
  gcore.cloud.reserved_fixed_ip:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: update
    port_id: "{{ port_id }}"
    is_vip: true

- name: Delete reserved fixed ip
  gcore.cloud.reserved_fixed_ip:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: delete
    port_id: "{{ port_id }}"
"""

RETURN = """
reserved_fixed_ip:
    description:
        - Response depends of I(command).
        - If I(command) is one of create or update then response will be resource dictionary.
        - If I(command) is delete then response will be dictionary with resource id.
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
from ansible_collections.gcore.cloud.plugins.module_utils.clients.reserved_fip import (
    ReservedFipManageAction,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.reserved_fip import (
    ReservedFipType,
)
from ansible_collections.gcore.cloud.plugins.module_utils.cloud import (
    AnsibleCloudClient,
)


def manage(module: AnsibleModule):
    api = AnsibleCloudClient(module)
    command = module.params.pop("command")
    result = api.reserved_fips.execute_command(command=command)
    module.exit_json(**result)


def main():
    module_spec = dict(
        command=dict(type="str", choices=list(ReservedFipManageAction), required=True),
        port_id=dict(type="str", required=False),
        type=dict(type="str", choices=list(ReservedFipType), required=False),
        is_vip=dict(type="bool", required=False),
        subnet_id=dict(type="str", required=False),
        network_id=dict(type="str", required=False),
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
