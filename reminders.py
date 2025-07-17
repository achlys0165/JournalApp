from datetime import datetime, timedelta

class Reminder:
    def __init__(self, hour: int, minute: int, message: str):
        self.time = datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
        if self.time < datetime.now():
            self.time += timedelta(days=1)
        self.message = message

    def __lt__(self, other):
        return self.time < other.time

    def __repr__(self):
        return f"Reminder({self.time.strftime('%H:%M')}, {self.message})"

class OrderedArray:
    def __init__(self):
        self.data = []

    def insert(self, reminder: Reminder):
        self.data.append(reminder)
        self.data.sort()

    def pop_due(self):
        if self.data and self.data[0].time <= datetime.now():
            return self.data.pop(0)
        return None

    def peek(self):
        return self.data[0] if self.data else None
