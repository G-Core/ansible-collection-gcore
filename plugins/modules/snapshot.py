# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: snapshot
author:
    - GCore (@GCore)
short_description: Manages snapshots
description:
    - Manages snapshots

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
        type: str
        required: false
extends_documentation_fragment:
    - gcore.cloud.gcore.documentation
"""

EXAMPLES = """
- name: Create new snapshot
  gcore.cloud.snapshot:
    api_key: "{{ api_key }}"
    command: create
    volume_id: "67baa7d1-08ea-4fc5-bef2-6b2465b7d227"
    name: "test-snap"
    description: "after boot"

- name: Delete snapshot
  gcore.cloud.snapshot:
    api_key: "{{ api_key }}"
    command: delete
    snapshot_id: "481797e0-472b-439e-86df-5b651279015d"
"""

RETURN = """
snapshot:
    description:
        - Dictionary with list of tasks
    returned: always
    type: complex
    contains:
        tasks:
            description: Task ID list object
            returned: always
            type: list
            elements: str
            sample: ['d478ae29-dedc-4869-82f0-96104425f565', '50f53a35-42ed-40c4-82b2-5a37fb3e00bc']
"""

from traceback import format_exc

from ansible.module_utils.basic import AnsibleModule, to_native
from ansible_collections.gcore.cloud.plugins.module_utils.clients.snapshot import (
    SnapshotAction,
)
from ansible_collections.gcore.cloud.plugins.module_utils.gcore import AnsibleGCore


def manage(module: AnsibleModule):
    api = AnsibleGCore(module)
    command = module.params.pop("command")
    result = api.snapshots.execute_command(command=command, params=module.params)
    module.exit_json(changed=False, data=result)


def main():
    module_spec = dict(
        command=dict(
            type="str",
            choices=list(SnapshotAction),
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
            type="str",
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
