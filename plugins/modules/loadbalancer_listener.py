# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: loadbalancer_listener
author:
    - GCore (@GCore)
short_description: Manages loadbalancer listeners.
description:
    - Create, update or delete loadbalancer listener.

options:
    command:
        description:
            - Operation to perform.
        choices: [create, update, delete]
        required: true
        type: str
    loadbalancer_listener_id:
        description:
            - Loadbalancer Id.
            - Required if I(command) is update or delete
        type: str
        required: false
    name:
        description:
            - Load balancer listener name.
            - Required if I(command) is create.
            - Used if I(command) is update
        type: str
        required: false
    protocol:
        description:
            - Load balancer protocol.
            - Required if I(command) is create.
        type: str
        choices: [
            HTTP,
            HTTPS,
            TCP,
            UDP,
            TERMINATED_HTTPS,
            PROMETHEUS
        ]
        required: false
    protocol_port:
        description:
            - Protocol port.
            - Required if I(command) is create.
        type: int
        required: false
    loadbalancer_id:
        description:
            - Load balancer ID.
            - Required if I(command) is create.
        type: str
        required: false
    insert_x_forwarded:
        description:
            - Add headers X-Forwarded-For, X-Forwarded-Port, X-Forwarded-Proto to requests.
            - Only used with HTTP or TERMINATED_HTTPS protocols.
            - Used if I(command) is create.
        type: bool
        required: false
    secret_id:
        description:
            - ID of the secret where PKCS12 file is stored for TERMINATED_HTTPS load balancer.
            - Used if I(command) is create.
        type: str
        required: false
    sni_secret_id:
        description:
            - List of secret's ID containing PKCS12 format certificate/key bundles for TERMINATED_HTTPS listeners.
            - Used if I(command) is create.
        type: list
        elements: str
        required: false
    allowed_cidrs:
        description:
            - Network CIDRs from which service will be accessible.
            - Used if I(command) is create.
        type: list
        elements: str
        required: false
extends_documentation_fragment:
    - gcore.cloud.cloud.documentation
"""

EXAMPLES = """
- name: Create new listener
  gcore.cloud.loadbalancer_listener:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: create
    name: tcp_test
    protocol: TCP
    protocol_port: 80
    loadbalancer_id: "{{ loadbalancer_id }}"

- name: Update listener
  gcore.cloud.loadbalancer_listener:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: update
    loadbalancer_listener_id: "{{ loadbalancer_listener_id }}"
    name: tcp_listener_2

- name: Delete listener
  gcore.cloud.loadbalancer_listener:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: delete
    loadbalancer_listener_id: "{{ loadbalancer_listener_id }}"
"""

RETURN = """
loadbalancer_listener:
    description:
        - Response depends of I(command).
        - If I(command) is create or update then response will be a dict of resource.
        - If I(command) is delete then response will be a dict of resource ID.
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
            type: str
            sample: TCP
        protocol_port:
            description: Protocol port
            returned: always
            type: int
            sample: 80
        loadbalancer_id:
            description: Load balancer ID
            returned: always
            type: str
            sample: 61d0a6c0-3676-4b5b-9455-03efff0143d3
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
            returned: always
            type: list
            elements: str
            sample: ['e76a3f17-f5a1-4efa-8917-c6c2e8eb157c']
        allowed_cidrs:
            description: Network CIDRs from which service will be accessible
            returned: always
            type: list
            elements: str
            sample: [
                '10.0.0.0/32'
            ]
"""

from traceback import format_exc

from ansible.module_utils.basic import AnsibleModule, to_native
from ansible_collections.gcore.cloud.plugins.module_utils.clients.loadbalancer_listener import (
    LbListenerManageAction,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.loadbalancer_listener import (
    LbListenerProtocol,
)
from ansible_collections.gcore.cloud.plugins.module_utils.cloud import (
    AnsibleCloudClient,
)


def manage(module: AnsibleModule):
    api = AnsibleCloudClient(module)
    command = module.params.pop("command")
    result = api.loadbalancer_listeners.execute_command(command=command)
    module.exit_json(changed=False, data=result)


def main():
    module_spec = dict(
        command=dict(type="str", choices=list(LbListenerManageAction), required=True),
        loadbalancer_listener_id=dict(type="str", required=False),
        name=dict(type="str", required=False),
        protocol=dict(type="str", choices=list(LbListenerProtocol), required=False),
        protocol_port=dict(type="int", required=False),
        loadbalancer_id=dict(type="str", required=False),
        insert_x_forwarded=dict(type="bool", required=False),
        secret_id=dict(type="str", required=False),
        allowed_cidrs=dict(type="list", elements="str", required=False),
        sni_secret_id=dict(type="list", elements="str", required=False),
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
