# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: securitygroup_rule
author:
    - GCore (@GCore)
short_description: Manages securitygroup rules.
description:
    - Create or delete rule from securitygroup.

options:
    command:
        description:
            - Operation to perform.
        choices: [create, delete]
        required: true
        type: str
    securitygroup_id:
        description:
            - The ID of securitygroup.
            - Required if I(command) is create.
        type: str
        required: false
    securitygroup_rule_id:
        description:
            - The ID of securitygroup rule.
            - Required if I(command) is delete.
        type: str
        required: false
    direction:
        description:
            - Direction type.
            - Used if I(command) is create.
        type: str
        choices: [egress, ingress]
        required: false
    ethertype:
        description:
            - Ether type.
            - Used if I(command) is create.
        type: str
        choices: [IPv4, IPv6]
        required: false
    description:
        description:
            - Rule description.
            - Used if I(command) is create.
        type: str
        required: false
    remote_group_id:
        description:
            - The remote group UUID to associate with this security group rule.
            - Used if I(command) is create.
        type: str
        required: false
    port_range_min:
        description:
            - The lowest port value for the rule to be applied to.
            - Used if I(command) is create.
        type: int
        required: false
    port_range_max:
        description:
            - The highest port value for the rule to be applied to.
            - Used if I(command) is create.
        type: int
        required: false
    remote_ip_prefix:
        description:
            - IP or Mask.
            - Used if I(command) is create.
        type: str
        required: false
    protocol:
        description:
            - IP or Mask.
            - Used if I(command) is create.
        type: str
        choices: [
            'any',
            'ah',
            'dccp',
            'egp',
            'esp',
            'gre',
            'icmp',
            'igmp',
            'ipip',
            'ospf',
            'pgm',
            'rsvp',
            'sctp',
            'tcp',
            'udp',
            'udplite',
            'vrrp',
            'ipv6-encap',
            'ipv6-frag',
            'ipv6-icmp',
            'ipv6-nonxt',
            'ipv6-opts',
            'ipv6-route',
            'ipencap'
        ]
        required: false
    id:
        description:
            - Rule ID.
            - Used if I(command) is create.
        type: str
        required: false
    revision_number:
        description:
            - The number of revisions.
            - Used if I(command) is create.
        type: int
        required: false
extends_documentation_fragment:
    - gcore.cloud.cloud.documentation
"""

EXAMPLES = """
- name: Add new rule to securitygroup
  gcore.cloud.securitygroup_rule:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: create
    securitygroup_id: "{{ securitygroup_id }}"
    direction: "ingress"
    ethertype: "IPv6"

- name: Delete rule from securitygroup
  gcore.cloud.securitygroup_rule:
    api_key: "{{ api_key }}"
    region_id: "{{ region_id }}"
    project_id: "{{ project_id }}"
    command: delete
    securitygroup_rule_id: "{{ securitygroup_rule_id }}"
"""

RETURN = """
securitygroup:
    description:
        - Response depends of I(command).
        - Resource dictionary.
    returned: always
    type: complex
    contains:
        id:
            description: Rule ID
            returned: always
            type: str
            sample: fc84ed5b-b6f9-4e0c-95af-d0991e218bf7
        security_group_id:
            description: Parent security group of this rule
            returned: always
            type: str
            sample: 3addc7a1-e926-46da-b5a2-eb4b2f935230
        direction:
            description: Direction type
            returned: always
            type: str
            sample: ingress
        created_at:
            description: Datetime when the rule was created
            returned: always
            type: str
            sample: 2019-07-26T13:25:03+0000
        updated_at:
            description: Datetime when the rule was last updated
            returned: always
            type: str
            sample: 2019-07-26T13:25:03+0000
        revision_number:
            description: The number of revisions
            returned: always
            type: int
            sample: 0
        ethertype:
            description: Ether type
            returned: always
            type: str
            sample: IPv4
        description:
            description: Rule description
            returned: always
            type: str
            sample: Test
        remote_group_id:
            description: The remote group UUID to associate with this security group rule
            returned: always
            type: str
            sample: af8e207c-df03-4e88-92d2-605459040722
        port_range_min:
            description: The lowest port value for the rule to be applied to
            returned: always
            type: int
            sample: 1
        port_range_max:
            description: The highest port value for the rule to be applied to
            returned: always
            type: int
            sample: 100
        remote_ip_prefix:
            description: IP or mask
            returned: always
            type: str
            sample: 94.14.91.255
        protocol:
            description: Protocol
            returned: always
            type: str
            sample: any
"""

from traceback import format_exc

from ansible.module_utils.basic import AnsibleModule, to_native

from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.securitygroup_rule import (
    DirectionType,
    Ethertype,
    SecurityGroupProtocol,
)
from ansible_collections.gcore.cloud.plugins.module_utils.clients.securitygroup_rule import (
    SecurityGroupRuleManageAction,
)
from ansible_collections.gcore.cloud.plugins.module_utils.cloud import (
    AnsibleCloudClient,
)


def manage(module: AnsibleModule):
    api = AnsibleCloudClient(module)
    command = module.params.pop("command")
    result = api.securitygroup_rules.execute_command(command=command)
    module.exit_json(**result)


def main():
    module_spec = dict(
        command=dict(type="str", choices=list(SecurityGroupRuleManageAction), required=True),
        securitygroup_id=dict(type="str", required=False),
        securitygroup_rule_id=dict(type="str", required=False),
        direction=dict(type="str", choices=list(DirectionType), required=False),
        ethertype=dict(type="str", choices=list(Ethertype), required=False),
        description=dict(type="str", required=False),
        remote_group_id=dict(type="str", required=False),
        port_range_min=dict(type="int", required=False),
        port_range_max=dict(type="int", required=False),
        remote_ip_prefix=dict(type="str", required=False),
        protocol=dict(type="str", choices=list(SecurityGroupProtocol), required=False),
        id=dict(type="str", required=False),
        revision_number=dict(type="int", required=False),
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
