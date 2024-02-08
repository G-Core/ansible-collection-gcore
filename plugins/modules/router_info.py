# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: router_info
author:
    - GCore (@GCore)
short_description: Gather infos about all GCore routers.
description:
    - Gather infos about all GCore routers.

options:
    router_id:
        description:
            - The ID of the router you want to get.
            - The module will fail if the provided ID is invalid.
        type: str
        required: false
    limit:
        description:
            - Limit the number of returned limit request entities.
        type: int
        required: false
    offset:
        description:
            - Offset value is used to exclude the first set of records from the result.
        type: int
        required: false
extends_documentation_fragment:
    - gcore.cloud.cloud.documentation
"""

EXAMPLES = """
- name: Gather gcore routers info
  gcore.cloud.router_info:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"

- name: Gather gcore specific router info
  gcore.cloud.router_info:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    router_id: "{{ router_id }}"
"""

RETURN = """
router_info:
    description:
        - When I(router_id) is passed, it is a dict of resource.
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

from ansible_collections.gcore.cloud.plugins.module_utils.cloud import (
    AnsibleCloudClient,
)


def manage(module: AnsibleModule):
    api = AnsibleCloudClient(module)
    router_id = module.params.get("router_id")
    command = "get_by_id" if router_id else "get_list"
    result = api.routers.execute_command(command=command)
    module.exit_json(**result)


def main():
    module_spec = dict(
        router_id=dict(
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
