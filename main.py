import logging
import logging.config

from assets.classes.Queue import Queue
from assets.helpers.loaders import load_yaml_config

logger = logging.getLogger(__name__)

# Load config and set-up logger
config = load_yaml_config()
logging.config.dictConfig(config.logging)

queue = Queue(logger)
