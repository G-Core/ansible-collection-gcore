# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: instance
author:
    - GCore (@GCore)
short_description: Manages instances.
description:
    - Create, update, delete, start, stop, powercycle, reboot, suspend or resume instance.

options:
    command:
        description:
            - Operation to perform.
        choices: [create, update, delete, start, stop, powercycle, reboot, suspend, resume]
        required: true
        type: str
    instance_id:
        description:
            - Instance ID.
            - Required for some operations.
        type: str
        required: false
    flavor:
        description:
            - Flavor ID.
            - Required if I(command) is create.
        type: str
        required: false
    keypair_name:
        description:
            - Keypair name to inject into new instance(s).
            - Optional if I(command) is create.
        type: str
        required: false
    user_data:
        description:
            - String in base64 format. Must not be passed together with username or password.
            - Optional if I(command) is create.
        type: str
        required: false
    username:
        description:
            - A name of a new user in the Linux VM. It may be passed with a password parameter.
            - Optional if I(command) is create.
        type: str
        required: false
    password:
        description:
            - A password for VM. This parameter is used to set a password for the Admin.
            - Optional if I(command) is create.
        type: str
        required: false
    name:
        description:
            - New instance names.
            - Required if I(command) is update.
        type: str
        required: false
    names:
        description:
            - List of instance names.
            - Required if I(command) is create and I(name_templates) are not passed.
        type: list
        elements: str
        required: false
    name_templates:
        description:
            - List of instance names which will be changed by template.
            - You can use forms ip_octets, two_ip_octets, one_ip_octet.
            - Required if I(command) is create and I(names) are not passed.
        type: list
        elements: str
        required: false
    interfaces:
        description:
            - Subnet IPs and floating IPs.
            - Required if I(command) is create.
        type: list
        elements: dict
        required: false
    metadata:
        description:
            - Create one or more metadata items for an instance.
            - Optional if I(command) is create.
        type: dict
        required: false
    volumes:
        description:
            - List of volumes for instances.
            - Required if I(command) is create.
            - Optional if I(command) is delete.
        type: list
        elements: dict
        required: false
    security_groups:
        description:
            - Security group UUIDs.
            - Optional if I(command) is create.
        type: list
        elements: str
        required: false
    configuration:
        description:
            - Parameters for the application template from the marketplace.
            - Optional if I(command) is create.
        type: dict
        required: false
    allow_app_ports:
        description:
            - If true, application ports will be allowed in the security group for instances created from
            - the marketplace application template.
            - Optional if I(command) is create.
        type: bool
        required: false
    servergroup_id:
        description:
            - Anti-affinity or affinity or soft-anti-affinity server group ID.
            - Optional if I(command) is create.
        type: str
        required: false
    floatings:
        description:
            - Floating ids that should be deleted.
            - Optional if I(command) is delete.
        type: list
        elements: str
        required: false
    reserved_fixed_ips:
        description:
            - Port IDs to be deleted with the instance.
            - Optional if I(command) is delete.
        type: list
        elements: str
        required: false
    activate_profile:
        description:
            - Should ddos_profile be activated.
            - Optional if I(command) is start.
        type: bool
        required: false
extends_documentation_fragment:
    - gcore.cloud.gcore.documentation
"""

EXAMPLES = """
- name: Create instance from volume
  gcore.cloud.instance:
    api_token: "{{ api_token }}"
    names: [Test]
    flavor: g1-standard-1-2
    volumes: [{
        'source': 'image',
        'image_id': '55d662eb-b2d5-4b3c-bc84-a2265e25c86e'
    }]
    interfaces: [{
        'type': 'external'
    }]
"""

RETURN = """
instance_info:
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
from ansible_collections.gcore.cloud.plugins.module_utils.clients.instance import (
    InstanceAction,
)
from ansible_collections.gcore.cloud.plugins.module_utils.gcore import AnsibleGCore


def manage(module: AnsibleModule):
    api = AnsibleGCore(module)
    command = module.params.pop("command")
    result = api.instances.execute_command(command=command, params=module.params)
    module.exit_json(changed=False, data=result)


def main():
    module_spec = dict(
        command=dict(
            type="str",
            choices=list(InstanceAction),
            required=True,
        ),
        flavor=dict(
            type="str",
            required=False,
        ),
        keypair_name=dict(
            type="str",
            required=False,
        ),
        user_data=dict(
            type="str",
            required=False,
        ),
        username=dict(
            type="str",
            required=False,
        ),
        password=dict(
            type="str",
            no_log=True,
            required=False,
        ),
        instance_id=dict(
            type="str",
            required=False,
        ),
        names=dict(
            type="list",
            elements="str",
            required=False,
        ),
        name_templates=dict(
            type="list",
            elements="str",
            required=False,
        ),
        interfaces=dict(
            type="list",
            elements="dict",
            required=False,
        ),
        metadata=dict(
            type="dict",
            required=False,
        ),
        volumes=dict(
            type="list",
            elements="dict",
            required=False,
        ),
        security_groups=dict(
            type="list",
            elements="str",
            required=False,
        ),
        configuration=dict(
            type="dict",
            required=False,
        ),
        allow_app_ports=dict(
            type="bool",
            required=False,
        ),
        servergroup_id=dict(
            type="str",
            required=False,
        ),
        floatings=dict(
            type="list",
            elements="str",
            required=False,
        ),
        reserved_fixed_ips=dict(
            type="list",
            elements="str",
            required=False,
        ),
        activate_profile=dict(
            type="bool",
            required=False,
        ),
        name=dict(
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
