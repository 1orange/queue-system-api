import statistics
from typing import List, Tuple

import pendulum

from smart_queue.analysis import CONDITION_TABLE, CONFIGURATION_PATH
from smart_queue.analysis.classes.Patient import Patient


class Queue:
    def __init__(self, open_time, close_time, iter_data=None, naive=True):
        self.open_time = pendulum.parse(open_time)
        self.close_time = pendulum.parse(close_time)
        self.naive = naive
        self.configuration = iter_data
        self.current_patient = None
        self.current_time = self.open_time
        self.patient_to_arrive = self.configuration.pop(0)
        self.queue = []
        self.served = []

    def set_configuration(self, iter_data):
        self.configuration = iter_data

    def simulate(self):
        while True:
            # Check whether any patient arrived
            # If Patient arrived:
            #   - Add to queue
            #   - Reevevaluate queue
            if self.configuration:
                if self.current_time >= self.patient_to_arrive.time_arrived:
                    # print(
                    #     f"Patient {self.patient_to_arrive.id} - Arrived @ {self.patient_to_arrive.time_arrived.to_time_string()}"
                    # )

                    self.queue.append(self.patient_to_arrive)
                    self.patient_to_arrive = self.configuration.pop(0)

                    self.reevaluate_queue()

            # Check whether patient inside is done
            # If patient done:
            #   - Add patient to served
            #   - Get new patient
            if self.current_patient:
                if self.current_time == self.current_patient.time_arrived.add(
                    minutes=self.current_patient.burst_time
                    + self.current_patient.waiting_time
                ):
                    self.get_next_patient()

            # If no patient inside, try get one
            if not self.current_patient and self.queue:
                self.current_patient = self.queue.pop(0)

            self.current_time = self.current_time.add(seconds=1)

            if (
                not self.configuration
                and not self.queue
                and not self.current_patient
            ):
                break

        return self.get_median_wait_time_condition()

    def get_median_wait_time_condition(self):
        # Map conditions
        stats_per_condition = {}

        for patient in self.served:
            if patient.condition in stats_per_condition:
                stats_per_condition[patient.condition] += [
                    patient.waiting_time
                ]

            else:
                stats_per_condition[patient.condition] = [patient.waiting_time]

        # return {
        #     condition: statistics.median(values)
        #     for condition, values in stats_per_condition.items()
        # }

        return stats_per_condition

    def eval_priority(self, patient):
        # NOTE: Original algorithm is @ smart_queue.db.database

        if not self.naive:
            duration = self.current_time - patient.time_arrived

            return (duration * patient.condition_urgency) / patient.burst_time

        return 1

    def reevaluate_queue(self):
        sorted_queue = self.queue

        for patient in sorted_queue:
            patient.priority = self.eval_priority(patient)

        self.queue = sorted(
            sorted_queue, key=lambda x: (-x.priority, x.time_arrived)
        )

    def get_next_patient(self):
        # Add to served
        self.served.append(self.current_patient)
        # print(f"Patient {self.current_patient.id} - Out @ {self.current_time.to_time_string()}")
        self.current_patient = None

        # Get next patient and update waiting time
        if self.queue:
            self.current_patient = self.queue.pop(0)
            self.current_patient.update_waiting_time(self.current_time)
            # print(
            #     f"Patient {self.current_patient.id} - Inside (Waited for {self.current_patient.waiting_time} min)"
            # )

        self.reevaluate_queue()

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

            return sorted(patients, key=lambda x: x.time_arrived)

    def _parse_configuration_line(self, line_raw: str) -> Tuple[str, str]:
        line = line_raw.split()

        condition = line[0].strip()
        arrival_time = line[1].strip()

        return condition, arrival_time
