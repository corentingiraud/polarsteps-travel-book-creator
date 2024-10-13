from datetime import datetime
from typing import List
from models.step import Step


class Trip:
    steps: List[Step]

    def __init__(self, start_date: float, end_date: float, steps: List[Step]):
        self.steps = steps
        self.start_date = datetime.fromtimestamp(start_date) if start_date else None
        self.end_date = datetime.fromtimestamp(end_date) if end_date else None

    def get_last_step_date(self) -> datetime:
        return max(self.steps, key=lambda step: step.start_time).start_time

    def get_duration_in_days(self) -> int:
        if self.end_date:
            return (self.end_date - self.start_date).days
        return (self.get_last_step_date() - self.start_date).days

    def get_template_vars(self):
        out = {"steps": []}

        for step in self.steps:
            out["steps"].append(step.get_template_vars(self.start_date, self.get_duration_in_days()))

        return out
