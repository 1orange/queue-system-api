import logging
import logging.config
import random

import numba as nb

import pendulum
from faker import Faker
from faker.providers import DynamicProvider

from smart_queue.analysis import CONFIGURATION_PATH
from smart_queue.db.database import get_all_conditions

logger = logging.getLogger(__name__)


def load_conditions():
    return [entry.name for entry in get_all_conditions()]


def generate_arrive_time(faker_instance, start, end) -> str:
    return pendulum.instance(
        faker_instance.date_time_between(start, end)
    ).to_time_string()


def generate_condition(faker_instance) -> str:
    return faker_instance.condition()


def register_provider(faker_instance):
    provider = DynamicProvider(
        provider_name="condition",
        elements=load_conditions(),
    )

    faker_instance.add_provider(provider)


def generate_configuration(conf_obj, SEED=1):
    logger.info(f"Iteration {SEED} - Generating")
    randon_instance = random.Random(SEED)

    fake = Faker()
    Faker.seed(SEED)

    register_provider(fake)

    start_time = pendulum.parse("08:00:00")
    end_time = pendulum.parse("16:00:00")

    configuration = [
        (
            generate_condition(fake),
            generate_arrive_time(fake, start_time, end_time),
        )
        for _ in range(randon_instance.randint(30, 80))
    ]

    logger.info(f"Iteration {SEED} - Done")

    conf_obj[SEED] = sorted(configuration, key=lambda v: v[1])
