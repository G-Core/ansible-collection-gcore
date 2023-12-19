# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: keypair
author:
    - GCore (@GCore)
short_description: Manages keypair
description:
    - Create/delete or share keypair

options:
    command:
        description:
            - Operation to perform.
        choices: [create, delete, share]
        required: true
        type: str
    keypair_id:
        description:
            - The ID of keypair
            - Required if I(command) is update or delete
        type: str
        required: false
    shared_in_project:
        description:
            - Keypair is shared.
            - Required if I(command) is share
        type: bool
        required: false
    sshkey_name:
        description:
            - Key name.
            - Required if I(command) is create.
        type: str
        required: false
    public_key:
        description:
            - Public part of the key. To generate public and private keys
            - Used if I(command) is create.
        type: str
        required: false
extends_documentation_fragment:
    - gcore.cloud.cloud.documentation
"""

EXAMPLES = """
- name: Create new keypair
  gcore.cloud.keypair:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: create
    sshkey_name: "alice"

- name: Share keypair in project
  gcore.cloud.keypair:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: share
    keypair_id: "{{ keypair_id }}"
    shared_in_project: true

- name: Un-share keypair in project
  gcore.cloud.keypair:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: share
    keypair_id: "{{ keypair_id }}"
    shared_in_project: false

- name: Delete keypair
  gcore.cloud.keypair:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: delete
    keypair_id: "{{ keypair_id }}"
"""

RETURN = """
network:
    description:
        - Response depends of I(command).
        - If I(command) is one of create or share then response will be resource dictionary.
        - If I(command) is delete then response will be a dict with resource id.
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
from ansible_collections.gcore.cloud.plugins.module_utils.clients.keypair import (
    KeypairManageAction,
)
from ansible_collections.gcore.cloud.plugins.module_utils.cloud import (
    AnsibleCloudClient,
)


def manage(module: AnsibleModule):
    api = AnsibleCloudClient(module)
    command = module.params.pop("command")
    result = api.keypairs.execute_command(command=command)
    module.exit_json(**result)


def main():
    module_spec = dict(
        command=dict(type="str", choices=list(KeypairManageAction), required=True),
        keypair_id=dict(type="str", required=False),
        shared_in_project=dict(type="bool", required=False),
        sshkey_name=dict(type="str", required=False),
        public_key=dict(type="str", required=False),
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
