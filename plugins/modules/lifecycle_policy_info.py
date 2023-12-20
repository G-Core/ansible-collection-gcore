# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: lifecycle_policy_info
author:
    - GCore (@GCore)
short_description: Gather infos about all GCore lifecycle policies.
description:
    - Gather infos about all GCore lifecycle policies.

options:
    lifecycle_policy_id:
        description:
            - The ID of lifecycle policy you want to get.
            - The module will fail if the provided ID is invalid.
        type: str
        required: false
    need_volumes:
        description:
            - Set it if you want to get volume ids.
        type: bool
        required: false
extends_documentation_fragment:
    - gcore.cloud.cloud.documentation
"""

EXAMPLES = """
- name: Gather gcore lifecycle policies infos
  gcore.cloud.lifecycle_policy_info:
    api_token: "{{ api_token }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"

- name: Gather gcore specific lifecycle policy info
  gcore.cloud.lifecycle_policy_info:
    api_token: "{{ api_token }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    lifecycle_policy_id: "{{ lifecycle_policy_id }}"
"""

RETURN = """
lifecycle_policy_info:
    description:
        - When I(lifecycle_policy_id) is passed, it is a dict of resource.
        - Otherwise it is a list of dictionaries.
    returned: always
    type: complex
    contains:
        project_id:
            description: Project ID
            returned: always
            type: int
            sample: 1
        region_id:
            description: Region ID
            returned: always
            type: int
            sample: 1
        id:
            description: Policy ID
            returned: always
            type: str
            sample: 1
        schedules:
            description: Flavor ID
            returned: always
            type: list
            elements: dict
            sample: [{
                'owner': 'lifecycle_policy',
                'owner_id': 1,
                'id': '1488e2ce-f906-47fb-ba32-c25a3f63df4f',
                'max_quantity': 2,
                'day_of_week': '*',
                'hour': '0, 10, 20',
                'minute': '30',
                'type': 'cron',
                'resource_name_template': 'reserve snap of the volume volume_id',
                'user_id': 12,
                'day': '*',
                'month': '*',
                'timezone': 'Asia/Tashkent',
                'week': '*'
            }]
        name:
            description: Policy name
            returned: always
            type: str
            sample: schedule_1
        action:
            description: Policy action
            returned: always
            type: str
            sample: volume_snapshot
        user_id:
            description: User created the policy.
            returned: always
            type: int
            sample: 11
        status:
            description: Lifecycle policys status
            returned: always
            type: str
            sample: active
        volumes:
            desciption: Data of volumes which should be reserved.
            returned: if available
            type: list
            elements: dict
            sample: [{'id': '3ed9e2ce-f906-47fb-ba32-c25a3f63df4f', 'name': 'test schedule'}]
"""

from traceback import format_exc

from ansible.module_utils.basic import AnsibleModule, to_native
from ansible_collections.gcore.cloud.plugins.module_utils.cloud import (
    AnsibleCloudClient,
)


def manage(module: AnsibleModule):
    api = AnsibleCloudClient(module)
    lifecycle_policy_id = module.params.get("lifecycle_policy_id")
    command = "get_by_id" if lifecycle_policy_id else "get_list"
    result = api.lifecycle_policy.execute_command(command=command)
    module.exit_json(**result)


def main():
    module_spec = dict(
        lifecycle_policy_id=dict(type="str", required=False),
        need_volumes=dict(type="bool", required=False),
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
        supports_check_mode=True
    )
    try:
        manage(module)
    except Exception as exc:
        module.fail_json(msg=to_native(exc), exception=format_exc())


if __name__ == "__main__":
    main()
