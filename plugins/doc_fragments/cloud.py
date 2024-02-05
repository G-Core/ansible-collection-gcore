class ModuleDocFragment:
    DOCUMENTATION = r"""
options:
    api_host:
        description:
            - GCore API base host
            - Can be passed as I(CLOUD_API_HOST) environment variable.
        type: str
        default: https://api.gcore.com/cloud
    api_key:
        description:
            - GCore API auth key
            - Can be passed as I(CLOUD_API_KEY) environment variable.
        type: str
    api_timeout:
        description:
            - Timeout in seconds to polling GCore API
        type: int
        default: 30
    project_id:
        description:
            - GCore API project ID
            - Required if I(project_name) is not passed
            - Can be passed as I(CLOUD_PROJECT_ID) environment variable.
        type: int
    project_name:
        description:
            - GCore API project name
            - Required if I(project_id) is not passed
            - Can be passed as I(CLOUD_PROJECT_NAME) environment variable.
        type: str
    region_id:
        description:
            - GCore API region ID
            - Required if I(region_name) is not passed
            - Can be passed as I(CLOUD_REGION_ID) environment variable.
        type: int
    region_name:
        description:
            - GCore API region name
            - Required if I(region_id) is not passed
            - Can be passed as I(CLOUD_REGION_NAME) environment variable.
        type: str
seealso:
- name: Documentation for GCore Cloud API
  description: Complete public API documentation.
  link: https://api.gcore.com/docs/cloud
"""
