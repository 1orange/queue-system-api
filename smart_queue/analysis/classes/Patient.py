class Patient:
    def __init__(self, condition, time_arrived):
        self.condition = condition.name
        self.burst_time = int(condition.burst_time)
        self.priority = 1
        self.time_arrived = time_arrived

    def __str__ (self):
        return f"Patient({self.condition}, {self.priority}, {self.time_arrived})"
    
    def __repr__ (self):
        return f"Patient({self.condition}, {self.priority}, {self.time_arrived})"
