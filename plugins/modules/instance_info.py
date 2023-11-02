# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: instance_info
author:
    - GCore (@GCore)
short_description: Gather infos about all GCore instances.
description:
    - Gather infos about all GCore instances.

options:
    instance_id:
        description:
            - The ID of instance you want to get.
            - The module will fail if the provided ID is invalid.
        type: str
        required: false
    name:
        description:
            - Filter out instances by name.
        type: str
        required: false
    flavor:
        description:
            - Filter out instances by flavor_id. Flavor id must match exactly.
        type: str
        required: false
    flavor_prefix:
        description:
            - Filter out instances by flavor prefix.
        type: str
        required: false
    status:
        description:
            - Filters instances by a server status, as a string.
        choices: [ACTIVE, ERROR, SHUTOFF, REBOOT, PAUSED]
        type: str
        required: false
    changes_since:
        description:
            - Filters the instances by a date and time stamp when the instances last changed status.
        type: str
        required: false
    changes_before:
        description:
            - Filters the instances by a date and time stamp when the instances last changed.
        type: str
        required: false
    exclude_secgroup:
        description:
            - Exclude instances with specified security group name.
        type: str
        required: false
    available_floating:
        description:
            - Pass any string to only show instances which are able to handle floating address.
        type: str
        required: false
    include_baremetal:
        description:
            - Include baremetal instances.
        type: bool
        required: false
    include_all_bm_ips:
        description:
            - Include all ips in baremetal instances.
        type: bool
        required: false
    include_k8s:
        description:
            - Include k8s instances.
        type: bool
        default: true
        required: false
    include_ai:
        description:
            - Include AI instances.
        type: bool
        default: false
        required: false
    ip:
        description:
            - An IPv4 address to filter results by. Regular expression allowed.
        type: str
        required: false
    uuid:
        description:
            - Filter the server list result by the UUID of the server.
            - Allowed list of UUIDs part.
        type: str
        required: false
    metadata_kv:
        description:
            - Filter by metadata key-value pairs. Must be a valid JSON string.
        type: str
        required: false
    metadata_v:
        description:
            - Filter by metadata values. Must be a valid JSON string.
        type: str
        required: false
    with_ddos:
        description:
            - DDoS profile information will be included if parameter is provided.
        type: bool
        required: false
    order_by:
        description:
            - Ordering the server list result by name or created date fields of the server.
        type: str
        required: false
    type_ddos_profile:
        description:
            - Return baremetals either only with advanced or only basic DDoS protection.
        choices: [advanced, basic]
        type: str
        required: false
    profile_name:
        description:
            - Filter baremetals by profile name.
        type: str
        required: false
    only_with_fixed_external_ip:
        description:
            - Will be returned only BM instance with fixed external IPs.
        type: bool
        required: false
extends_documentation_fragment:
    - gcore.cloud.gcore.documentation
"""

EXAMPLES = """
- name: Gather gcore instances infos
  gcore.cloud.instance_info:
    api_key: "{{ api_key }}"

- name: Gather gcore specific instance info
  gcore.cloud.gcore_instance_info:
    instance_id: "{{ instance_id }}"
    api_key: "{{ api_key }}"
"""

RETURN = """
instance_info:
    description:
        - When I(instance_id) is passed, it is a dict of resource.
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
        instance_id:
            description: Region ID
            returned: always
            type: str
            sample: a7e7e8d6-0bf7-4ac9-8170-831b47ee2ba9
        flavor_id:
            description: Flavor ID
            returned: always
            type: str
            sample: g1s-shared-1-0.5
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
            returned: if available
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
            returned: if available
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
            returned: if available
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
from ansible_collections.gcore.cloud.plugins.module_utils.gcore import AnsibleGCore


def manage(module: AnsibleModule):
    api = AnsibleGCore(module)
    instance_id = module.params.pop("instance_id", None)
    if instance_id:
        result = api.instances.get_by_id(instance_id)
    else:
        result = api.instances.get_list(**module.params)
    module.exit_json(changed=False, data=result)


def main():
    module_spec = dict(
        instance_id=dict(type="str", required=False),
        name=dict(type="str", required=False),
        flavor=dict(type="str", required=False),
        flavor_prefix=dict(type="str", required=False),
        status=dict(type="str", choices=["ACTIVE", "ERROR", "SHUTOFF", "REBOOT", "PAUSED"], required=False),
        changes_since=dict(type="str", required=False),
        changes_before=dict(type="str", required=False),
        exclude_secgroup=dict(type="str", required=False),
        available_floating=dict(type="str", required=False),
        include_baremetal=dict(type="bool", required=False),
        include_all_bm_ips=dict(type="bool", required=False),
        include_k8s=dict(type="bool", default=True, required=False),
        include_ai=dict(type="bool", default=False, required=False),
        ip=dict(type="str", required=False),
        uuid=dict(type="str", required=False),
        metadata_kv=dict(type="str", required=False),
        metadata_v=dict(type="str", required=False),
        with_ddos=dict(type="bool", required=False),
        order_by=dict(type="str", required=False),
        type_ddos_profile=dict(type="str", choices=["advanced", "basic"], required=False),
        profile_name=dict(type="str", required=False),
        only_with_fixed_external_ip=dict(type="bool", required=False),
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
