# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: servergroup_info
author:
    - GCore (@GCore)
short_description: Gather infos about all GCore servergroups.
description:
    - Gather infos about all GCore servergroups.

options:
    servergroup_id:
        description:
            - The ID of the servergroup you want to get.
            - The module will fail if the provided ID is invalid.
        type: str
        required: false
extends_documentation_fragment:
    - gcore.cloud.cloud.documentation
"""

EXAMPLES = """
- name: Gather gcore servergroups infos
  gcore.cloud.servergroup_info:
    api_key: "{{ api_key }}"

- name: Gather gcore specific servergroup info
  gcore.cloud.servergroup_info:
    servergroup_id: "{{ servergroup_id }}"
    api_key: "{{ api_key }}"
"""

RETURN = """
servergroup_info:
    description:
        - When I(servergroup_id) is passed, it is a dict of resource.
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
        servergroup_id:
            description: Server group ID
            returned: always
            type: str
            sample: 47003067-550a-6f17-93b6-81ee16ba061e
        policy:
            description: anti-affinity or affinity or soft-anti-affinity
            returned: if available
            type: str
            sample: anti-affinity
        name:
            description: Server group name
            returned: always
            type: str
            sample: example_server_group
        instances:
            description: Instances in this server group
            returned: if available
            type: list
            elements: dict
            sample: [{'instance_id': '6d14f194-6c1e-49b3-9fc7-50dc8401eb74', 'instance_name': 'test_ruslan_aa2'}]
"""

from traceback import format_exc

from ansible.module_utils.basic import AnsibleModule, to_native
from ansible_collections.gcore.cloud.plugins.module_utils.cloud import (
    AnsibleCloudClient,
)


def manage(module: AnsibleModule):
    api = AnsibleCloudClient(module)
    servergroup_id = module.params.get("servergroup_id")
    command = "get_by_id" if servergroup_id else "get_list"
    result = api.servergroups.execute_command(command=command)
    module.exit_json(changed=False, data=result)


def main():
    module_spec = dict(
        servergroup_id=dict(
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
