import pendulum


class Patient:
    def __init__(self, patient_id, condition, time_arrived):
        self.id = patient_id
        self.condition = condition.name
        self.burst_time = int(condition.burst_time)
        self.priority = 1
        self.condition_urgency = condition.urgency
        self.time_arrived = pendulum.parse(time_arrived)
        self.waiting_time = 0

    def update_waiting_time(self, current_time):
        duration = current_time - self.time_arrived
        self.waiting_time = duration.in_minutes()

    def __str__(self):
        return f"Patient {self.id}({self.condition}, {self.priority}, {self.time_arrived.to_time_string()})"

    def __repr__(self):
        return f"Patient {self.id}({self.condition}, {self.priority}, {self.time_arrived.to_time_string()})"

    def __eq__(self, other):
        return (
            other
            and self.condition == other.condition
            and self.time_arrived == other.time_arrived
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.condition, self.time_arrived))
