# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: loadbalancer_listener_info
author:
    - GCore (@GCore)
short_description: Gather infos about all GCore loadbalancer listeners.
description:
    - Gather infos about all GCore loadbalancer listeners.

options:
    loadbalancer_listener_id:
        description:
            - The ID of loadbalancer listener you want to get.
            - The module will fail if the provided ID is invalid.
        type: str
        required: false
    show_stats:
        description:
            - Show statistics.
        type: bool
        required: false
    loadbalancer_id:
        description:
            - Loadbalancer ID.
        type: str
        required: false
extends_documentation_fragment:
    - gcore.cloud.cloud.documentation
"""

EXAMPLES = """
- name: Gather gcore loadbalancer listener infos
  gcore.cloud.loadbalancer_listener_info:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"

- name: Gather gcore specific loadbalancer listener info
  gcore.cloud.loadbalancer_listener_info:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    loadbalancer_listener_id: "{{ loadbalancer_listener_id }}"

- name: Gather info about all listeners for specif loadbalancer
  gcore.cloud.loadbalancer_listener_info:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    loadbalancer_id: "{{ loadbalancer_id }}"
"""

RETURN = """
loadbalancer_listener_info:
    description:
        - When I(loadbalancer_listener_id) is passed, it is a dict of resource.
        - Otherwise it is a list of dictionaries.
    returned: always
    type: complex
    contains:
        id:
            description: Load balancer listener ID
            returned: always
            type: str
            sample: 43658ea9-54bd-4807-90b1-925921c9a0d1
        name:
            description: Load balancer listener name
            returned: always
            type: str
            sample: lbaas_test_listener
        protocol:
            description: Load balancer protocol
            returned: always
            type: dict
            sample: TCP
        protocol_port:
            description: Protocol port
            returned: always
            type: int
            sample: 80
        insert_headers:
            description:
                - Dictionary of additional header insertion into HTTP headers.
                - Only used with HTTP and TERMINATED_HTTPS protocols.
            returned: always
            type: dict
            sample: {}
        pool_count:
            description: Number of pools
            returned: always
            type: int
            sample: 0
        operating_status:
            description: Listener operating status
            returned: always
            type: str
            sample: ONLINE
        provisioning_status:
            description: Listener lifecycle status
            returned: always
            type: str
            sample: ACTIVE
        creator_task_id:
            description: Task that created this entity
            returned: always
            type: str
            sample: d2d871da-d7ce-4c2b-bedc-5900c37880e6
        task_id:
            description: Active task. If None, action has been performed immediately in the request itself.
            returned: always
            type: str
            sample: c593da0c-1fa4-4882-8d0c-c5179fbcfc71
        stats:
            description: Statistic of the listener. It is available only in get functions by a flag.
            returned: if available
            type: dict
            sample: {
                'active_connections': 0,
                'bytes_in': 34942398609,
                'bytes_out': 304777113641,
                'request_errors': 4,
                'total_connections': 21095970
            }
        secret_id:
            description: ID of the secret where PKCS12 file is stored for TERMINATED_HTTPS load balancer
            returned: always
            type: str
            sample: eddd2336-0e38-4efc-86d7-e8b3801e83e0
        sni_secret_id:
            description:
                - List of secret's ID containing PKCS12 format certificate/key bundles for TERMINATED_HTTPS listeners.
            returned: if available
            type: list
            elements: str
            sample: ['e76a3f17-f5a1-4efa-8917-c6c2e8eb157c']
        allowed_cidrs:
            description: Network CIDRs from which service will be accessible
            returned: always
            type: list
            elements: str
            sample: []
"""

from traceback import format_exc

from ansible.module_utils.basic import AnsibleModule, to_native
from ansible_collections.gcore.cloud.plugins.module_utils.cloud import (
    AnsibleCloudClient,
)


def manage(module: AnsibleModule):
    api = AnsibleCloudClient(module)
    loadbalancer_listener_id = module.params.get("loadbalancer_listener_id")
    command = "get_by_id" if loadbalancer_listener_id else "get_list"
    result = api.loadbalancer_listeners.execute_command(command=command)
    module.exit_json(**result)


def main():
    module_spec = dict(
        loadbalancer_listener_id=dict(type="str", required=False),
        show_stats=dict(type="bool", required=False),
        loadbalancer_id=dict(type="str", required=False),
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
