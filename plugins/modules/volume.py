# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: volume
author:
    - GCore (@GCore)
short_description: Manages volumes
description:
    - Create/update/delete or attach/detach or retype/revert or extend volume

options:
    command:
        description:
            - Operation to perform.
        choices: [create, update, delete, attach, detach, extend, retype, revert]
        required: true
        type: str

    volume_id:
        description:
            - Volume ID
        type: str
    type_name:
        description:
            - One of 'standard', 'ssd_hiiops', 'cold', 'ultra', 'ssd_lowlatency'.
            - If not specified for - source 'snapshot', volume type will be derived from the snapshot volume.
            - Otherwise defaults to standard.
            - Required if I(command) is create
        choices: [standard, ssd_hiiops, cold, ultra, ssd_local, ssd_lowlatency]
        type: str
    volume_type:
        description:
            - Volume type. Must be one of standard or ssd_hiiops
            - Required if I(command) is retype
        choices: [standard, ssd_hiiops]
        type: str
    name:
        description:
            - Volume name
            - Required if I(command) is create
        type: str
    instance_id_to_attach_to:
        description:
            - VM instance_id to attach newly-created volume to
            - Used if I(command) is create
        type: str
    attachment_tag:
        description:
            - Block device attachment tag (exposed in the metadata).
            - Only used in conjunction with instance_id_to_attach_to.
            - Used if I(command) is create
        type: str
    lifecycle_policy_ids:
        description:
            - Lifecycle policy ID list
            - Used if I(command) is create
        type: list
        elements: int
    metadata:
        description:
            - Create one or more metadata items for a volume
            - Used if I(command) one of create
        type: dict
    size:
        description:
            - Volume size. Must be positive integer
            - Used if I(command) one of create
        type: int
    source:
        description:
            - Source of new volume
            - Required if I(command) is create
        choices: [image, snapshot, new-volume]
        type: str
    image_id:
        description:
            - Image ID
            - Required if I(command) is create and I(source) is image
        type: str
    snapshot_id:
        description:
            - Snapshot ID
            - Required if I(command) is create
        type: str
    instance_id:
        description:
            - Instance ID attach to
            - Required if I(command) is attach
        type: str
    snapshots:
        description:
            - Comma separated list of snapshot IDs to be deleted with the volume
            - Used if I(command) is delete
        type: str
extends_documentation_fragment:
    - gcore.cloud.cloud.documentation
"""

EXAMPLES = """
- name: Create a new empty volume
  gcore.cloud.volume:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: create
    source: new-volume
    type_name: standard
    name: test-volume
    size: 2

- name: Create a new volume from image
  gcore.cloud.volume:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: create
    source: image
    type_name: standard
    image_id: "{{ image_id }}"
    name: test-volume
    size: 5

- name: Create a new volume from snapshot
  gcore.cloud.volume:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: create
    source: snapshot
    type_name: standard
    snapshot_id: "{{ snapshot_id }}"
    name: test-volume
    size: 5

- name: Extend existing volume
  gcore.cloud.volume:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: extend
    volume_id: "{{ volume_id }}"
    size: 20

- name: Attach existing volume to instance
  gcore.cloud.volume:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: attach
    volume_id: "{{ volume_id }}"
    instance_id: "{{ instance_id }}"

- name: Detach existing volume from instance
  gcore.cloud.volume:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: detach
    volume_id: "{{ volume_id }}"
    instance_id: "{{ instance_id }}"

- name: Update existing volume's name
  gcore.cloud.volume:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: update
    volume_id: "{{ volume_id }}"
    name: new-volume-name

- name: Retype existing volume
  gcore.cloud.volume:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: retype
    volume_id: "{{ volume_id }}"
    volume_type: "{{ volume_type }}"

- name: Revert existing volume
  gcore.cloud.volume:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: revert
    volume_id: "{{ volume_id }}"

- name: Delete existing volume
  gcore.cloud.volume:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: delete
    volume_id: "{{ volume_id }}"
