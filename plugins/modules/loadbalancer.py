# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: loadbalancer
author:
    - GCore (@GCore)
short_description: Manages loadblancers
description:
    - Create, update or delete loadbalancer

options:
    command:
        description:
            - Operation to perform.
        choices: [create, update, delete]
        required: true
        type: str
    loadbalancer_id:
        description:
            - Loadbalancer Id.
            - Required if I(command) is update or delete
        type: str
        required: false
    name:
        description:
            - Load balancer name.
            - Used if I(command) is create or update
            - Required if I(command) is create and name_template is not passed
        type: str
        required: false
    name_template:
        description:
            - Load balancer name which will be changed by template.
            - Required if I(command) is create and name is not passed
        type: str
        required: false
    flavor:
        description:
            - Load balancer flavor name.
            - Used if I(command) is create
        type: str
        required: false
    listeners:
        description:
            - Load balancer listeners.
            - Used if I(command) is create
        type: list
        elements: dict
        required: false
    vip_network_id:
        description:
            - Network ID for load balancer. If not specified, default external network will be used.
            - vip_subnet_id is required in addition to vip_network_id. Mutually exclusive with vip_port_id.
            - Used if I(command) is create.
        type: str
        required: false
    vip_subnet_id:
        description:
            - Subnet ID for load balancer.
            - If not specified, any subnet from vip_network_id will be selected.
            - Ignored when vip_network_id is not specified.
            - Used if I(command) is create
        type: str
        required: false
    vip_port_id:
        description:
            - Existing Reserved Fixed IP port ID for load balancer.
            - Mutually exclusive with vip_network_id.
            - Used if I(command) is create
        type: str
        required: false
    floating_ip:
        description:
            - Floating IP configuration for assignment.
            - Used if I(command) is create
        type: dict
        required: false
    metadata:
        description:
            - Loadbalancer metadata.
            - Used if I(command) is create
        type: dict
        required: false
    tag:
        description:
            - A list of inner tags (k8s, k8s_ingress) assigned to the load balancer.
            - Used if I(command) is create
        type: list
        elements: str
        required: false
    logging:
        description:
            - Logging configuration.
            - Used if I(command) is create
        type: dict
        required: false
extends_documentation_fragment:
    - gcore.cloud.cloud.documentation
"""

EXAMPLES = """
- name: Create new loadbalancer
  gcore.cloud.loadbalancer:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: create
    name: 'my-loadbalancer'

- name: Update loadbalancer
  gcore.cloud.loadbalancer:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    comamnd: update
    loadbalancer_id: "{{ loadbalancer_id }}"
    name: 'new-name'

- name: Delete loadbalancer
  gcore.cloud.loadbalancer:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    comamnd: delete
    loadbalancer_id: "{{ loadbalancer_id }}"
