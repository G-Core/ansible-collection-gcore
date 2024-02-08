# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: lifecycle_policy
author:
    - GCore (@GCore)
short_description: Manages lifecycle policies.
description:
    - Create, update or delete lifecycle policy.
    - Add or remove schedules to the policy.
    - Add or remove volumes to the policy.

options:
    command:
        description:
            - Operation to perform.
        choices: [create, update, delete, add_schedules, remove_schedules, add_volumes, remove_volumes]
        required: true
        type: str
    lifecycle_policy_id:
        description:
            - Lifecycle policy ID.
            - Required for some operations.
        type: str
        required: false
    name:
        description:
            - Policy name.
            - Required if I(command) is create.
            - Used if I(command) is update.
        type: str
        required: false
    volume_ids:
        description:
            - Ids of volumes which should be archived.
            - Used if I(command) is create.
            - Required if I(command) is add_volumes or remove_volumes.
        type: list
        elements: str
        required: false
    schedules:
        description:
            - Schedules.
            - Used if I(command) is create.
            - Required if I(command) is add_schedules.
        type: list
        elements: dict
        required: false
    schedule_ids:
        description:
            - Schedule ids list.
            - Required if I(command) is remove_schedules.
        type: list
        elements: str
        required: false
    action:
        description:
            - Policy action.
            - Used if I(command) is create.
        choices: [volume_snapshot]
        type: str
        required: false
    status:
        description:
            - Lifecycle policys status.
            - Used if I(command) is create or update.
        choices: [active, paused]
        type: str
        required: false
extends_documentation_fragment:
    - gcore.cloud.cloud.documentation
"""

EXAMPLES = """
- name: Create blank policy
  gcore.cloud.lifecycle_policy:
    api_token: "{{ api_token }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: create
    name: "my-policy"
    action: "volume_snapshot"

- name: Update policy
  gcore.cloud.lifecycle_policy:
    api_token: "{{ api_token }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: update
    lifecycle_policy_id: "{{ lifecycle_policy_id }}"
    name: "new-name"

- name: Add volume to policy
  gcore.cloud.lifecycle_policy:
    api_token: "{{ api_token }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: add_volumes
    lifecycle_policy_id: "{{ lifecycle_policy_id }}"
    volume_ids: ["{{ volume_id }}"]

- name: Remove volume from policy
  gcore.cloud.lifecycle_policy:
    api_token: "{{ api_token }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: remove_volumes
    lifecycle_policy_id: "{{ lifecycle_policy_id }}"
    volume_ids: ["{{ volume_id }}"]

- name: Add schedules to policy
  gcore.cloud.lifecycle_policy:
    api_token: "{{ api_token }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: add_schedules
    lifecycle_policy_id: "{{ lifecycle_policy_id }}"
    schedules: ["{{ schedules }}"]

- name: Remove schedules from policy
  gcore.cloud.lifecycle_policy:
    api_token: "{{ api_token }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: remove_schedules
    lifecycle_policy_id: "{{ lifecycle_policy_id }}"
    schedule_ids: ["{{ schedule_id }}"]

- name: Delete schedules from policy
  gcore.cloud.lifecycle_policy:
    api_token: "{{ api_token }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: delete
    lifecycle_policy_id: "{{ lifecycle_policy_id }}"
"""

RETURN = """
lifecycle_policy:
    description:
        - Resouce dictionary.
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
"""

from traceback import format_exc

from ansible.module_utils.basic import AnsibleModule, to_native

from ansible_collections.gcore.cloud.plugins.module_utils.clients.lifecycle_policy import (
    LifecyclePolicyManageAction,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.lifecycle_policy import (
    LifecyclePolicyAction,
    LifecyclePolicyStatus,
)
from ansible_collections.gcore.cloud.plugins.module_utils.cloud import (
    AnsibleCloudClient,
)


def manage(module: AnsibleModule):
    api = AnsibleCloudClient(module)
    command = module.params.pop("command")
    result = api.lifecycle_policy.execute_command(command=command)
    module.exit_json(**result)


def main():
    module_spec = dict(
        command=dict(type="str", choices=list(LifecyclePolicyManageAction), required=True),
        lifecycle_policy_id=dict(type="str", required=False),
        name=dict(type="str", required=False),
        volume_ids=dict(type="list", elements="str", required=False),
        schedules=dict(type="list", elements="dict", required=False),
        schedule_ids=dict(type="list", elements="str", required=False),
        action=dict(type="str", choices=list(LifecyclePolicyAction), required=False),
        status=dict(type="str", choices=list(LifecyclePolicyStatus), required=False),
    )
    spec = AnsibleCloudClient.get_api_spec()
    spec.update(module_spec)
    module = AnsibleModule(argument_spec=spec, supports_check_mode=True)
    try:
        manage(module)
    except Exception as exc:
        module.fail_json(msg=to_native(exc), exception=format_exc())


if __name__ == "__main__":
    main()
