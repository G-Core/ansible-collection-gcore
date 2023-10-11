# GCore Ansible Community Collection
## Installation and Usage
- ansible-core >= 2.15
- python >= 3.9

```bash
mkdir -p /home/<user>/ansible_collections/community
cd /home/<user>/ansible_collections/community
git clone ssh://git@gitlab-ed7.cloud.gc.onl:2200/cloudapi/ansible-provider.git gcore
```

## Tests
Fill tests/integration_config.yml

| key                | value                 |
|--------------------|-----------------------|
| GCORE_API_TOKEN    | Yor api token         |
| GCORE_API_ENDPOINT | Your local api url    |
| GCORE_PROJECT_ID   | Your local project ID |
| GCORE_REGION_ID    | ED-10 region ID       |

```bash
# sanity
poetry run ansible-test sanity --docker
# unit tests
poetry run ansible-test units --docker
# integration tests
poetry run ansible-test integration --docker
```
