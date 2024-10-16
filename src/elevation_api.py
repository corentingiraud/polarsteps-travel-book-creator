from itertools import islice
from pathlib import Path
from typing import Any, Dict, List, Tuple, Iterator, Optional
import requests
import time
import json
import os

CACHE_FILE_NAME = "elevation_cache.json"


class ElevationAPI:
    def __init__(self, cache_directory: Path) -> None:
        self.api_url: str = "https://api.opentopodata.org/v1/aster30m"
        self.max_locations_per_request: int = 100
        self.max_calls_per_day: int = 1000
        self.calls_made: int = 0
        self.cache_file = cache_directory.joinpath(CACHE_FILE_NAME)

        # Load cache from file if it exists
        self.cache: Dict[str, Optional[float]] = self._load_cache()

    def get_elevation(
        self, locations: List[Tuple[float, float]]
    ) -> List[Optional[float]]:
        """
        Get the elevation for a list of locations in batches, using a caching layer and respecting API limitations.

        :param locations: A list of tuples where each tuple contains (latitude, longitude)
        :return: A list of elevations corresponding to each location
        """
        all_elevations: List[Optional[float]] = []
        locations_to_query: List[Tuple[float, float]] = []

        # First, check if locations are in cache
        for loc in locations:
            lat, lon = loc
            key: str = f"{lat},{lon}"
            if key in self.cache:
                all_elevations.append(self.cache[key])
            else:
                locations_to_query.append(loc)

        # Process only locations that were not found in cache
        location_batches: Iterator[List[Tuple[float, float]]] = self._chunks(
            locations_to_query, self.max_locations_per_request
        )

        for batch in location_batches:
            if self.calls_made >= self.max_calls_per_day:
                print("Reached the maximum number of API calls for today.")
                break

            # Prepare the locations string for the API request
            locations_param: str = "|".join([f"{lat},{lon}" for lat, lon in batch])
            url: str = f"{self.api_url}?locations={locations_param}"

            try:
                response = requests.get(url)
                response.raise_for_status()
                data: Dict[str, Any] = response.json()

                if "results" in data:
                    for loc, result in zip(batch, data["results"]):
                        lat, lon = loc
                        elevation: Optional[float] = result.get("elevation")
                        all_elevations.append(elevation)

                        # Cache the result
                        key = f"{lat},{lon}"
                        self.cache[key] = elevation
                else:
                    all_elevations.extend([None] * len(batch))

                self.calls_made += 1

                # Respect the API rate limit (1 call per second)
                time.sleep(1)

            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
                all_elevations.extend(
                    [None] * len(batch)
                )  # Return None for each location in case of an error

        # Save updated cache to file
        self._save_cache()

        return all_elevations

    def _chunks(
        self, data: List[Tuple[float, float]], size: int
    ) -> Iterator[List[Tuple[float, float]]]:
        """
        Yield successive n-sized chunks from a list.
        """
        iterator = iter(data)
        for first in iterator:
            yield [first] + list(islice(iterator, size - 1))

    def _load_cache(self) -> Dict[str, Optional[float]]:
        """
        Load the cache from a JSON file if it exists, otherwise return an empty dictionary.
        """
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "r") as f:
                return json.load(f)
        return {}

    def _save_cache(self) -> None:
        """
        Save the cache to a JSON file.
        """
        with open(self.cache_file, "w") as f:
            json.dump(self.cache, f)
