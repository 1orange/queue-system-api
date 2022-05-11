class Condition:
    def __init__(self, name, burst_time, urgency):
        self.name = name
        self.burst_time = int(burst_time)
        self.urgency = int(urgency)
