# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: gcore_image_info
author:
    - GCore (@GCore)
short_description: Gather infos about all GCore images.
description:
    - Gather infos about all GCore images.

options:
    image_id:
        description:
            - The ID of the image you want to get.
            - The module will fail if the provided ID is invalid.
        type: str
        required: false
    visibility:
        description:
            - Image visibility. Globally visible images are public.
        type: str
        choices: [ private, public, shared ]
        required: false
    private:
        description:
            - Any value to show private images
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
    - community.gcore.gcore.documentation
"""

EXAMPLES = """
- name: Gather gcore image infos
  community.gcore.gcore_image_info:
    api_token: "{{ api_token }}"

- name: Gather gcore specific image info
  community.gcore.gcore_image_info:
    image_id: "{{ image_id }}"
    api_token: "{{ api_token }}"
"""

RETURN = """
gcore_image_info:
    description:
        - When I(image_id) is passed, it is a dict of resource.
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
        disk_format:
            description: Disk format
            returned: if available
            type: str
            sample: raw
        hw_machine_type:
            description: A virtual chipset type
            returned: if available
            type: str
            sample: q35
        id:
            description: Image ID
            returned: always
            type: str
            sample: 44e136a7-15c1-4b5f-a086-20b7b3237d40
        min_disk:
            description: Minimal boot volume required
            returned: if available
            type: int
            sample: 3
        os_type:
            description: The operating system installed on the image
            returned: if available
            type: str
            sample: linux
        architecture:
            description: An image architecture type
            returned: if available
            type: str
            sample: x86_64
        ssh_key:
            description: Whether the image supports SSH key or not
            returned: if available
            type: str
            sample: allow
        min_ram:
            description: Minimal VM RAM required
            returned: if available
            type: int
            sample: 0
        os_version:
            description: OS version, i.e. 19.04 (for Ubuntu) or 9.4 for Debian
            returned: if available
            type: str
            sample: 20.10
        task_id:
            description: Active task. If None, action has been performed immediately in the request itself
            returned: present
            type: str
            sample: 907a87b0-7b63-4fd5-beb3-5ab4ba445c93
        visibility:
            description: Image visibility. Globally visible images are public
            returned: if available
            type: str
            sample: public
        display_order:
            description: Display order
            returned: if available
            type: int
            sample: 2010
        status:
            description: Image status, i.e. active
            returned: if available
            type: str
            sample: active
        size:
            description: Image size in bytes
            returned: if available
            type: int
            sample: 2361393152
        updated_at:
            description: Datetime when the image was updated
            returned: changed
            type: str
            sample: 2020-12-18T14:51:20+0000
        created_at:
            description: Datetime when the image was created
            returned: always
            type: str
            sample: 2020-11-13T11:26:19+0000
        name:
            description: Image display name
            returned: always
            type: str
            sample: ubuntu-20.10-x64
        creator_task_id:
            description: Task that created this entity
            returned: if available
            type: str
            sample: b10dd116-07f5-4225-abb7-f42da5cb78fb
        description:
            description: Image description
            returned: if available
            type: str
            sample: Test image
        is_baremetal:
            description: Set to true if the image will be used by baremetal instances. Defaults to false
            returned: if availble
            type: bool
            sample: false
        hw_firmware_type:
            description: Specifies the type of firmware with which to boot the guest
            returned: if available
            type: str
            sample: bios
        os_distro:
            description: OS Distribution, i.e. Debian, CentOS, Ubuntu, CoreOS etc
            returned: if available
            type: str
            sample: ubuntu
        metadata:
            description: Metadata
            returned: if available
            type: dict
            sample: {'key': 'value'}
        metadata_detailed:
            description: Image metadata
            returned: if available
            type: list
            sample: [{'key': 'key', 'value': 'value', 'read_only': False}]
        price_per_hour:
            description: Price per hour
            returned: if available
            type: int
            sample: 1
        price_per_month:
            description: Price per month
            returned: if available
            type: int
            sample: 720
        price_status:
            description: Price status
            returned: if available
            type: str
            sample: show
        currency_code:
            description: Currency code
            returned: if available
            type: str
            sample: USD
"""

from traceback import format_exc

from ansible.module_utils.basic import AnsibleModule, to_native

from ..module_utils.gcore import AnsibleGCore


def manage(module: AnsibleModule):
    api = AnsibleGCore(module)
    image_id = module.params.get("image_id")
    if image_id:
        result = api.images.get_by_id(image_id)
    else:
        result = api.images.get_list()
    module.exit_json(changed=False, data=result)


def main():
    module_spec = dict(
        image_id=dict(
            type="str",
            required=False,
        ),
        visibility=dict(
            type="str",
            required=False,
            choices=["private", "public", "shared"],
        ),
        private=dict(
            type="str",
            required=False,
        ),
        metadata_k=dict(
            type="str",
            required=False,
        ),
        metadata_kv=dict(
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
