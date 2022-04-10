import logging
import logging.config
import os
from typing import Dict

import addict
import yaml


def load_yaml_file(file) -> Dict:
    """ Load yaml file and return as dict. """
    with open(file) as yaml_file:
        return addict.Dict(yaml.safe_load(yaml_file))


config = load_yaml_file(
    os.path.abspath(os.path.join("smart_queue", "config", "config.yaml"))
)

logger = logging.getLogger(__name__)
logging.config.dictConfig(config.logging)
