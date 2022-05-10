from typing import List, Tuple
import pendulum
import simpy
from pyparsing import line

from smart_queue.analysis import CONDITION_TABLE, CONFIGURATION_PATH
from smart_queue.analysis.classes.Patient import Patient


def parse_configuration_line(line_raw: str) -> Tuple[str, str]:
    line = line_raw.split()

    condition = line[0].strip()
    arrival_time = line[1].strip()

    return condition, arrival_time


def load_configuration(configuration_id: int) -> List[Patient]:
    with open(
        file=f"{CONFIGURATION_PATH}/example",
        mode="r",
        encoding="utf-8",
    ) as file:
        patients = []

        for line in file:
            condition, arrival_time = parse_configuration_line(line)

            patients.append(Patient(CONDITION_TABLE[condition], arrival_time))
        
        return patients


def source(env, patients, ambulance):
    for index, patient in enumerate(patients):
        c = client(
            env,
            f"Patient {index}",
            ambulance,
            patient,
            procedure_time=patient.burst_time,
        )

        env.process(c)


def client(env, name, ambulance, patient, procedure_time):
    print(f"{name} arrived at {pendulum.parse(patient.time_arrived).to_time_string()}")

    with ambulance.request() as req:
        results = yield req

        wait = pendulum.parse(patient.time_arrived).add(minutes=procedure_time).timestamp() - env.now

        # print("%s waited %6.3f" % (name, pendulum.parse(wait).to_time_string()))
        print(f"{name} waited {wait//60} minutes")

        yield env.timeout(procedure_time)
        # print("%s exited the office at %7.4f" % (name, pendulum.parse(env.now).to_time_string()))
        print(f"{name} exited the ambulance at {pendulum.from_timestamp(env.now).add(seconds=wait).to_time_string()}")


if __name__ == "__main__":
    patients = load_configuration(configuration_id=1)

    # print(clients)

    env = simpy.Environment(
        initial_time=pendulum.parse("08:00:00").timestamp(),
    )

    ambulance = simpy.Resource(env, capacity=1)
    source(env, patients, ambulance)
    env.run()
