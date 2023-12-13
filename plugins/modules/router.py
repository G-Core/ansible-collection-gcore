# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: router
author:
    - GCore (@GCore)
short_description: Manages routers
description:
    - Create/update/delete or attach/detach router

options:
    command:
        description:
            - Operation to perform.
        choices: [create, update, delete, attach, detach]
        required: true
        type: str
    router_id:
        description:
            - The ID of the router you want to get.
            - Required if I(command) one of create, update, delete, attach or detach
        type: str
        required: false
    name:
        description:
            - Router name.
            - Required if I(command) is create create
            - Used if I(command) is update
        type: str
        required: false
    external_gateway_info:
        description:
            - External gateway info.
            - Used if I(command) is create create or update
        type: dict
        required: false
    interfaces:
        description:
            - List of interfaces to attach to router immediately after creation.
            - Used if I(command) is create
        type: list
        elements: dict
        required: false
    routes:
        description:
            - List of custom routes.
            - Used if I(command) is create or update
        type: list
        elements: dict
        required: false
    subnet_id:
        description:
            - Subnet ID.
            - Target IP is identified by it's subnet.
            - Required if I(command) is attach or detach.
        type: str
        required: false

extends_documentation_fragment:
    - gcore.cloud.cloud.documentation
"""

EXAMPLES = """
- name: Create new router
  gcore.cloud.router:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: create
    name: "my-router"
    external_gateway_info: {'enable_snat': True, 'type': 'default'}
    interfaces: [{'subnet_id': "{{ subnet_id }}", 'type': 'subnet'}]
    routes: [{'destination': '10.0.3.0/24', 'nexthop': '10.0.0.13'}]

- name: Update router
  gcore.cloud.router:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: update
    router_id: "{{ router_id }}"
    name: "new-router-name"

- name: Attach router
  gcore.cloud.router:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: attach
    router_id: "{{ router_id }}"
    subnet_id: "{{ subnet_id }}"

- name: Detach router
  gcore.cloud.router:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: detach
    router_id: "{{ router_id }}"
    subnet_id: "{{ subnet_id }}"

- name: Delete router
  gcore.cloud.router:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: delete
    router_id: "{{ router_id }}"
"""

RETURN = """
router:
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
        id:
            description: Router ID
            returned: always
            type: str
            sample: 4d380efe-aecd-4aa1-82a8-573632ed37f9
        name:
            description: Router name
            returned: always
            type: str
            sample: router_1
        status:
            description: Status of the router
            returned: always
            type: str
            sample: ACTIVE
        external_gateway_info:
            description: State of this router's external gateway
            returned: always
            type: dict
            sample: {
                'network_id': '340d7d54-e165-4d83-b99c-103ce0e6efa7',
                'enable_snat': true,
                'external_fixed_ips': [{
                    'ip_address': '10.94.77.162',
                    'subnet_id': 'db5ebada-a86a-4702-8a19-00b23a1acb05'
                }]
            }
        interfaces:
            description: List of router interfaces
            returned: always
            type: list
            elements: dict
            sample: [{'subnet_id': 'd0a6bd13-81b9-415b-8362-b3f711baf6ac', 'type': 'subnet'}]
        routes:
            description: List of custom routes
            returned: always
            type: list
            elements: dict
            sample: [{'destination': '10.0.3.0/24', 'nexthop': '10.0.0.13'}]
        created_at:
            description: Datetime when the router was created
            returned: always
            type: str
            sample: 2023-11-09T10:34:23+0000
        updated_at:
            description: Datetime when the router was last updated
            returned: always
            type: str
            sample: 2023-11-09T10:34:24+0000
        creator_task_id:
            description: Task that created this entity
            returned: always
            type: str
            sample: 4d7bc56d-9b2e-46be-8a6e-e0f8102c5cc5
        task_id:
            description: Active task. If None, action has been performed immediately in the request itself
            returned: present
            type: str
            sample: 907a87b0-7b63-4fd5-beb3-5ab4ba445c93
"""

from traceback import format_exc

from ansible.module_utils.basic import AnsibleModule, to_native
from ansible_collections.gcore.cloud.plugins.module_utils.clients.router import (
    RouterManageAction,
)
from ansible_collections.gcore.cloud.plugins.module_utils.cloud import (
    AnsibleCloudClient,
)


def manage(module: AnsibleModule):
    api = AnsibleCloudClient(module)
    command = module.params.pop("command")
    result = api.routers.execute_command(command=command)
    module.exit_json(**result)


def main():
    module_spec = dict(
        command=dict(
            type="str",
            choices=list(RouterManageAction),
            required=True,
        ),
        router_id=dict(
            type="str",
            required=False,
        ),
        name=dict(
            type="str",
            required=False,
        ),
        external_gateway_info=dict(
            type="dict",
            required=False,
        ),
        interfaces=dict(
            type="list",
            elements="dict",
            required=False,
        ),
        routes=dict(
            type="list",
            elements="dict",
            required=False,
        ),
        subnet_id=dict(
            type="str",
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
