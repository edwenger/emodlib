import os
from typing import Any, Dict, TypeVar

import yaml

from .._emodlib_py.malaria import Infection, IntrahostComponent, Susceptibility


def params_from_default_file():
    with open(
        os.path.join(
            os.path.realpath(os.path.dirname(__file__)),
            "config.yml",
        )
    ) as cfg:
        params = yaml.load(cfg, Loader=yaml.FullLoader)

    return params


KeyType = TypeVar("KeyType")


def deep_update(
    mapping: Dict[KeyType, Any], *updating_mappings: Dict[KeyType, Any]
) -> Dict[KeyType, Any]:
    updated_mapping = mapping.copy()
    for updating_mapping in updating_mappings:
        for k, v in updating_mapping.items():
            if (
                k in updated_mapping
                and isinstance(updated_mapping[k], dict)
                and isinstance(v, dict)
            ):
                updated_mapping[k] = deep_update(updated_mapping[k], v)
            else:
                updated_mapping[k] = v
    return updated_mapping


def configure(params={}):
    cfg = deep_update(IntrahostComponent.params, params)
    IntrahostComponent.params = cfg
    IntrahostComponent._configure_from_params(cfg)


IntrahostComponent.params = params_from_default_file()
IntrahostComponent._configure_from_params(IntrahostComponent.params)

IntrahostComponent.configure = configure


__all__ = ["IntrahostComponent", "Susceptibility", "Infection"]
