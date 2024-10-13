import os
import json

import requests

from models.step import Step
from models.trip import Trip


class DataParser:
    def load(self, data_path: str) -> Trip:
        file_path = os.path.join(data_path, "trip.json")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        with open(file_path, "r") as file:
            data = json.load(file)

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
            for step in data["all_steps"]
        ]

        return Trip(steps=steps, start_date=data["start_date"], end_date=data["end_date"])
