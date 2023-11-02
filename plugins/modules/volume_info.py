# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: volume_info
author:
    - GCore (@GCore)
short_description: Gather infos about all GCore volumes.
description:
    - Gather infos about all GCore volumes.

options:
    volume_id:
        description:
            - The ID of volume you want to get.
            - The module will fail if the provided ID is invalid.
        type: str
        required: false
    instance_id:
        description:
            - Can be used to only show volumes of a specific instance
        type: str
        required: false
    cluster_id:
        description:
            - Can be used to only show volumes of a specific k8s cluster
        type: str
        required: false
    limit:
        description:
            - Limit the number of returned volumes
        type: int
        required: false
    offset:
        description:
            - Offset value is used to exclude the first set of records from the result
        type: int
        required: false
    has_attachments:
        description:
            - Filter by the presence of attachments
        type: bool
        required: false
    id_part:
        description:
            - Filter the volume list result by the ID part of the volume
        type: str
        required: false
    name_part:
        description:
            - Filter out volumes by name_part inclusion in volume name
        type: str
        required: false
    metadata_k:
        description:
            - Filter by metadata keys. Must be a valid JSON string
        type: str
        required: false
    metadata_kv:
        description:
            - Filter by metadata key-value pairs. Must be a valid JSON string
        type: str
        required: false
extends_documentation_fragment:
    - gcore.cloud.gcore.documentation
"""

EXAMPLES = """
- name: Gather gcore volume infos
  gcore.cloud.volume_info:
    api_key: "{{ api_key }}"

- name: Gather gcore specific volume info
  gcore.cloud.volume_info:
    volume_id: "{{ volume_id }}"
    api_key: "{{ api_key }}"
"""

RETURN = """
volume_info:
    description:
        - When I(volume_id) is passed, it is a dict of resource.
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
        instance_id:
            description: Instance ID
            returned: if available
            type: str
            sample: b10dd116-07f5-4225-abb7-f42da5cb78fb
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
from ansible_collections.gcore.cloud.plugins.module_utils.gcore import AnsibleGCore


def manage(module: AnsibleModule):
    api = AnsibleGCore(module)
    volume_id = module.params.pop("volume_id", None)
    if volume_id:
        result = api.volumes.get_by_id(volume_id)
    else:
        result = api.volumes.get_list(**module.params)
    module.exit_json(changed=False, data=result)


def main():
    module_spec = dict(
        volume_id=dict(type="str", required=False),
        instance_id=dict(type="str", required=False),
        cluster_id=dict(type="str", required=False),
        limit=dict(type="int", required=False),
        offset=dict(type="int", required=False),
        has_attachments=dict(type="bool", required=False),
        id_part=dict(type="str", required=False),
        name_part=dict(type="str", required=False),
        metadata_k=dict(type="str", required=False),
        metadata_kv=dict(type="str", required=False),
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
