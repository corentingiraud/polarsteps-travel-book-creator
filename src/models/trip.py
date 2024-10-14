from datetime import datetime
from typing import Any, Dict, List
from models.step import Step


class Trip:
    steps: List[Step]

    def __init__(self, id: int, name: str, start_date: float, end_date: float | None, steps: List[Step]):
        self.id = id
        self.name = name
        self.steps = steps
        self.start_date = datetime.fromtimestamp(start_date)
        self.end_date = datetime.fromtimestamp(end_date) if end_date else None

    def get_last_step_date(self) -> datetime:
        return max(self.steps, key=lambda step: step.start_time).start_time

    def get_duration_in_days(self) -> int:
        if self.end_date:
            return (self.end_date - self.start_date).days
        return (self.get_last_step_date() - self.start_date).days

    def get_template_vars(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {"steps": []}

        for step in self.steps:
            out["steps"].append(step.get_template_vars(self.start_date, self.get_duration_in_days()))

        return out
