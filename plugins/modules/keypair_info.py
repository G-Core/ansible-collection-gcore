# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: keypair_info
author:
    - GCore (@GCore)
short_description: Gather infos about all GCore keypairs.
description:
    - Gather infos about all GCore keypairs.

options:
    keypair_id:
        description:
            - The ID of keypair you want to get.
            - The module will fail if the provided ID is invalid.
        type: str
        required: false
extends_documentation_fragment:
    - gcore.cloud.cloud.documentation
"""

EXAMPLES = """
- name: Gather gcore keypairs infos
  gcore.cloud.keypair_info:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"

- name: Gather gcore specific keypair info
  gcore.cloud.keypair_info:
    keypair_id: "{{ keypair_id }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    api_key: "{{ api_key }}"
"""

RETURN = """
keypair_info:
    description:
        - When I(keypair_id) is passed, it is a dict of resource.
        - Otherwise it is a list of dictionaries.
    returned: always
    type: complex
    contains:
        project_id:
            description: Project ID
            returned: always
            type: int
            sample: 1
        sshkey_id:
            description: Key ID, equal to sshkey_name
            returned: always
            type: str
            sample: alice
        public_key:
            description: Public part of the key
            returned: always
            type: str
            sample: '''
                ssh-rsa
                AAAAB3NzaC1yc2EAAAADAQABAAABAQDFHrnwGVBZs6q6vmTBzQFfzdRLQW8N6Rd0ogGe3h8tm83ZJLTTsF+1H4JcOvwI5ETkHMaFIWd2U1
                5nHU5M7plE6UPRKfzy4rq6yI6cE4tojd3A9attMpbEEX7EbGKrbrb4AsjzxHKAVaREAb31ZplJkUlsiees25hTQXBcWQ
                nOESlc9RCxZ/QQgNUUgqm7QGg7CNkL8Mpq9V4YaOhcFGWj0jXP1CL3g6Xe3xJo1CmUbkIOGUyAmrSfLEiy2O91iOUhbm
                YQyXksznNrT9O6uLkijf6syLZOdyAuUd/Z86eYXej4/YsvIA5eIFU4B6y9zOXEO2A81txPYMRAytYt7+e7
                alice@alice
            '''
        private_key:
            description: Private part of the key
            returned: if available
            type: str
            sample: null
        fingerprint:
            description: Key fingerprint
            returned: if available
            type: str
            sample: 86:75:ce:e7:e9:1e:f0:79:ec:6f:d8:92:9b:43:fc:4d
        sshkey_name:
            description: Key name
            returned: always
            type: str
            sample: alice
        state:
            description: Key state
            returned: always
            type: str
            sample: ACTIVE
        shared_in_project:
            description: Keypair is shared for all users in the project
            returned: always
            type: bool
            sample: false
        created_at:
            description:
                - Datetime object. It automatically is being generated when the keypair is created or imported.
            returned: always
            type: str
            sample: '2021-11-10T06:58:11'
"""

from traceback import format_exc

from ansible.module_utils.basic import AnsibleModule, to_native

from ansible_collections.gcore.cloud.plugins.module_utils.cloud import (
    AnsibleCloudClient,
)


def manage(module: AnsibleModule):
    api = AnsibleCloudClient(module)
    keypair_id = module.params.get("keypair_id")
    command = "get_by_id" if keypair_id else "get_list"
    result = api.keypairs.execute_command(command=command)
    module.exit_json(**result)


def main():
    module_spec = dict(
        keypair_id=dict(type="str", required=False),
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
