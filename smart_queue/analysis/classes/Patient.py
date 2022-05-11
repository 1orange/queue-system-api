import pendulum


class Patient:
    def __init__(self, patient_id, condition, time_arrived):
        self.id = patient_id
        self.condition = condition.name
        self.burst_time = int(condition.burst_time)
        self.priority = 999
        self.condition_urgency = condition.urgency
        self.time_arrived = time_arrived
        self.req = None
    
    def update_request_priority(self, resource):
        self.req.cancel()

        with resource.request(priority=self.priority) as req:
        # self.req = resource.request(priority=-self.priority)
            self.req = req
            return self.req

    def __str__(self):
        return (
            f"Patient {self.id}({self.condition}, {self.priority}, {self.time_arrived})"
        )

    def __repr__(self):
        return (
            f"Patient {self.id}({self.condition}, {self.priority}, {self.time_arrived})"
        )

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
