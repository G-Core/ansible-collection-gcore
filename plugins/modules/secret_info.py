# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: secret_info
author:
    - GCore (@GCore)
short_description: Gather infos about all GCore secrets.
description:
    - Gather infos about all GCore secrets.

options:
    secret_id:
        description:
            - The ID of secret you want to get.
            - The module will fail if the provided ID is invalid.
        type: str
        required: false
extends_documentation_fragment:
    - gcore.cloud.cloud.documentation
"""

EXAMPLES = """
- name: Gather gcore secrets info
  gcore.cloud.secret_info:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"

- name: Gather gcore specific secret info
  gcore.cloud.secret_info:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    secret_id: "{{ secret_id }}"
"""

RETURN = """
secret_info:
    description:
        - When I(secret_id) is passed, it is a dict of resource.
        - Otherwise it is a list of dictionaries.
    returned: always
    type: complex
    contains:
        algorithm:
            description: Metadata provided by a user or system for informational purposes
            returned: always
            type: str
            sample: aes
        bit_length:
            description: Metadata provided by a user or system for informational purposes
            returned: always
            type: int
            sample: 256
        content_types:
            description: Describes the content-types that can be used to retrieve the payload
            returned: always
            type: dict
            sample: {'default': 'application/octet-stream'}
        created:
            description: Datetime when the secret was created
            returned: always
            type: str
            sample: '2023-03-23T20:00:00+00:00'
        expiration:
            description: Datetime when the secret will expire
            returned: always
            type: str
            sample: '2023-06-23T20:00:00+00:00'
        mode:
            description: Metadata provided by a user or system for informational purposes
            returned: always
            type: str
            sample: cbc
        name:
            description: Secret name
            returned: always
            type: str
            sample: 'AES key'
        id:
            description: Secret ID
            returned: always
            type: str
            sample: bfc7824b-31b6-4a28-a0c4-7df137139215
        secret_type:
            description: Secret type, base64 encoded.
            returned: always
            type: str
            sample: opaque
        status:
            description: Status
            returned: always
            type: str
            sample: ACTIVE
"""

from traceback import format_exc

from ansible.module_utils.basic import AnsibleModule, to_native

from ansible_collections.gcore.cloud.plugins.module_utils.cloud import (
    AnsibleCloudClient,
)


def manage(module: AnsibleModule):
    api = AnsibleCloudClient(module)
    secret_id = module.params.get("secret_id")
    command = "get_by_id" if secret_id else "get_list"
    result = api.secrets.execute_command(command=command)
    module.exit_json(**result)


def main():
    module_spec = dict(
        secret_id=dict(type="str", required=False),
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
