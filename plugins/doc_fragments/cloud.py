class ModuleDocFragment:
    DOCUMENTATION = r"""
options:
    api_host:
        description:
            - GCore API base host
        type: str
        default: https://api.gcore.com/cloud
        env:
            - name: CLOUD_API_HOST
    api_key:
        description:
            - GCore API auth key
        type: str
        env:
            - name: CLOUD_API_KEY
    api_timeout:
        description:
            - Timeout in seconds to polling GCore API
        type: int
        default: 30
    project_id:
        description:
            - GCore API project ID
            - Required if I(project_name) is not passed
        type: int
        env:
            - name: CLOUD_PROJECT_ID
    project_name:
        description:
            - GCore API project name
            - Required if I(project_id) is not passed
        type: str
        env:
            - name: CLOUD_PROJECT_NAME
    region_id:
        description:
            - GCore API region ID
            - Required if I(region_name) is not passed
        type: int
        env:
            - name: CLOUD_REGION_ID
    region_name:
        description:
            - GCore API region name
            - Required if I(region_id) is not passed
        type: str
        env:
            - name: CLOUD_REGION_NAME
seealso:
- name: Documentation for GCore Cloud API
  description: Complete public API documentation.
  link: https://api.gcore.com/docs/cloud
"""
