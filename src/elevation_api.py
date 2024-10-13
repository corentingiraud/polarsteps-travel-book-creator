from itertools import islice
import requests
import time
import json
import os

class ElevationAPI:
    def __init__(self, cache_file='data/elevation_cache.json'):
        self.api_url = "https://api.opentopodata.org/v1/aster30m"
        self.max_locations_per_request = 100
        self.max_calls_per_day = 1000
        self.calls_made = 0
        self.cache_file = cache_file

        # Load cache from file if it exists
        self.cache = self._load_cache()

    def get_elevation(self, locations: list):
        """
        Get the elevation for a list of locations in batches, using a caching layer and respecting API limitations.
        
        :param locations: A list of tuples where each tuple contains (latitude, longitude)
        :return: A list of elevations corresponding to each location
        """
        all_elevations = []
        locations_to_query = []

        # First, check if locations are in cache
        for loc in locations:
            lat, lon = loc
            key = f"{lat},{lon}"
            if key in self.cache:
                all_elevations.append(self.cache[key])
            else:
                locations_to_query.append(loc)

        # Process only locations that were not found in cache
        location_batches = self._chunks(locations_to_query, self.max_locations_per_request)

        for batch in location_batches:
            if self.calls_made >= self.max_calls_per_day:
                print("Reached the maximum number of API calls for today.")
                break

            # Prepare the locations string for the API request
            locations_param = "|".join([f"{lat},{lon}" for lat, lon in batch])
            url = f"{self.api_url}?locations={locations_param}"

            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()

                if "results" in data:
                    for loc, result in zip(batch, data["results"]):
                        lat, lon = loc
                        elevation = result.get("elevation")
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
                all_elevations.extend([None] * len(batch))  # Return None for each location in case of an error

        # Save updated cache to file
        self._save_cache()

        return all_elevations

    def _chunks(self, data, size):
        """
        Yield successive n-sized chunks from a list.
        """
        iterator = iter(data)
        for first in iterator:
            yield [first] + list(islice(iterator, size - 1))

    def _load_cache(self):
        """
        Load the cache from a JSON file if it exists, otherwise return an empty dictionary.
        """
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_cache(self):
        """
        Save the cache to a JSON file.
        """
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f)
