# Ansible Collection for GCore Cloud

This collection provides a series of Ansible modules and plugins for interacting with the [GCore](https://gcore.com) Cloud.

## Installation

To install the collection hosted in Galaxy:

```bash
ansible-galaxy collection install gcore.cloud
```

To upgrade to the latest version of the collection:

```bash
ansible-galaxy collection install gcore.cloud --force
```

## License

GNU General Public License v3.0

See [COPYING](COPYING) to see the full text.

## Usage

### Playbooks

To use a module from the gcore collection, please reference the full namespace, collection name, and modules name that you want to use:

```yaml
---
- name: Using gcore collection
  hosts: localhost
  tasks:
    - gcore.cloud.instance:
        names: ["my_new_vm"]
        flavor: "g1-standard-1-2"
        volumes: [{
          'source': 'image',
          'size': 10,
          'type_name': 'standard',
          'boot_index': 0,
          'image_id': '9c440e4d-a157-4389-bb10-c53a72755356',
          'delete_on_termination': False
        }]
        interfaces: [{"type": "external"}]
        api_key: ...
        api_host: ...
        project_id: 111
        region_id: 76
        command: create
```

Or you can add the full namespace and collection name in the `collections` element:

```yaml
---
- name: Using gcore collection
  hosts: localhost
  collections:
    - gcore.cloud
  tasks:
    - instance:
        ...
```

## Contributing

There are many ways in which you can participate in the project, for example:

- Submit bugs and feature requests, and help us verify them as they are checked in
- Review source code changes
- Review the documentation and make pull requests for anything from typos to new content


## Testing Collection

Once installed, you can reference a collection content by its fully qualified collection name (FQCN).

To run integration tests, provide required config variables under `tests/integration/integration_config.yml`

| key              | value                 |
|------------------|-----------------------|
| API_KEY    | Yor api key           |
| API_HOST   | Your local api url    |
| PROJECT_ID | Your local project ID |
| REGION_ID  | Your region ID       |

and execute the command:

```
ansible-test integration volume --docker -v --diff --color
```
