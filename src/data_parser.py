import os
import json
from pathlib import Path

from arguments_manager import ArgumentManager
from models.step import Step
from models.trip import Trip


class DataParser:
    def load(self, data_path: Path) -> Trip:
        file_path = data_path.joinpath("trip.json")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        with open(file_path, "r") as file:
            data = json.load(file)

        step_indices = ArgumentManager().step_indices

        steps = [
            Step(
                name=step["display_name"],
                description=step["description"],
                country=step["location"]["detail"],
                country_code=step["location"]["country_code"],
                weather_condition=step["weather_condition"],
                weather_temperature=step["weather_temperature"],
                start_time=step["start_time"],
                lat=step["location"]["lat"],
                lon=step["location"]["lon"],
                slug=step["slug"],
                id=step["id"],
            )
            for i, step in enumerate(data["all_steps"], start=1)
            if not step_indices or i in step_indices
        ]

        return Trip(
            id=data["id"],
            name=data["name"],
            steps=steps,
            start_date=data["start_date"],
            end_date=data["end_date"],
        )
