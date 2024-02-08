# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: loadbalancer_pool
author:
    - GCore (@GCore)
short_description: Manages loadbalancer pools.
description:
    - Create, update, delete loadbalancer pools.

options:
    command:
        description:
            - Operation to perform.
        choices: [create, update, delete]
        required: true
        type: str
    loadbalancer_pool_id:
        description:
            - Loadbalancer pool ID.
            - Required if I(command) is update or delete.
        type: str
        required: false
    name:
        description:
            - Load balancer pool name.
            - Required if I(command) is create.
            - Used if I(command) is update.
        type: str
        required: false
    lb_algorithm:
        description:
            - Load balancer algorithm.
            - Required if I(command) is create.
            - Used if I(command) is update.
        type: str
        choices: [
            ROUND_ROBIN,
            LEAST_CONNECTIONS,
            SOURCE_IP,
            SOURCE_IP_PORT
        ]
        required: false
    protocol:
        description:
            - Protocol.
            - Used if I(command) is create or update
        type: str
        choices: [
            HTTP,
            HTTPS,
            PROXY,
            TCP,
            UDP
        ]
        required: false
    loadbalancer_id:
        description:
            - Loadbalancer ID.
            - Required if I(command) is create and I(listener_id) is not passed
            - Used if I(command) is update
        type: str
        required: false
    listener_id:
        description:
            - Listener ID.
            - Required if I(command) is create and I(loadbalancer_id) is not passed
            - Used if I(command) is update
        type: str
        required: false
    members:
        description:
            - Pool members.
            - Used if I(command) is create or update
        type: list
        elements: dict
        required: false
    healthmonitor:
        description:
            - Health monitor details.
            - Used if I(command) is create or update
        type: dict
        required: false
    session_persistence:
        description:
            - Session persistence details.
            - Used if I(command) is create or update
        type: dict
        required: false
    timeout_client_data:
        description:
            - Frontend client inactivity timeout in milliseconds.
            - Used if I(command) is create or update
        type: int
        required: false
    timeout_member_connect:
        description:
            - Backend member connection timeout in milliseconds.
            - Used if I(command) is create or update
        type: int
        required: false
    timeout_member_data:
        description:
            - Backend member inactivity timeout in milliseconds.
            - Used if I(command) is create or update
        type: int
        required: false
extends_documentation_fragment:
    - gcore.cloud.cloud.documentation
"""

EXAMPLES = """
- name: Create new pool for specific loadbalancer
  gcore.cloud.loadbalancer_pool:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: create
    name: "test_lb_pool"
    lb_algorithm: "{{ lb_algorithm }}"
    protocol: "{{ protocol }}"
    loadbalancer_id: "{{ loadbalancer_id }}"

- name: Create new pool for specific loadbalancer listener
  gcore.cloud.loadbalancer_pool:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: create
    name: "test_lb_pool"
    lb_algorithm: "{{ lb_algorithm }}"
    protocol: "{{ protocol }}"
    loadbalancer_id: "{{ loadbalancer_id }}"
    listener_id: "{{ listener_id }}"

- name: Update pool
  gcore.cloud.loadbalancer_pool:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: update
    loadbalancer_pool_id: "{{ loadbalancer_pool_id }}"
    name: "test_lb_pool_2"
    timeout_client_data: "{{ timeout_client_data }}"
    lb_algorithm: "{{ lb_algorithm }}"

- name: Delete pool
  gcore.cloud.loadbalancer_pool:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: delete
    loadbalancer_pool_id: "{{ loadbalancer_pool_id }}"
"""

RETURN = """
loadbalancer_pool:
    description:
        - Response depends of I(command).
        - If I(command) is create or update then response will be a dict of resource.
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
            sample: {
                'cookie_name': 'test',
                'persistence_granularity': null,
                'persistence_timeout': null,
                'type': 'APP_COOKIE'
            }
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

from ansible_collections.gcore.cloud.plugins.module_utils.clients.loadbalancer_pool import (
    LbPoolManageAction,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.loadbalancer_pool import (
    LbPoolAlgorithm,
    LbPoolProtocol,
)
from ansible_collections.gcore.cloud.plugins.module_utils.cloud import (
    AnsibleCloudClient,
)


def manage(module: AnsibleModule):
    api = AnsibleCloudClient(module)
    command = module.params.pop("command")
    result = api.loadbalancer_pools.execute_command(command=command)
    module.exit_json(**result)


def main():
    module_spec = dict(
        command=dict(type="str", choices=list(LbPoolManageAction), required=True),
        loadbalancer_pool_id=dict(type="str", required=False),
        name=dict(type="str", required=False),
        lb_algorithm=dict(type="str", choices=list(LbPoolAlgorithm), required=False),
        protocol=dict(type="str", choices=list(LbPoolProtocol), required=False),
        loadbalancer_id=dict(type="str", required=False),
        listener_id=dict(type="str", required=False),
        members=dict(type="list", elements="dict", required=False),
        healthmonitor=dict(type="dict", required=False),
        session_persistence=dict(type="dict", required=False),
        timeout_client_data=dict(type="int", required=False),
        timeout_member_connect=dict(type="int", required=False),
        timeout_member_data=dict(type="int", required=False),
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
