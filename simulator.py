from typing import List, Tuple

import pendulum
import simpy
from pyparsing import line

from smart_queue.analysis import CONDITION_TABLE, CONFIGURATION_PATH
from smart_queue.analysis.classes.Patient import Patient


class Queue(object):
    def __init__(self, env, ambulance, configuration_id, eval_type) -> None:
        self.env = env
        self.loaded_conf_file = self.load_configuration(
            configuration_id=configuration_id
        )
        self.ambulance = ambulance
        # self.current_patient = self.patients.pop(0)
        self.type = eval_type
        self.current_waiting_time = 0

        self.action = self.run()

    def eval_priority(self, patient):
        # NOTE: Original algorithm is @ smart_queue.db.database

        if self.type == 1:
            duration = pendulum.from_timestamp(self.env.now).timestamp() - pendulum.parse(patient.time_arrived).timestamp()
            
            if duration > 0:
                return (duration * patient.condition_urgency) / patient.burst_time

            return 0

        return 1

    def reevaluate_queue(self):
        queue = self.patients

        for patient in queue:
            patient.priority = self.eval_priority(patient)

        # print("Evaluating queue")

        queue = sorted(queue, key = lambda x: (-x.priority, x.time_arrived))

        self.patients = queue


    def get_next_patient(self):
        new_waiting_time = self.current_waiting_time - self.current_patient.burst_time
    
        if new_waiting_time >= 0:
            self.current_waiting_time = new_waiting_time
            
        self.reevaluate_queue()
        self.current_patient = self.patients.pop(0)


    def run(self):
        while not self.loaded_conf_file:
            self.env.run()

            current_time = pendulum.from_timestamp(self.env.now).timestamp()
            arrive_time = pendulum.parse(patient.time_arrived).timestamp()


        # for index, patient in enumerate(self.patients):      
        #     self.env.process(
        #         self.client(
        #             f"Patient {patient.id}",
        #             self.ambulance,
        #             patient,
        #             procedure_time=patient.burst_time,
        #         ),
        #     )

        
    def client(self, name, ambulance, patient, procedure_time):
        current_time = pendulum.from_timestamp(self.env.now).timestamp()
        ctime_human = pendulum.from_timestamp(self.env.now).to_time_string()
        arrive_time = pendulum.parse(patient.time_arrived).timestamp()
        atime_human = pendulum.parse(patient.time_arrived).to_time_string()

        time_delta = arrive_time - current_time

        # Wait till time is actually arive time
        if time_delta > 0:
            yield self.env.timeout(time_delta) 

        self.reevaluate_queue()
        print(f"{name} - Arrived @ {pendulum.from_timestamp(self.env.now).to_time_string()}")

        with ambulance.request() as req:
            if self.current_patient != patient:
                yield self.env.timeout(self.current_waiting_time)  # Wait one min, if not chosen by priority
            
            yield req
            
            wait = self.env.now - pendulum.parse(patient.time_arrived).timestamp()

            print(f"{name} - Inside (Waited for {round(wait/60, 3)} min)")

            self.current_waiting_time += procedure_time
            yield self.env.timeout(procedure_time * 60)

            self.get_next_patient()
            print(
                f"{name} - Out @ {pendulum.from_timestamp(self.env.now).to_time_string()}"
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
    ambulance = simpy.Resource(env, capacity=1)

    queue = Queue(env, ambulance, 2, 1)