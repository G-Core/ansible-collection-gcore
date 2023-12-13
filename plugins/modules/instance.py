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
        type: list
        elements: dict
        required: false
    volumes_to_delete:
        description:
            - Comma separated list of volume IDs to be deleted with the instance.
            - Used if I(command) is delete.
        type: str
        required: false
    security_groups:
        description:
            - Security group UUIDs.
            - Optional if I(command) is create.
        type: list
        elements: dict
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
    - gcore.cloud.cloud.documentation
"""

EXAMPLES = """
- name: Create instance from volume
  gcore.cloud.instance:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: create
    names: [Test]
    flavor: g1-standard-1-2
    volumes: [{
        'source': 'image',
        'image_id': '55d662eb-b2d5-4b3c-bc84-a2265e25c86e',
        'size': 20,
        'boot_index': 0,
    }]
    interfaces: [{
        'type': 'external'
    }]

- name: Create instance from snapshot
  gcore.cloud.instance:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: create
    names: [Test]
    flavor: g1-standard-1-2
    volumes: [{
        'source': 'snapshot',
        'image_id': '55d662eb-b2d5-4b3c-bc84-a2265e25c86e',
        'size': 20,
        'boot_index': 0,
    }]
    interfaces: [{
        'type': 'external'
    }]

- name: Rename instance
  gcore.cloud.instance:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: update
    instance_id: "{{ instance_id }}"
    name: "new-name"

- name: Stop instance
  gcore.cloud.instance:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: stop
    instance_id: "{{ instance_id }}"

- name: Start instance
  gcore.cloud.instance:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: start
    instance_id: "{{ instance_id }}"

- name: Powercycle instance
  gcore.cloud.instance:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: powercycle
    instance_id: "{{ instance_id }}"

- name: Reboot instance
  gcore.cloud.instance:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: reboot
    instance_id: "{{ instance_id }}"

- name: Suspend instance
  gcore.cloud.instance:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: suspend
    instance_id: "{{ instance_id }}"

- name: Resume instance
  gcore.cloud.instance:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: resume
    instance_id: "{{ instance_id }}"

- name: Delete instance
  gcore.cloud.instance:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: delete
    instance_id: "{{ instance_id }}"
"""

RETURN = """
instance_info:
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
        instance_id:
            description: Region ID
            returned: always
            type: str
            sample: a7e7e8d6-0bf7-4ac9-8170-831b47ee2ba9
        flavor:
            description: Flavor
            returned: always
            type: dict
            sample: {
                'disk': 0,
                'flavor_id': 'g1s-shared-1-0.5',
                'flavor_name': 'g1s-shared-1-0.5',
                'ram': 512,
                'vcpus': 1,
            }
        metadata:
            description: Metadata
            returned: if available
            type: dict
            sample: {
                'image_id': 'f01fd9a0-9548-48ba-82dc-a8c8b2d6f2f1',
                'image_name': 'cirros-0.3.5-x86_64-disk',
                'os_distro': 'centos',
                'os_version': '1711-x64',
                'snapshot_id': 'c286cd13-fba9-4302-9cdb-4351a05a56ea',
                'snapshot_name': 'test_snapshot',
                'task_id': 'd1e1500b-e2be-40aa-9a4b-cc493fa1af30',
            }
        metadata_detailed:
            description: Detailed VM metadata
            returned: if available
            type: list
            sample: [{
                'key': 'task_id',
                'value': 'd1e1500b-e2be-40aa-9a4b-cc493fa1af30',
                'read_only': True,
            }]
        instance_name:
            description: Instance name
            returned: always
            type: str
            sample: Testing
        instance_description:
            description: Instance description
            returned: always
            type: str
            sample: Testing
        instance_created:
            description: Datetime when instance was created
            returned: always
            type: str
            sample: "2019-07-11T06:58:48Z"
        status:
            description: VM status
            returned: always
            type: str
            sample: ACTIVE
        vm_state:
            description: Virtual machine state
            returned: always
            type: str
            sample: active
        task_state:
            description: Task state
            returned: always
            type: str
            sample: None
        volumes:
            description: List of volumes
            returned: always
            type: dict
            sample: [{
                'delete_on_termination': False,
                'id': '28bfe198-a003-4283-8dca-ab5da4a71b62',
            }]
        addresses:
            description: Map of network_name
            returned: always
            type: dict
            sample: {
                'net1': [
                    {
                        'addr': '10.0.0.17',
                        'type': 'fixed',
                        'subnet_name': 'string',
                        'subnet_id': '91200a6c-07e0-42aa-98da-32d1f6545ae7',
                    },
                    {
                        'addr': '92.38.157.215',
                        'type': 'floating',
                        'subnet_name': 'string',
                        'subnet_id': '91200a6c-07e0-42aa-98da-32d1f6545ae7',
                    },
                ],
                'net2': [
                    {
                        'addr': '192.168.68.68',
                        'type': 'fixed',
                        'subnet_name': 'string',
                        'subnet_id': '91200a6c-07e0-42aa-98da-32d1f6545ae7',
                    }
                ],
            }
        security_groups:
            description: Security groups
            returned: if available
            type: list
            sample: [{'name': 'default'}]
        creator_task_id:
            description: Task that created this entity
            returned: if available
            type: str
            sample: d1e1500b-e2be-40aa-9a4b-cc493fa1af30
        task_id:
            description: Active task. If None, action has been performed immediately in the request itself
            returned: always
            type: str
            sample: f28a4982-9be1-4e50-84e7-6d1a6d3f8a02
        keypair_name:
            description: Keypair name
            returned: if available
            type: str
            sample: None
        blackhole_ports:
            description: IP addresses of the instances that are blackholed by DDoS mitigation system
            returned: if available
            type: list
            sample: [
                {
                    'ID': 1,
                    'AlertDuration': '2 hours',
                    'DestinationIP': '92.38.162.134',
                    'AlarmStart': '2021-03-17T14:24:06',
                    'AlarmEnd': '2021-03-17T16:24:06',
                    'AlarmState': 'ALARM',
                }
            ]
"""

from traceback import format_exc

from ansible.module_utils.basic import AnsibleModule, to_native
from ansible_collections.gcore.cloud.plugins.module_utils.clients.instance import (
    InstanceManageAction,
)
from ansible_collections.gcore.cloud.plugins.module_utils.cloud import (
    AnsibleCloudClient,
)


def manage(module: AnsibleModule):
    api = AnsibleCloudClient(module)
    command = module.params.pop("command")
    result = api.instances.execute_command(command=command)
    module.exit_json(**result)


def main():
    module_spec = dict(
        command=dict(
            type="str",
            choices=list(InstanceManageAction),
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
            elements="dict",
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
        volumes_to_delete=dict(
            type="str",
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
