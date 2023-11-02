# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: snapshot_info
author:
    - GCore (@GCore)
short_description: Gather infos about all GCore snapshots.
description:
    - Gather infos about all GCore snapshots.

options:
    snapshot_id:
        description:
            - The ID of the snapshot you want to get.
            - The module will fail if the provided ID is invalid.
        type: str
        required: false
    volume_id:
        description:
            - Can be used to list snapshots of a single volume
        type: str
        required: false
    instance_id:
        description:
            - Can be used to list snapshots of any volume in a specific server instance
        type: str
        required: false
    schedule_id:
        description:
            - Can be used to list snapshots by schedule id
        type: str
        required: false
    lifecycle_policy_id:
        description:
            - Can be used to list snapshots by lifecycle policy id
        type: str
        required: false
    limit:
        description:
            - Limit the number of returned snapshots
        type: int
        required: false
    offset:
        description:
            - Offset value is used to exclude the first set of records from the result
        type: int
        required: false
extends_documentation_fragment:
    - gcore.cloud.gcore.documentation
"""

EXAMPLES = """
- name: Gather gcore snapshot infos
  gcore.cloud.snapshot_info:
    api_key: "{{ api_key }}"

- name: Gather gcore snapshots info for specific volume
  gcore.cloud.snapshot_info:
    volume_id: "{{ volume_id }}"
    api_key: "{{ api_key }}"
"""

RETURN = """
snapshot_info:
    description:
        - List of dictionaries.
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
            description: Snapshot ID
            returned: always
            type: str
            sample: 726ecfcc-7fd0-4e30-a86e-7892524aa483
        name:
            description: Snapshot name
            returned: always
            type: str
            sample: '123'
        description:
            description: Snapshot description
            returned: if available
            type: str
            sample: test
        status:
            description: Snapshot status
            returned: always
            type: str
            sample: available
        size:
            description: Snapshot size, GiB
            returned: always
            type: int
            sample: 2
        volume_id:
            description: ID of the volume this snapshot was made from
            returned: always
            type: str
            sample: 67baa7d1-08ea-4fc5-bef2-6b2465b7d227
        created_at:
            description: Datetime when the volume was created
            returned: always
            type: str
            sample: 2019-05-29T05:32:41+0000
        updated_at:
            description: Datetime when the volume was last updated
            returned: if available
            type: str
            sample: 2019-05-29T05:39:20+0000
        creator_task_id:
            description: Task that created this entity
            returned: if available
            type: str
            sample: 2358e3b1-5c42-4705-8950-6ddcfc19c3bd
        task_id:
            description: Active task. If None, action has been performed immediately in the request itself
            returned: if available
            type: str
            sample: 907a87b0-7b63-4fd5-beb3-5ab4ba445c93
        metadata:
            description: Metadata
            returned: if available
            type: dict
            sample: {'bootable': 'False', 'task_id': 'a4d72afa-1c67-44af-9f91-0b893cd204da', 'volume_type': 'standard', 'volume_name': 'namevolume'}
"""

from traceback import format_exc

from ansible.module_utils.basic import AnsibleModule, to_native
from ansible_collections.gcore.cloud.plugins.module_utils.gcore import AnsibleGCore


def manage(module: AnsibleModule):
    api = AnsibleGCore(module)
    snapshot_id = module.params.pop("snapshot_id", None)
    if snapshot_id:
        result = api.snapshots.get_by_id(snapshot_id)
    else:
        result = api.snapshots.get_list(**module.params)
    module.exit_json(changed=False, data=result)


def main():
    module_spec = dict(
        snapshot_id=dict(
            type="str",
            required=False,
        ),
        volume_id=dict(
            type="str",
            required=False,
        ),
        instance_id=dict(
            type="str",
            required=False,
        ),
        schedule_id=dict(
            type="str",
            required=False,
        ),
        lifecycle_policy_id=dict(
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
    spec = AnsibleGCore.get_api_spec()
    spec.update(module_spec)
    module = AnsibleModule(argument_spec=spec, supports_check_mode=True)
    try:
        manage(module)
    except Exception as exc:
        module.fail_json(msg=to_native(exc), exception=format_exc())


if __name__ == "__main__":
    main()
