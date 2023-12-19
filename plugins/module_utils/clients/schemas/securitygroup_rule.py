from dataclasses import dataclass
from enum import Enum
from typing import Optional

from ansible_collections.gcore.cloud.plugins.module_utils.clients.schemas.base import (
    BaseSchema,
)


class Ethertype(str, Enum):
    IPv4 = "IPv4"
    IPv6 = "IPv6"


class SecurityGroupProtocol(str, Enum):
    any = "any"
    ah = "ah"
    dccp = "dccp"
    egp = "egp"
    esp = "esp"
    gre = "gre"
    icmp = "icmp"
    igmp = "igmp"
    ipip = "ipip"
    ospf = "ospf"
    pgm = "pgm"
    rsvp = "rsvp"
    sctp = "sctp"
    tcp = "tcp"
    udp = "udp"
    udplite = "udplite"
    vrrp = "vrrp"
    ipv6_encap = "ipv6-encap"
    ipv6_frag = "ipv6-frag"
    ipv6_icmp = "ipv6-icmp"
    ipv6_nonxt = "ipv6-nonxt"
    ipv6_opts = "ipv6-opts"
    ipv6_route = "ipv6-route"
    ipencap = "ipencap"


class DirectionType(str, Enum):
    egress = "egress"
    ingress = "ingress"


@dataclass
class CreateSecurityGroupRule(BaseSchema):
    direction: DirectionType
    ethertype: Optional[Ethertype] = None
    description: Optional[str] = None
    remote_group_id: Optional[str] = None
    port_range_min: Optional[int] = None
    port_range_max: Optional[int] = None
    remote_ip_prefix: Optional[str] = None
    protocol: Optional[SecurityGroupProtocol] = None
    id: Optional[str] = None
    securitygroup_id: Optional[str] = None
    revision_number: Optional[int] = None


@dataclass
class SecurityGroupRuleId(BaseSchema):
    securitygroup_rule_id: str
