from typing import Dict

import addict
import yaml

from .generators import generate_config_path

def load_yaml_file(file) -> Dict:
    """ Load yaml file and return as dict. """
    with open(file) as yaml_file:
        return addict.Dict(
            yaml.safe_load(
                yaml_file
            )
        )

def load_yaml_config() -> Dict:
    """ Load config file. """
    return load_yaml_file(
        generate_config_path()
    )