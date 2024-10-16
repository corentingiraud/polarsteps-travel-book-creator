import json
import os
from pathlib import Path
import re
from typing import Set
from pyproj import Geod
import requests

from models.step import Step
from models.trip import Trip

DATA_SOURCE = "https://raw.githubusercontent.com/djaiss/mapsicon/master/all/{country_code}/vector.svg"
FILL_COLOR = "#4b5a6c"
COUNTRY_BOUNDING_BOXES_PATH = "data/country_bounding_boxes.json"


class MapManager:
    def __init__(self):
        with open(COUNTRY_BOUNDING_BOXES_PATH, "r") as f:
            self.country_bounding_boxes = json.load(f)
        self.geod = Geod(ellps="WGS84")

    def calculate_position_percentage(self, step: Step) -> tuple[float, float] | None:
        bounding_box = self.country_bounding_boxes.get(step.country_code.lower())

        if not bounding_box:
            print(f"ℹ️ No country bounding box data found for step '{step.name}'")
            return (0, 0)

        sw = bounding_box["sw"]
        ne = bounding_box["ne"]

        # Calculate the distance between southwest and northeast corners (both latitudinal and longitudinal distances)
        _, _, total_lat_distance = self.geod.inv(sw["lon"], sw["lat"], sw["lon"], ne["lat"])
        _, _, total_lon_distance = self.geod.inv(sw["lon"], sw["lat"], ne["lon"], sw["lat"])

        # Calculate the maximum of the two distances for square scaling
        max_distance = max(total_lat_distance, total_lon_distance)
        min_distance = min(total_lat_distance, total_lon_distance)
        diff_distance = max_distance - min_distance

        # Calculate the distance from the southwest to the step's latitude and longitude
        _, _, lat_distance = self.geod.inv(sw["lon"], sw["lat"], sw["lon"], step.lat)
        _, _, lon_distance = self.geod.inv(sw["lon"], sw["lat"], step.lon, sw["lat"])

        if max_distance == total_lat_distance:
            lon_distance += diff_distance / 2
        else:
            lat_distance += diff_distance / 2

        # Calculate the relative position as a percentage (compared to top-left corner)
        lat_percentage = (lat_distance / max_distance) * 100
        lon_percentage = (lon_distance / max_distance) * 100

        return lat_percentage, lon_percentage

    def update_style(self, maps_path: Path):
        for filename in os.listdir(maps_path):
            if filename.endswith(".svg"):
                file_path = maps_path.joinpath(filename)

                # Read the content of the SVG file
                with open(file_path, "r") as file:
                    content = file.read()

                # Use regex to replace fill="#000000" with the new FILL_COLOR
                updated_content = re.sub(
                    r'fill="#000000"', f'fill="{FILL_COLOR}"', content
                )

                # Write the updated content back to the file
                with open(file_path, "w") as file:
                    file.write(updated_content)

    def download_maps_from_trip(self, trip: Trip, output_path: Path):
        output_path.mkdir(parents=True, exist_ok=True)

        downloaded_countries: Set[str] = set()

        for step in trip.steps:
            if step.country_code in downloaded_countries:
                continue

            svg_url = DATA_SOURCE.format(country_code=step.country_code.lower())

            try:
                response = requests.get(svg_url)
                response.raise_for_status()

                svg_path = output_path / f"{step.country_code.lower()}.svg"

                with open(svg_path, "wb") as svg_file:
                    svg_file.write(response.content)

                downloaded_countries.add(step.country_code)

            except requests.exceptions.RequestException:
                print(f"ℹ️ Failed to download map for step '{step.name}'")
