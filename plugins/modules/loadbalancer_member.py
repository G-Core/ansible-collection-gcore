# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: loadbalancer_member
author:
    - GCore (@GCore)
short_description: Manages loadbalancer members.
description:
    - Create, delete loadbalancer members.

options:
    command:
        description:
            - Operation to perform.
        choices: [create, delete]
        required: true
        type: str
    loadbalancer_pool_id:
        description:
            - Loadbalancer pool ID.
            - Required if I(command) is create or delete.
        type: str
        required: false
    loadbalancer_pool_member_id:
        description:
            - Loadbalancer pool ID.
            - Required if I(command) is delete.
        type: str
        required: false
    protocol_port:
        description:
            - Member IP port.
            - Required if I(command) is create.
        type: int
        required: false
    address:
        description:
            - Member IP address.
            - Required if I(command) is create.
        type: str
        required: false
    subnet_id:
        description:
            - Either subnet_id or instance_id should be provided.
            - Required if I(command) is create and I(instance_id) is not passed
        type: str
        required: false
    instance_id:
        description:
            - Either subnet_id or instance_id should be provided.
            - Required if I(command) is create and I(subnet_id) is not passed
        type: str
        required: false
    admin_state_up:
        description:
            - true if enabled
            - Used if I(command) is create
        type: bool
        required: false
    weight:
        description:
            - Member weight.
            - Used if I(command) is create
        type: int
        required: false
    monitor_address:
        description:
            - An alternate IP address used for health monitoring a backend member.
            - Used if I(command) is create
        type: str
        required: false
    monitor_port:
        description:
            - An alternate protocol port used for health monitoring a backend member.
            - Used if I(command) is create
        type: int
        required: false
    id:
        description:
            - Member ID must be provided if an existing member is being updated.
            - Used if I(command) is create
        type: str
        required: false
    operating_status:
        description:
            - Member operating status.
            - Used if I(command) is create
        type: str
        required: false
extends_documentation_fragment:
    - gcore.cloud.cloud.documentation
"""

EXAMPLES = """
- name: Create new pool member
  gcore.cloud.loadbalancer_member:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: create
    loadbalancer_pool_id: "{{ loadbalancer_pool_id }}"
    protocol_port: 80
    address: '192.168.40.33'

- name: Delete pool member
  gcore.cloud.loadbalancer_member:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: delete
    loadbalancer_pool_id: "{{ loadbalancer_pool_id }}"
    loadbalancer_pool_member_id: "{{ loadbalancer_pool_member_id }}"
"""

RETURN = """
loadbalancer_member:
    description:
        - Response depends of I(command).
        - If I(command) is create then response will loadbalancer pool.
        - If I(command) is delete then response will be a dict of resource ID.
    returned: always
    type: complex
    contains:
        id:
            description: Pool ID
            returned: always
            type: str
            sample: 43658ea9-54bd-4807-90b1-925921c9a0d1
        name:
            description: Pool name
            returned: always
            type: str
            sample: lbaas_test_pool
        lb_algorithm:
            description: Load balancer algorithm
            returned: always
            type: str
            sample: ROUND_ROBIN
        protocol:
            description: Protocol
            returned: always
            type: str
            sample: TCP
        loadbalancers:
            description: Load balancers IDs
            returned: always
            type: list
            elements: dict
            sample: [{'id': '79943b39-5e67-47e1-8878-85044b39667a'}]
        listeners:
            description:
                - Listeners IDs
            returned: always
            type: list
            elements: dict
            sample: [{'id': 'c63341da-ea44-4027-bbf6-1f1939c783da'}]
        members:
            description: Number of pools
            returned: always
            type: list
            elements: dict
            sample: [{
                'address': '192.168.13.9',
                'id': '65f4e0eb-7846-490e-b44d-726c8baf3c25',
                'operating_status': 'ONLINE',
                'protocol_port': 80,
                'subnet_id': 'c864873b-8d9b-4d29-8cce-bf0bdfdaa74d',
                'weight': 1
            }]
        healthmonitor:
            description: Health monitor parameters
            returned: always
            type: dict
            sample: {
                'delay': 10,
                'http_method': 'GET',
                'max_retries': 3,
                'max_retries_down': 3,
                'timeout': 5,
                'type': 'HTTP',
                'url_path': '/'
            }
        session_persistence:
            description: Session persistence parameters
            returned: always
            type: dict
            sample: {}
        operating_status:
            description: Pool operating status
            returned: always
            type: str
            sample: ONLINE
        provisioning_status:
            description: Pool lifecycle status
            returned: always
            type: str
            sample: ACTIVE
        creator_task_id:
            description: Active task. If None, action has been performed immediately in the request itself
            returned: if available
            type: str
            sample: d8334c12-2881-4c4a-84ad-1b21fea73ad1
        timeout_client_data:
            description: Frontend client inactivity timeout in milliseconds
            returned: always
            type: int
            sample: 50000
        timeout_member_connect:
            description:
                - Backend member connection timeout in milliseconds.
            returned: always
            type: int
            sample: 5000
        timeout_member_data:
            description: Backend member inactivity timeout in milliseconds
            returned: always
            type: int
            sample: null
"""

from traceback import format_exc

from ansible.module_utils.basic import AnsibleModule, to_native
from ansible_collections.gcore.cloud.plugins.module_utils.clients.loadbalancer_member import (
    LbPoolMemeberManageAction,
)
from ansible_collections.gcore.cloud.plugins.module_utils.cloud import (
    AnsibleCloudClient,
)


def manage(module: AnsibleModule):
    api = AnsibleCloudClient(module)
    command = module.params.pop("command")
    result = api.loadbalancer_members.execute_command(command=command)
    module.exit_json(changed=False, data=result)


def main():
    module_spec = dict(
        command=dict(type="str", choices=list(LbPoolMemeberManageAction), required=True),
        loadbalancer_pool_id=dict(type="str", required=False),
        loadbalancer_pool_member_id=dict(type="str", required=False),
        protocol_port=dict(type="int", required=False),
        address=dict(type="str", required=False),
        subnet_id=dict(type="str", required=False),
        instance_id=dict(type="str", required=False),
        admin_state_up=dict(type="bool", required=False),
        weight=dict(type="int", required=False),
        monitor_address=dict(type="str", required=False),
        monitor_port=dict(type="int", required=False),
        id=dict(type="str", required=False),
        operating_status=dict(type="str", required=False),
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
