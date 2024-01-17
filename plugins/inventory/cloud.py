# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


DOCUMENTATION = r"""
    name: cloud
    author:
      - GCore (@GCore)
    short_description: Ansible dynamic inventory plugin for the GCore Cloud.
    requirements:
        - python >= 3.10
    description:
        - Reads inventories from the GCore public API.
        - Uses a YAML configuration file that ends with gcore.(yml|yaml).
    extends_documentation_fragment:
        - constructed
        - inventory_cache
    options:
        plugin:
            description:
            - The name of the GCore Inventory Plugin.
            required: true
            choices: ['gcore.cloud.cloud']
        api_key:
            description: GCore API auth key
            required: true
        project_id:
            description:
                - GCore API project ID
                - Required if I(project_name) is not passed
            type: int
            required: false
        project_name:
            description:
                - GCore API project name
                - Required if I(project_id) is not passed
            type: str
            required: false
        region_id:
            description:
                - GCore API region ID
                - Required if I(region_name) is not passed
            type: int
            required: false
        region_name:
            description:
                - GCore API region name
                - Required if I(region_id) is not passed
            type: str
            required: false
        os_type:
          description: Populate inventory with instances with specific os distro type.
          default: ""
          type: str
          required: false
        status:
          description: Populate inventory with instances with this status.
          default: []
          type: list
          elements: str
          required: false
        group:
            description: Name for server grouping.
            default: gcore
            type: str
            required: false
        inventory_hostname:
            description:
                - How to populate inventory on instance.
            type: str
            choices:
                - name
                - uuid
            default: "uuid"
"""

EXAMPLES = """
# gcore.yml name ending file in YAML format
# Example command line: ansible-inventory --list -i myinventory-gcore.yml

plugin: gcore.cloud.cloud
api_key: "{{ api_key }}"
project_name: "{{ project_name }}"
region_name: "{{ region_name }}"

# Get only active servers
plugin: gcore.cloud.cloud
api_key: "{{ api_key }}"
project_name: "{{ project_name }}"
region_name: "{{ region_name }}"
status:
    - ACTIVE

# Get only windows servers
plugin: gcore.cloud.cloud
api_key: "{{ api_key }}"
project_name: "{{ project_name }}"
region_name: "{{ region_name }}"
os_type: windows
"""


import json
import os

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.inventory.manager import InventoryData
from ansible.module_utils.urls import Request, open_url
from ansible.plugins.inventory import BaseInventoryPlugin, Cacheable, Constructable

inventory_hostname_map = {
    "uuid": "instance_id",
    "name": "instance_name",
}


class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):
    NAME = "gcore.cloud.gcore"

    inventory: InventoryData

    def verify_file(self, path):
        return super().verify_file(path) and path.endswith(("gcore.yaml", "gcore.yml"))

    @property
    def api_key(self):
        api_key = self.templar.template(self.get_option("api_key"), fail_on_undefined=False) or os.getenv("api_key")
        if api_key is None:
            raise AnsibleError("Please specify an api key, via the option api_key, via environment variable api_key.")
        return api_key

    @property
    def headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"APIKey {self.api_key}",
        }

    @property
    def api_host(self):
        return os.environ.get("api_host", "https://api.gcore.com/cloud")

    @property
    def project_id(self):
        project_id = self.templar.template(self.get_option("project_id"), fail_on_undefined=False)
        project_name = self.templar.template(self.get_option("project_name"), fail_on_undefined=False)
        if project_id is None and project_name is None:
            raise AnsibleError(
                "Please specify a project_id or project_name, via the option project_id or project_name."
            )
        if project_id:
            return project_id
        response = open_url(url=f"{self.api_host}/v1/projects", headers=self.headers)
        response = json.loads(response.read())
        for project in response["results"]:
            if project["name"] == project_name:
                return project["id"]
        raise AnsibleError(f"Cannot find project with name: {project_name}")

    @property
    def region_id(self):
        region_id = self.templar.template(self.get_option("region_id"), fail_on_undefined=False)
        region_name = self.templar.template(self.get_option("region_name"), fail_on_undefined=False)
        if region_id is None and region_name is None:
            raise AnsibleError("Please specify a region_id or region_name, via the option region_id or region_name.")
        if region_id:
            return region_id
        response = open_url(url=f"{self.api_host}/v1/regions", headers=self.headers)
        response = json.loads(response.read())
        for region in response["results"]:
            if region["display_name"] == region_name:
                return region["id"]
        raise AnsibleError(f"Cannot find region with name: {region_name}")

    def _request(self, path: str):
        project_id = self.project_id
        region_id = self.region_id
        url = f"{self.api_host}/{path}/{project_id}/{region_id}"
        try:
            self.display.vvv(f"Sending request to {url}")
            request = Request(headers=self.headers)
            return json.load(request.get(url))["results"]
        except ValueError as exc:
            raise AnsibleParserError("Cannot parse the JSON from response.") from exc

    def _filter_servers(self, servers):
        status = self.get_option("status")
        if status:
            servers = [server for server in servers if server["status"] in status]

        os_type = self.get_option("os_type")
        if os_type:
            servers = [server for server in servers if server["metadata"]["os_type"] == os_type]
        return servers

    def _get_servers_list(self):
        return self._request("v1/instances")

    def parse(self, inventory, loader, path, cache=True):
        super().parse(inventory, loader, path)

        self._read_config_data(path)

        inventory_hostname = self.get_option("inventory_hostname")
        if inventory_hostname not in (
            "uuid",
            "name",
        ):
            raise AnsibleError(f"Invalid value for option inventory_hostname: {inventory_hostname}")

        servers = self._get_servers_list()
        filtered_servers = self._filter_servers(servers)
        self.inventory.add_group(group=self.get_option("group"))
        strict = self.get_option("strict")
        inventory_key = inventory_hostname_map[inventory_hostname]

        for server in filtered_servers:
            host_name = server[inventory_key]
            self.inventory.add_host(host_name, group=self.get_option("group"))

            addresses = [addr["addr"] for addresses in server["addresses"].values() for addr in addresses]

            variables = self.inventory.get_host(host_name).get_vars()

            if len(addresses) > 0:
                self.inventory.set_variable(
                    host_name,
                    "ansible_host",
                    addresses[0],
                )

            self._set_composite_vars(
                self.get_option("compose"),
                variables,
                host_name,
                strict,
            )
            self._add_host_to_composed_groups(
                self.get_option("groups"),
                variables,
                host_name,
                strict,
            )
