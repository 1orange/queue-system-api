import random
from typing import List

import pendulum
from faker import Faker
from faker.providers import DynamicProvider

from smart_queue.analysis import CONFIGURATION_PATH
from smart_queue.db.database import get_all_conditions


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


def dump_to_file(configuration, file_name):
    with open(
        file=f"{CONFIGURATION_PATH}/{file_name}", mode="a", encoding="utf-8"
    ) as configuration_file:
        for patient in sorted(configuration, key=lambda v: v[1]):
            line_size = 50
            spaces = line_size - len(patient[0]) - len(patient[1])

            print(
                f"{patient[0]}{' '*spaces}{patient[1]}",
                file=configuration_file,
            )


def generate_configration(NAME="example_iter", SEED=1):
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

    dump_to_file(configuration, NAME)
