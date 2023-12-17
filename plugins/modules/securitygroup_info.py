# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: securitygroup_info
author:
    - GCore (@GCore)
short_description: Gather infos about all GCore securitygroups.
description:
    - Gather infos about all GCore securitygroups.

options:
    securitygroup_id:
        description:
            - The ID of securitygroup you want to get.
            - The module will fail if the provided ID is invalid.
        type: str
        required: false
    metadata_kv:
        description:
            - Filter by metadata key-value pairs. Must be a valid JSON string.
        type: str
        required: false
    metadata_k:
        description:
            - Filter by metadata keys. Must be a valid JSON string.
        type: str
        required: false
    limit:
        description:
            - Limit the number of returned limit request entities.
        type: int
        required: false
    offset:
        description:
            - Offset value is used to exclude the first set of records from the result.
        type: int
        required: false
    
extends_documentation_fragment:
    - gcore.cloud.cloud.documentation
"""

EXAMPLES = """
- name: Gather gcore securitygroup infos
  gcore.cloud.securitygroup_info:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"

- name: Gather gcore specific securitygroup info
  gcore.cloud.securitygroup_info:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    securitygroup_id: "{{ securitygroup_id }}"
"""

RETURN = """
securitygroup_info:
    description:
        - When I(securitygroup_id) is passed, it is a dict of resource.
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
        id:
            description: Security group ID
            returned: always
            type: str
            sample: 3addc7a1-e926-46da-b5a2-eb4b2f935230
        name:
            description: Security group name
            returned: always
            type: str
            sample: default
        description:
            description: Security group description
            returned: always
            type: str
            sample: Default security group
        security_group_rules:
            description: Security group rules
            returned: always
            type: list
            elements: dict
            sample: [{
                'created_at': '2019-07-26T13:25:03+0000',
                'description': None,
                'direction': 'egress',
                'ethertype': 'IPv4',
                'id': '253c1ad7-8061-44b9-9f33-5616ad8ba5b6',
                'port_range_max': None,
                'port_range_min': None,
                'protocol': None,
                'remote_group_id': None,
                'remote_ip_prefix': None,
                'revision_number': 0,
                'security_group_id': '3addc7a1-e926-46da-b5a2-eb4b2f935230',
                'updated_at': '2019-07-26T13:25:03+0000'
            }]
        created_at:
            description: Datetime when the security group was created
            returned: always
            type: str
            sample: '2019-07-26T13:25:03+0000'
        updated_at:
            description: Datetime when the security group was last updated
            returned: always
            type: str
            sample: 2019-07-26T13:25:03+0000
        revision_number:
            description: The number of revisions
            returned: always
            type: int
            sample: 0
        metadata:
            description: Network metadata
            returned: always
            type: list
            elements: dict
            sample: [{'key': 'hosting', 'value': 'some value', 'read_only': false}]
        tags:
            description: Security group tags
            returned: always
            type: list
            elements: str
            sample: ['hosting']
"""

from traceback import format_exc

from ansible.module_utils.basic import AnsibleModule, to_native
from ansible_collections.gcore.cloud.plugins.module_utils.cloud import (
    AnsibleCloudClient,
)


def manage(module: AnsibleModule):
    api = AnsibleCloudClient(module)
    securitygroup_id = module.params.get("securitygroup_id")
    command = "get_by_id" if securitygroup_id else "get_list"
    result = api.securitygroups.execute_command(command=command)
    module.exit_json(changed=False, data=result)


def main():
    module_spec = dict(
        securitygroup_id=dict(type="str", required=False),
        metadata_k=dict(type="str", required=False),
        metadata_kv=dict(type="str", required=False),
        limit=dict(type="int", required=False),
        offset=dict(type="int", required=False),
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