"""

RETURN = """
loadbalancer:
    description:
        - Response depends of I(command).
        - If I(command) is create or update then response will be a dict of resource.
        - If I(command) is delete then response will be a dict of resource ID.
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
            description: Loadbalancer ID
            returned: always
            type: str
            sample: e8ab1be4-1521-4266-be69-28dad4148a30
        name:
            description: Loadbalancer name
            returned: always
            type: str
            sample: lbaas_test_lb
        flavor:
            description: Load balancer flavor
            returned: always
            type: dict
            sample: {
                'flavor_id': '1d276f53-2834-4855-9859-aa922f073055',
                'flavor_name': 'lb1-1-2',
                'ram': 2048,
                'vcpus': 1
            }
        vip_address:
            description: Load balancer IP address
            returned: always
            type: str
            sample: 5.5.5.5
        vip_port_id:
            description: Port ID
            returned: always
            type: str
            sample: 5eee7e6f-55d6-4044-b205-4988247d2540
        vrrp_ips:
            description: List of VRRP IP addresses
            returned: always
            type: list
            elements: str
            sample: ['127.0.0.1']
        floating_ips:
            description: List of assigned floating IPs
            returned: always
            type: list
            elements: dict
            sample: {
                'created_at': '2019-06-13T13:58:12+0000',
                'creator_task_id': 'd1e1500b-e2be-40aa-9a4b-cc493fa1af30',
                'fixed_ip_address': None,
                'floating_ip_address': '172.24.4.34',
                'id': 'c64e5db1-5f1f-43ec-a8d9-5090df85b82d',
                'port_id': 'ee2402d0-f0cd-4503-9b75-69be1d11c5f1',
                'project_id': 1,
                'region': 'Luxembourg 1',
                'region_id': 1,
                'router_id': '11005a33-c5ac-4c96-ab6f-8f2827cc7da6',
                'status': 'DOWN',
                'updated_at': '2019-06-13T13:58:12+0000',
                'dns_domain': 'gcore.com',
                'dns_name': 'string',
                'subnet_id': 'b1a3dd16-04c1-4f13-b8f9-f6569f74bb15',
                'task_id': 'a4eb4b29-048e-42f6-a5e1-2c18bc001c45',
                'metadata': [
                {
                    'key': 'hosting',
                    'value': 'some value',
                    'read_only': False,
                }
            ]
        }
        operating_status:
            description: Load balancer operating status
            returned: always
            type: str
            sample: ONLINE
        provisioning_status:
            description: Load balancer lifecycle status
            returned: always
            type: str
            sample: ACTIVE
        listeners:
            description: Load balancer listeners
            returned: always
            type: list
            elements: dict
            sample: [{
                'id': '0b831470-0160-4601-bfd6-04a0df623eae',
                'name': 'listener',
                'description': 'test',
                'protocol': 'HTTP',
                'protocol_port': 80,
                'operating_status': 'ONLINE',
                'provisioning_status': 'ACTIVE',
                'allowed_cidrs': []
            }]
        created_at:
            description: Loadbalancer create datetime
            returned: always
            type: str
            sample: 2020-01-24T13:57:12+0000
        updated_at:
            description: Loadbalancer update datetime
            returned: if available
            type: str
            sample: 2020-01-24T13:57:35+0000
        task_id:
            description: Active task. If None, action has been performed immediately in the request itself
            returned: if available
            type: str
            sample: 4966d73a-451a-4768-9fb7-65661f246fad
        stats:
            description: Statistic of the load balancer. It is available only in get functions by a flag
            returned: if available
            type: dict
            sample: {
                'active_connections': 0,
                'bytes_in': 34942398609,
                'bytes_out': 304777113641,
                'request_errors': 4,
                'total_connections': 21095970
            }
        metadata:
            description: Create one or more metadata items for a loadbalancers
            returned: if available
            type: list
            elements: dict
            sample: [{'key': 'type', 'value': 'standart', 'read_only': false}]
        logging:
            description: Logging configuration
            returned: if available
            type: dict
            sample: {
                'enabled': false,
                'topic_name': 'some_topic_name',
                'destination_region_id': 1,
                'retention_policy': {'period': 45}
            }
"""

from traceback import format_exc

from ansible.module_utils.basic import AnsibleModule, to_native
from ansible_collections.gcore.cloud.plugins.module_utils.clients.loadbalancer import (
    LoadbalancerManageAction,
)
from ansible_collections.gcore.cloud.plugins.module_utils.cloud import (
    AnsibleCloudClient,
)


def manage(module: AnsibleModule):
    api = AnsibleCloudClient(module)
    command = module.params.pop("command")
    result = api.loadbalancers.execute_command(command=command)
    module.exit_json(changed=False, data=result)


def main():
    module_spec = dict(
        command=dict(type="str", choices=list(LoadbalancerManageAction), required=True),
        loadbalancer_id=dict(type="str", required=False),
        name=dict(type="str", required=False),
        name_template=dict(type="str", required=False),
        flavor=dict(type="str", required=False),
        listeners=dict(type="list", elements="dict", required=False),
        vip_network_id=dict(type="str", required=False),
        vip_subnet_id=dict(type="str", required=False),
        vip_port_id=dict(type="str", required=False),
        floating_ip=dict(type="dict", required=False),
        metadata=dict(type="dict", required=False),
        tag=dict(type="list", elements="str", required=False),
        logging=dict(type="dict", required=False),
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
