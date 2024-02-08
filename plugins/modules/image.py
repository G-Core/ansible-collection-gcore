# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: image
author:
    - GCore (@GCore)
short_description: Manages images
description:
    - Create/update/download or delete image

options:
    command:
        description:
            - Operation to perform.
        choices: [create, update, download, delete]
        required: true
        type: str
    image_id:
        description:
            - The ID of image.
            - Required if I(command) is one of update or delete
        type: str
        required: false
    volume_id:
        description:
            - Volume ID.
            - Required if I(command) is create
        type: str
        required: false
    name:
        description:
            - Image name.
            - Used if I(command) is create or update
        type: str
        required: false
    url:
        description:
            - Image url.
            - Used if I(command) is download
        type: str
        required: false
    ssh_key:
        description:
            - Permission to use a ssh key in instances.
            - Used if I(command) is one of create, update or download.
        choices: [allow, deny, required]
        type: str
        required: false
    is_baremetal:
        description:
            - Set to true if the image will be used by baremetal instances. Defaults to false.
            - Used if I(command) is one of create, update or download.
        type: bool
        required: false
    os_type:
        description:
            - The operating system installed on the image.
            - Used if I(command) is one of create, update or download.
        type: str
        choices: [linux, windows]
        required: false
    hw_firmware_type:
        description:
            - Specifies the type of firmware with which to boot the guest.
            - Used if I(command) is one of create, update or download.
        type: str
        choices: [bios, uefi]
        required: false
    hw_machine_type:
        description:
            - A virtual chipset type.
            - Used if I(command) is one of create, update or download.
        type: str
        choices: [i440, q35]
        required: false
    architecture:
        description:
            - An image architecture type.
            - Used if I(command) is one of create, update or download.
        type: str
        choices: [aarch64, x86_64]
        required: false
    cow_format:
        description:
            - When True, image cannot be deleted unless all volumes, created from it, are deleted.
            - Used if I(command) is download.
        type: bool
        required: false
    os_distro:
        description:
            - OS Distribution, i.e. Debian, CentOS, Ubuntu, CoreOS etc.
            - Used if I(command) is download.
        type: str
        required: false
    os_version:
        description:
            - OS version, i.e. 19.04 (for Ubuntu) or 9.4 for Debian.
            - Used if I(command) is download.
        type: str
        required: false
    metadata:
        description:
            - Image metadata.
            - Used if I(command) is one of create, update or download.
        type: dict
        required: false
extends_documentation_fragment:
    - gcore.cloud.cloud.documentation
"""

EXAMPLES = """
- name: Create new image
  gcore.cloud.image:
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    api_key: "{{ api_key }}"
    command: create
    name: "test-image"
    volume_id: "{{ volume_id }}"

- name: Download new image
  gcore.cloud.image:
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    api_key: "{{ api_key }}"
    command: download
    name: "test-image"
    url: "{{ image_url }}"

- name: Rename image
  gcore.cloud.image:
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    api_key: "{{ api_key }}"
    command: update
    image_id: "{{ image_id }}"
    name: "new-image-name"

- name: Delete image
  gcore.cloud.image:
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    api_key: "{{ api_key }}"
    command: delete
    image_id: "{{ image_id }}"
"""

RETURN = """
image:
    description:
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
            description: Image ID
            returned: always
            type: str
            sample: 726ecfcc-7fd0-4e30-a86e-7892524aa483
        name:
            description: Image name
            returned: always
            type: str
            sample: 123
        description:
            description: Image description
            returned: always
            type: str
            sample: test
        status:
            description: Image status, i.e. active
            returned: always
            type: str
            sample: 2019-06-19T11:56:16+0000
        visibility:
            description: Image visibility. Globally visible images are public
            returned: always
            type: str
            sample: public
        min_disk:
            description: Minimal boot volume required
            returned: always
            type: int
            sample: 0
        min_ram:
            description: Minimal VM RAM required
            returned: always
            type: int
            sample: 0
        os_distro:
            description: OS Distribution, i.e. Debian, CentOS, Ubuntu, CoreOS etc.
            returned: always
            type: str
            sample: ubuntu
        os_version:
            description: OS version, i.e. 19.04 (for Ubuntu) or 9.4 for Debian.
            returned: always
            type: str
            sample: '20.10'
        ssh_key:
            description: Whether the image supports SSH key or not
            returned: always
            type: str
            elements: str
            sample: allow
        display_order:
            description: Display order
            returned: always
            type: int
            sample: 2010
        created_at:
            description: Datetime when the image was created
            returned: always
            type: str
            sample: 2020-11-13T11:26:19+0000
        updated_at:
            description: Datetime when the image was updated
            returned: if available
            type: str
            sample: 2020-12-18T14:51:20+0000
        size:
            description: Image size in bytes
            returned: always
            type: int
            sample: 2361393152
        creator_task_id:
            description: Image size in bytes
            returned: always
            type: str
            sample: b10dd116-07f5-4225-abb7-f42da5cb78fb
        task_id:
            description: Active task. If None, action has been performed immediately in the request itself.
            returned: always
            type: str
            sample: b10dd116-07f5-4225-abb7-f42da5cb78fb
        disk_format:
            description: Disk format
            returned: always
            type: str
            sample: raw
        is_baremetal:
            description: Set to true if the image will be used by baremetal instances
            returned: always
            type: bool
            sample: false
        os_type:
            description: The operating system installed on the image.
            returned: always
            type: str
            sample: linux
        hw_firmware_type:
            description: Specifies the type of firmware with which to boot the guest.
            returned: always
            type: str
            sample: bois
        hw_machine_type:
            description: A virtual chipset type.
            returned: always
            type: str
            sample: i440
        architecture:
            description: A virtual chipset type.
            returned: always
            type: str
            sample: x86_64
        metadata:
            description: Image metadata.
            returned: always
            type: dict
            sample: {'key': 'value'}
        metadata_detailed:
            description: Detailed image metadata.
            returned: always
            type: dict
            sample: [{'key': 'key', 'value': 'value', 'read_only': False}]
"""

from traceback import format_exc

from ansible.module_utils.basic import AnsibleModule, to_native

from ansible_collections.gcore.cloud.plugins.module_utils.clients.image import (
    ImageManageAction,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.image import (
    HwMachineType,
    ImageArchitectureType,
    ImageHwFirmwareType,
    ImageOsType,
    SshKey,
)
from ansible_collections.gcore.cloud.plugins.module_utils.cloud import (
    AnsibleCloudClient,
)


def manage(module: AnsibleModule):
    api = AnsibleCloudClient(module)
    command = module.params.pop("command")
    result = api.images.execute_command(command=command)
    module.exit_json(**result)


def main():
    module_spec = dict(
        command=dict(type="str", choices=list(ImageManageAction), required=True),
        image_id=dict(type="str", required=False),
        volume_id=dict(type="str", required=False),
        name=dict(type="str", required=False),
        url=dict(type="str", required=False),
        ssh_key=dict(type="str", choices=list(SshKey), required=False),
        is_baremetal=dict(type="bool", required=False),
        os_type=dict(type="str", choices=list(ImageOsType), required=False),
        hw_firmware_type=dict(type="str", choices=list(ImageHwFirmwareType), required=False),
        hw_machine_type=dict(type="str", choices=list(HwMachineType), required=False),
        architecture=dict(type="str", choices=list(ImageArchitectureType), required=False),
        cow_format=dict(type="bool", required=False),
        os_distro=dict(type="str", required=False),
        os_version=dict(type="str", required=False),
        metadata=dict(type="dict", required=False),
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
