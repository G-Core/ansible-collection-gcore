# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: loadbalancer_pool_info
author:
    - GCore (@GCore)
short_description: Gather infos about all GCore loadbalancer pools.
description:
    - Gather infos about all GCore loadbalancer pools.

options:
    loadbalancer_pool_id:
        description:
            - The ID of loadbalancer pool you want to get.
            - The module will fail if the provided ID is invalid.
        type: str
        required: false
    loadbalancer_id:
        description:
            - Load balancer ID.
        type: str
        required: false
    listener_id:
        description:
            - Load balancer listener ID.
        type: str
        required: false
    details:
        description:
            - If true, show member and healthmonitor details of each pool.
        type: bool
        required: false
extends_documentation_fragment:
    - gcore.cloud.cloud.documentation
"""

EXAMPLES = """
- name: Gather gcore loadbalancer pool infos
  gcore.cloud.loadbalancer_pool_info:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"

- name: Gather gcore specific loadbalancer pool info
  gcore.cloud.loadbalancer_pool_info:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    loadbalancer_pool_id: "{{ loadbalancer_pool_id }}"

- name: Gather info about all pools for specific loadbalancer
  gcore.cloud.loadbalancer_pool_info:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    loadbalancer_id: "{{ loadbalancer_id }}"

- name: Gather info about all pools for specific loadbalancer listener
  gcore.cloud.loadbalancer_pool_info:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    listener_id: "{{ listener_id }}"
"""

RETURN = """
loadbalancer_pool_info:
    description:
        - When I(loadbalancer_pool_id) is passed, it is a dict of resource.
        - Otherwise it is a list of dictionaries.
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
            returned: if available
            type: dict
            sample: {
                'id': '5df62f3a-45b0-42e2-b136-86e1ffc1a53e',
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

from ansible_collections.gcore.cloud.plugins.module_utils.cloud import (
    AnsibleCloudClient,
)


def manage(module: AnsibleModule):
    api = AnsibleCloudClient(module)
    loadbalancer_pool_id = module.params.get("loadbalancer_pool_id")
    command = "get_by_id" if loadbalancer_pool_id else "get_list"
    result = api.loadbalancer_pools.execute_command(command=command)
    module.exit_json(**result)


def main():
    module_spec = dict(
        loadbalancer_pool_id=dict(type="str", required=False),
        loadbalancer_id=dict(type="str", required=False),
        listener_id=dict(type="str", required=False),
        details=dict(type="bool", required=False),
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
