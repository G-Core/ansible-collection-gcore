# GCore Ansible Community Collection
## Installation and Usage
- ansible-core >= 2.15
- python >= 3.9


## Building Collection 

to building collection run the following command in the project directory:

```
ansible-galaxy collection build
```

install the built collection locally for testing:

```
ansible-galaxy collection install <path_to_tarball_from_previous_command>
```


## Testing Collection 

Once installed, you can reference a collection content by its fully qualified collection name (FQCN).

Example `local_playbook.yml` can be found in the `tests/integration` directory.
To run it, provide required config variables under `tests/integration/config.yml`

| key              | value                 |
|------------------|-----------------------|
| GCORE_API_TOKEN  | Yor api token         |
| GCORE_API_HOST   | Your local api url    |
| GCORE_PROJECT_ID | Your local project ID |
| GCORE_REGION_ID  | ED-10 region ID       |

and from the `tests/integration` dir execute the command:

```
ansible-playbook -i localhost, local_playbook.yml -vvvv
```
