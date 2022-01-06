"""
Purpose of this module is to define global variables used among other modules.
"""

import logging
import logging.config

from assets.classes.QueueClass import QueueClass
from assets.helpers.loaders import load_yaml_config

logger = logging.getLogger(__name__)

# Load config and set-up logger
config = load_yaml_config()
logging.config.dictConfig(config.logging)

clients_queue = QueueClass(logger)
