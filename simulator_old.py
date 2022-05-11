from typing import List, Tuple

import pendulum
import simpy
from pyparsing import line

from smart_queue.analysis import CONDITION_TABLE, CONFIGURATION_PATH
from smart_queue.analysis.classes.Patient import Patient
from smart_queue.analysis.classes.store import PriorityBaseStore


class Queue(object):
    def __init__(self, env, ambulance, configuration_id, eval_type) -> None:
        self.env = env
        self.patients = self.load_configuration(
            configuration_id=configuration_id
        )
        self.ambulance = ambulance
        self.current_patient = self.patients.pop(0)
        self.type = eval_type
        self.current_waiting_time = 0

        self.action = self.run()

    def eval_priority(self, patient):
        # NOTE: Original algorithm is @ smart_queue.db.database

        if self.type == 1:
            duration = (
                pendulum.from_timestamp(self.env.now).timestamp()
                - pendulum.parse(patient.time_arrived).timestamp()
            )

            if duration > 0:
                return -(
                    (duration * patient.condition_urgency) / patient.burst_time
                )

            return 9999

        return 999

    def reevaluate_queue(self):
        queue = self.patients

        for patient in queue:
            patient.priority = self.eval_priority(patient)
            yield patient.update_request_priority(self.ambulance)

        queue = sorted(queue, key=lambda x: (x.priority, x.time_arrived))

        self.patients = queue

    def get_next_patient(self):
        new_waiting_time = (
            self.current_waiting_time - self.current_patient.burst_time
        )

        if new_waiting_time >= 0:
            self.current_waiting_time = new_waiting_time

        self.reevaluate_queue()
        self.current_patient = self.patients.pop(0)

    def fill_store(self):
        for patient in self.patients:
            self.env.process(
                self.client(
                    f"Patient {patient.id}",
                    self.ambulance,
                    patient,
                    procedure_time=patient.burst_time,
                ),
            )

    def run(self):
        self.fill_store()

        self.env.run()

    def client(self, name, ambulance, patient, procedure_time):
        current_time = pendulum.from_timestamp(self.env.now).timestamp()
        arrive_time = pendulum.parse(patient.time_arrived).timestamp()

        time_delta = arrive_time - current_time

        # Wait till time is actually arive time
        if time_delta > 0:
            yield self.env.timeout(time_delta)

        # while self.current_patient != patient:
        #         self.env.step()

        self.reevaluate_queue()
        print(
            f"{name} - Arrived @ {pendulum.from_timestamp(self.env.now).to_time_string()}"
        )

        with ambulance.request(priority=patient.priority) as req:
            # patient.req = ambulance.request(priority=-patient.priority)
            patient.req = req
            yield patient.req

            try:
                wait = (
                    self.env.now
                    - pendulum.parse(patient.time_arrived).timestamp()
                )

                print(f"{name} - Inside (Waited for {round(wait/60, 3)} min)")

                self.current_waiting_time += procedure_time
                yield self.env.timeout(procedure_time * 60)

                self.get_next_patient()
                print(
                    f"{name} - Out @ {pendulum.from_timestamp(self.env.now).to_time_string()}"
                )

            except simpy.Interrupt as interrupt:
                by = interrupt.cause.by
                usage = env.now - interrupt.cause.usage_since
                print(
                    f"{name} got preempted by {by} at {env.now}"
                    f" after {usage}"
                )

    def load_configuration(self, configuration_id: int) -> List[Patient]:
        with open(
            file=f"{CONFIGURATION_PATH}/configuration_{configuration_id}",
            # file=f"{CONFIGURATION_PATH}/example",
            mode="r",
            encoding="utf-8",
        ) as file:
            patients = []

            for pat_id, line in enumerate(file):
                condition, arrival_time = self._parse_configuration_line(line)

                patients.append(
                    Patient(pat_id, CONDITION_TABLE[condition], arrival_time)
                )

            return patients

    def _parse_configuration_line(self, line_raw: str) -> Tuple[str, str]:
        line = line_raw.split()

        condition = line[0].strip()
        arrival_time = line[1].strip()

        return condition, arrival_time


if __name__ == "__main__":
    env = simpy.Environment(
        initial_time=pendulum.parse("08:00:00").timestamp(),
    )
    ambulance = simpy.PriorityResource(env, capacity=1)

    queue = Queue(env, ambulance, 2, 1)
