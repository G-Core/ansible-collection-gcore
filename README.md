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

Example `local_playbook.yml` can be found in the `tests/integration` directory.
To run it, provide required config variables under `tests/integration/config.yml`

| key              | value                 |
|------------------|-----------------------|
| API_KEY    | Yor api key           |
| API_HOST   | Your local api url    |
| PROJECT_ID | Your local project ID |
| REGION_ID  | ED-10 region ID       |

and from the `tests/integration` dir execute the command:

```
ansible-playbook -i localhost, local_playbook.yml -vvvv
```
