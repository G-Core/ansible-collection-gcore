# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: instance_quota_info
author:
    - GCore (@GCore)
short_description: Check quota for instance creation.
description:
    - Check quota for instance creation.

options:
    names:
        description:
            - List of instance names.
            - Optional. Used if I(name_templates) is not passed.
        type: list
        elements: str
        required: false
    name_templates:
        description:
            - List of instance name templates.
            - Optional. Used if I(names) is not passed.
        type: list
        elements: str
        required: false
    interfaces:
        description:
            - Subnet IPs and floating IPs.
        type: list
        elements: dict
        required: true
    flavor:
        description:
            - Flavor name.
        type: str
        required: true
    volumes:
        description:
            - Volumes configuration.
        type: list
        elements: dict
        required: true
extends_documentation_fragment:
    - gcore.cloud.cloud.documentation
"""

EXAMPLES = """
- name: Check quota before create instance
  gcore.cloud.instance_quota_info:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    flavor: g1-standard-1-2
    names: ['inst1', 'inst2']
    volumes: [
        {'size': 10, 'source': 'image', 'type_name': 'ssd_hiiops'},
        {'size': 5, 'source': 'new-volume', 'type_name': 'standard'},
        {'snapshot_id': '7cca40d7-a843-4e9f-ae08-62b9a394b1ab', 'source': 'snapshot'},
    ]
    interfaces: [
        {
            'network_id': '783b36b4-3ef4-48ac-879d-5b3ea53180d8',
            'subnet_id': '382a83e5-1b38-49f9-bd83-730353b29ed4',
            'type': 'subnet',
        },
        {'type': 'external'}
    ]
"""

RETURN = """
instance_info:
    description:
        - If the quota is not exceeded, then the response will be an empty dictionary.
        - Dictionary of quotas.
    returned: if available
    type: dict
    sample: {
        'baremetal_basic_count_requested': 1,
        'baremetal_gpu_count_requested': 1,
        'baremetal_hf_count_requested': 1,
        'baremetal_infrastructure_count_requested': 1,
        'baremetal_network_count_requested': 1,
        'baremetal_storage_count_requested': 1,
        'cluster_count_requested': 1,
        'cpu_count_requested': 1,
        'dbaas_postgres_cluster_count_requested': 1,
        'external_ip_count_requested': 1,
        'faas_cpu_count_requested': 1,
        'faas_function_count_requested': 1,
        'faas_namespace_count_requested': 1,
        'faas_ram_size_requested': 1,
        'firewall_count_requested': 1,
        'floating_count_requested': 1,
        'gpu_count_requested': 1,
        'image_count_requested': 1,
        'image_size_requested': 1,
        'ipu_count_requested': 1,
        'laas_topic_count_requested': 1,
        'loadbalancer_count_requested': 1,
        'network_count_requested': 1,
        'ram_requested': 1,
        'router_count_requested': 1,
        'secret_count_requested': 1,
        'servergroup_count_requested': 1,
        'sfs_count_requested': 1,
        'sfs_size_requested': 1,
        'shared_vm_count_requested': 1,
        'snapshot_schedule_count_requested': 1,
        'subnet_count_requested': 1,
        'vm_count_requested': 1,
        'volume_count_requested': 1,
        'volume_size_requested': 1,
        'volume_snapshots_count_requested': 1,
        'volume_snapshots_size_requested': 1,
        'baremetal_basic_count_limit': 0,
        'baremetal_basic_count_usage': 0,
        'baremetal_gpu_count_limit': 0,
        'baremetal_gpu_count_usage': 0,
        'baremetal_hf_count_limit': 0,
        'baremetal_hf_count_usage': 0,
        'baremetal_infrastructure_count_limit': 0,
        'baremetal_infrastructure_count_usage': 0,
        'baremetal_network_count_limit': 0,
        'baremetal_network_count_usage': 0,
        'baremetal_storage_count_limit': 0,
        'baremetal_storage_count_usage': 0,
        'cluster_count_limit': 0,
        'cluster_count_usage': 0,
        'cpu_count_limit': 0,
        'cpu_count_usage': 0,
        'dbaas_postgres_cluster_count_limit': 0,
        'dbaas_postgres_cluster_count_usage': 0,
        'external_ip_count_limit': 0,
        'external_ip_count_usage': 0,
        'faas_cpu_count_limit': 0,
        'faas_cpu_count_usage': 0,
        'faas_function_count_limit': 0,
        'faas_function_count_usage': 0,
        'faas_namespace_count_limit': 0,
        'faas_namespace_count_usage': 0,
        'faas_ram_size_limit': 0,
        'faas_ram_size_usage': 0,
        'firewall_count_limit': 0,
        'firewall_count_usage': 0,
        'floating_count_limit': 0,
        'floating_count_usage': 0,
        'gpu_count_limit': 0,
        'gpu_count_usage': 0,
        'image_count_limit': 0,
        'image_count_usage': 0,
        'image_size_limit': 0,
        'image_size_usage': 0,
        'ipu_count_limit': 0,
        'ipu_count_usage': 0,
        'laas_topic_count_limit': 0,
        'laas_topic_count_usage': 0,
        'loadbalancer_count_limit': 0,
        'loadbalancer_count_usage': 0,
        'network_count_limit': 0,
        'network_count_usage': 0,
        'ram_limit': 0,
        'ram_usage': 0,
        'router_count_limit': 0,
        'router_count_usage': 0,
        'secret_count_limit': 0,
        'secret_count_usage': 0,
        'servergroup_count_limit': 0,
        'servergroup_count_usage': 0,
        'sfs_count_limit': 0,
        'sfs_count_usage': 0,
        'sfs_size_limit': 0,
        'sfs_size_usage': 0,
        'shared_vm_count_limit': 0,
        'shared_vm_count_usage': 0,
        'snapshot_schedule_count_limit': 0,
        'snapshot_schedule_count_usage': 0,
        'subnet_count_limit': 0,
        'subnet_count_usage': 0,
        'vm_count_limit': 0,
        'vm_count_usage': 0,
        'volume_count_limit': 0,
        'volume_count_usage': 0,
        'volume_size_limit': 0,
        'volume_size_usage': 0,
        'volume_snapshots_count_limit': 0,
        'volume_snapshots_count_usage': 0,
        'volume_snapshots_size_limit': 0,
        'volume_snapshots_size_usage': 0
    }
"""

from traceback import format_exc

from ansible.module_utils.basic import AnsibleModule, to_native
from ansible_collections.gcore.cloud.plugins.module_utils.cloud import (
    AnsibleCloudClient,
)


def manage(module: AnsibleModule):
    api = AnsibleCloudClient(module)
    result = api.instances.execute_command(command="get_quota")
    module.exit_json(**result)


def main():
    module_spec = dict(
        names=dict(type="list", elements="str", required=False),
        name_templates=dict(type="list", elements="str", required=False),
        interfaces=dict(type="list", elements="dict", required=True),
        flavor=dict(type="str", required=True),
        volumes=dict(type="list", elements="dict", required=True),
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
