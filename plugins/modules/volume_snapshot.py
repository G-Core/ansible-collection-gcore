# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: volume_snapshot
author:
    - GCore (@GCore)
short_description: Manages snapshots
description:
    - Create or delete snapshot for volume

options:
    command:
        description:
            - Operation to perform.
        choices: [create, delete]
        required: true
        type: str
    snapshot_id:
        description:
            - Snapshot ID.
            - Required if I(command) is delete
        type: str
        required: false
    volume_id:
        description:
            - Volume ID to make snapshot of.
            - Required if I(command) is create
        type: str
        required: false
    name:
        description:
            - Snapshot name.
            - Required if I(command) is create.
        type: str
        required: false
    description:
        description:
            - Snapshot description.
            - Used if I(command) is create.
        type: str
        required: false
    metadata:
        description:
            - Snapshot metadata.
            - Used if I(command) is create.
        type: dict
        required: false
extends_documentation_fragment:
    - gcore.cloud.cloud.documentation
"""

EXAMPLES = """
- name: Create new snapshot
  gcore.cloud.volume_snapshot:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: create
    volume_id: "{{ volume_id }}"
    name: "test-snap"
    description: "after boot"

- name: Delete snapshot
  gcore.cloud.volume_snapshot:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: delete
    snapshot_id: "{{ snapshot_id }}"
"""

RETURN = """
volume_snapshot:
    description:
        - Response depends of I(command).
        - If I(command) is create then response will be a dict of resource.
        - If I(command) is delete then response will be a dict of resource ID.
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
            sample: test
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

from ansible_collections.gcore.cloud.plugins.module_utils.clients.snapshot import (
    SnapshotManageAction,
)
from ansible_collections.gcore.cloud.plugins.module_utils.cloud import (
    AnsibleCloudClient,
)


def manage(module: AnsibleModule):
    api = AnsibleCloudClient(module)
    command = module.params.pop("command")
    result = api.snapshots.execute_command(command=command)
    module.exit_json(**result)


def main():
    module_spec = dict(
        command=dict(
            type="str",
            choices=list(SnapshotManageAction),
            required=True,
        ),
        snapshot_id=dict(
            type="str",
            required=False,
        ),
        volume_id=dict(
            type="str",
            required=False,
        ),
        name=dict(
            type="str",
            required=False,
        ),
        description=dict(
            type="str",
            required=False,
        ),
        metadata=dict(
            type="dict",
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
