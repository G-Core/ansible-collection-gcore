from dataclasses import MISSING, asdict, dataclass, fields


@dataclass
class BaseResource:
    @classmethod
    def init_as_dict(cls, data: dict, include_empty: bool = False):
        _class = cls.from_dict(data)
        return cls.to_dict(_class, include_empty=include_empty)

    @classmethod
    def from_dict(cls, data: dict) -> "BaseResource":
        params = {f.name: f.default for f in fields(cls)}
        filtered_data = {k: v for k, v in data.items() if k in params and v is not None}
        for field_name in params:
            if params[field_name] != MISSING:
                filtered_data[field_name] = params[field_name]
        return cls(**filtered_data)

    @classmethod
    def get_required(cls):
        return [f.name for f in fields(cls) if f.default == MISSING and f.default_factory == MISSING]

    def to_dict(self, include_empty: bool = False) -> dict:
        if include_empty:
            return asdict(self)
        return {k: v for k, v in asdict(self).items() if v is not None}
