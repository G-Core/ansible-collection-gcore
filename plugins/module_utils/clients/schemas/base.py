from dataclasses import MISSING, dataclass, fields
from typing import Optional

from ansible_collections.gcore.cloud.plugins.module_utils.exceptions import (
    ValidationError,
)


@dataclass
class BaseSchema:
    @classmethod
    def init_as_dict(cls, allow_none: Optional[list] = None, **kwargs):
        allow_none = allow_none or []
        schema_fields = {f.name: f.default for f in fields(cls)}
        alias_map = {f.name: f.metadata.get("alias", f.name) for f in fields(cls)}

        filtered_data = {}
        for k, v in kwargs.items():
            field_name = alias_map.get(k)
            if field_name and (v is not None or field_name in allow_none):
                filtered_data[field_name] = v

        missing_fields = [
            field for field, value in schema_fields.items() if value is MISSING and not filtered_data.get(field)
        ]
        if missing_fields:
            raise ValidationError(f"Expected required params: {', '.join(missing_fields)}")

        return filtered_data

    @classmethod
    def get_required(cls):
        return [f.name for f in fields(cls) if f.default is MISSING]
