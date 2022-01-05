import os
import pendulum
import random

from hashlib import sha256
from pathlib import Path


def generate_unique_client_id():
    """ Return SHA256 hash of current timestamp in UNIX format """

    current_timestamp = pendulum.now('Europe/Prague')
    curent_salt = random.randint(1, 100000)

    return sha256(
        f"{current_timestamp}{curent_salt}".encode('utf-8')
    ).hexdigest(), current_timestamp


def generate_config_path():
    return os.path.abspath(os.path.join('assets', 'config', 'config.yaml'))
