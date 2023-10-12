class ModuleDocFragment:
    DOCUMENTATION = r"""
options:
    api_endpoint:
        description:
            - GCore API base endpoint
        type: str
        default: https://api.gcore.com/cloud
    api_token:
        description:
            - GCore API auth token
        type: str
        required: true
    api_timeout:
        description:
            - Timeout in seconds to polling GCore API
        type: int
        default: 30
    project_id:
        description:
            - GCore API project ID
        type: int
        required: true
    region_id:
        description:
            - GCore API region ID
        type: int
        required: true
"""
