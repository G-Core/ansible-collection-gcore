# GCore Ansible Community Collection
## Installation and Usage
- ansible-core >= 2.15
- python >= 3.10


## Building Collection
Clone repository
```
mkdir -p /home/$USER/ansible_collections/gcore
cd /home/$USER/ansible_collections/gcore
git clone ssh://git@gitlab-ed7.cloud.gc.onl:2200/cloudapi/ansible-provider.git cloud
```

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