"""

RETURN = """
volume:
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
            description: Volume ID
            returned: always
            type: str
            sample: 726ecfcc-7fd0-4e30-a86e-7892524aa483
        name:
            description: Volume name
            returned: always
            type: str
            sample: 123
        status:
            description: Volume status
            returned: always
            type: str
            sample: available
        size:
            description: Volume size, GiB
            returned: always
            type: int
            sample: 2
        created_at:
            description: Datetime when the volume was created
            returned: always
            type: str
            sample: 2019-05-29T05:32:41+0000
        updated_at:
            description: Datetime when the volume was last updated
            returned: always
            type: str
            sample: 2019-05-29T05:39:20+0000
        volume_type:
            description: Volume type
            returned: always
            type: str
            sample: standard
        device:
            description: Device name
            returned: if available
            type: str
            sample: test
        bootable:
            description: Bootable boolean flag
            returned: if available
            type: bool
            sample: false
        attachments:
            description: Attachment list
            returned: if available
            type: list
            sample: [
                {
                    'attached_at': '2019-07-26T14:22:03.000000',
                    'attachment_id': 'f2ed59d9-8068-400c-be4b-c4501ef6f33c',
                    'device': '/dev/vda',
                    'instance_name': '123',
                    'server_id': '8dc30d49-bb34-4920-9bbd-03a2587ec0ad',
                    'volume_id': '67baa7d1-08ea-4fc5-bef2-6b2465b7d227',
                }
            ]
        metadata:
            description: Metadata
            returned: if available
            type: dict
            sample: {'attached_mode': 'rw', 'task_id': 'd74c2bb9-cea7-4b23-a009-2f13518ae66d'}
        metadata_detailed:
            description: Volume metadata
            returned: if available
            type: list
            sample: [{'key': 'attached_mode', 'value': 'rw', 'read_only': True}]
        volume_image_metadata:
            description: Image information for volumes that were created from image
            returned: if available
            type: dict
            sample: {
                'checksum': 'ba3cd24377dde5dfdd58728894004abb',
                'container_format': 'bare',
                'disk_format': 'raw',
                'image_id': '723037e2-ec6d-47eb-92de-6276c8907839',
                'image_name': 'cirros-gcloud',
                'min_disk': '1',
                'min_ram': '0',
                'owner_specified.openstack.md5': 'ba3cd24377dde5dfdd58728894004abb',
                'owner_specified.openstack.object': 'images/cirros-gcloud',
                'owner_specified.openstack.sha256': '87ddf8eea6504b5eb849e418a568c4985d3cea59b5a5d069e1dc644de676b4ec',
                'size': '46137344'
            }
        creator_task_id:
            description: Task that created this entity
            returned: if available
            type: str
            sample: d74c2bb9-cea7-4b23-a009-2f13518ae66d
        task_id:
            description: Active task. If None, action has been performed immediately in the request itself
            returned: present
            type: str
            sample: 907a87b0-7b63-4fd5-beb3-5ab4ba445c93
        snapshot_ids:
            description: Snapshots of this volume
            returned: if available
            type: list
            sample: [907a87b0-7b63-4fd5-beb3-5ab4ba445c93]
        limiter_stats:
            description: Snapshots of this volume
            returned: if available
            type: dict
            sample: {
                'MBps_base_limit': 10,
                'MBps_burst_limit': 100,
                'iops_base_limit': 12,
                'iops_burst_limit': 120,
            }
        is_root_volume:
            description: Root volume flag
            returned: if available
            type: bool
            sample: false
"""

from traceback import format_exc

from ansible.module_utils.basic import AnsibleModule, to_native
from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.volume import (
    RetypableVolumeType,
    VolumeSource,
    VolumeType,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.volume import (
    VolumeManageAction,
)
from ansible_collections.gcore.cloud.plugins.module_utils.cloud import (
    AnsibleCloudClient,
)


def manage(module: AnsibleModule):
    api = AnsibleCloudClient(module)
    command = module.params.pop("command")
    result = api.volumes.execute_command(command=command)
    module.exit_json(**result)


def main():
    module_spec = dict(
        command=dict(
            type="str",
            choices=list(VolumeManageAction),
            required=True,
        ),
        volume_id=dict(
            type="str",
            required=False,
        ),
        type_name=dict(
            type="str",
            choices=list(VolumeType),
            required=False,
        ),
        volume_type=dict(
            type="str",
            choices=list(RetypableVolumeType),
            required=False,
        ),
        name=dict(
            type="str",
        ),
        instance_id_to_attach_to=dict(
            type="str",
            required=False,
        ),
        attachment_tag=dict(
            type="str",
            required=False,
        ),
        lifecycle_policy_ids=dict(
            type="list",
            elements="int",
            required=False,
        ),
        metadata=dict(
            type="dict",
            required=False,
        ),
        size=dict(
            type="int",
            required=False,
        ),
        source=dict(
            type="str",
            choices=list(VolumeSource),
            required=False,
        ),
        image_id=dict(
            type="str",
            required=False,
        ),
        snapshot_id=dict(
            type="str",
        ),
        instance_id=dict(
            type="str",
        ),
        snapshots=dict(
            type="str",
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
