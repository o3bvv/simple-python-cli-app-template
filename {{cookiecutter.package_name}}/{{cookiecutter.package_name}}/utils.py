import collections

from typing import Dict


def update_nested_dict(target: Dict, overrides: Dict) -> Dict:
    for key, value in overrides.items():
        value = (
            update_nested_dict(target.get(key, {}), value)
            if isinstance(value, collections.Mapping)
            else overrides[key]
        )
        target[key] = value

    return target
