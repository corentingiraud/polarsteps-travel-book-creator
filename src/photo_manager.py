import json
import os
from pathlib import Path
import shutil
from typing import List
from models.photo import Photo
from models.trip import Trip


PHOTOS_BY_PAGES_FILE_NAME = "photos_by_pages.txt"
PHOTOS_MAPPING_FILE_NAME = "photos_mapping.json"


class PhotoManager:
    def save_photos_pages(self, trip: Trip, save_path: Path):
        # Create dictionaries to hold the data for the two files
        photos_mapping = {}
        photos_by_pages: List[str] = []

        # Iterate over each step in the trip
        for step in trip.steps:
            # Add step name to photos_by_pages
            photos_by_pages.append(step.get_name_for_photos_by_pages_export())

            # Prepare a list to hold all photo indices for the step
            step_photos_mapping = {}
            for photo in step.photos:
                step_photos_mapping[photo.index] = photo.to_dict()

            # Save the photo mapping for this step
            photos_mapping[step.id] = step_photos_mapping

            # Iterate over pages in the step and append the photo indices
            for page in step.photos_by_pages:
                photos_by_pages.append(" ".join(str(photo.index) for photo in page))

            # Add an empty line to separate the step
            photos_by_pages.append("")

        # Save the two files
        with open(
            save_path.joinpath(PHOTOS_MAPPING_FILE_NAME),
            "w",
        ) as f:
            json.dump(photos_mapping, f, indent=4)

        with open(
            save_path.joinpath(PHOTOS_BY_PAGES_FILE_NAME),
            "w",
        ) as f:
            f.write("\n".join(photos_by_pages))

    def get_photos_mapping_from_file(self, trip: Trip, save_path: Path):
        try:
            with open(
                save_path.joinpath(PHOTOS_MAPPING_FILE_NAME),
                "r",
            ) as f:
                return json.load(f)

        except FileNotFoundError:
            print(
                f"ℹ️ No file named '{trip.get_formatted_name()}{PHOTOS_MAPPING_FILE_NAME}' found. Continuing with default photos by pages."
            )

    def get_photos_by_pages_from_file(self, trip: Trip, save_path: Path):
        try:
            with open(
                save_path.joinpath(PHOTOS_BY_PAGES_FILE_NAME),
                "r",
            ) as f:
                return f.read().splitlines()
        except FileNotFoundError:
            print(
                f"ℹ️ No file named '{trip.get_formatted_name()}{PHOTOS_BY_PAGES_FILE_NAME}' found. Continuing with default photos by pages."
            )

    def load_photos_pages(self, trip: Trip, save_path: Path):
        photos_mapping = self.get_photos_mapping_from_file(trip, save_path)
        photos_by_pages = self.get_photos_by_pages_from_file(trip, save_path)

        if not photos_mapping or not photos_by_pages:
            trip.compute_default_photos_by_pages()
            return

        for step in trip.steps:
            line_index = None

            try:
                line_index = (
                    photos_by_pages.index(step.get_name_for_photos_by_pages_export())
                    + 1
                )
            except ValueError:
                print(
                    f"ℹ️ Step '{step.get_name_for_photos_by_pages_export()}' is present in PolarSteps export but not in '{trip.get_formatted_name()}{PHOTOS_BY_PAGES_FILE_NAME}' file. Using default layout..."
                )
                step.compute_default_photos_by_pages()
                continue

            while (
                len(photos_by_pages) > line_index and photos_by_pages[line_index] != ""
            ):
                photo_indexes = photos_by_pages[line_index].split(" ")

                photos_for_this_page = [
                    Photo.from_dict(photos_mapping[str(step.id)][photo_index])
                    for photo_index in photo_indexes
                ]

                step.photos_by_pages.append(photos_for_this_page)

                line_index += 1

            # Check if all photos loaded from PolarSteps export are present in pages.
            photos_not_in_pages = [
                photo
                for photo in step.photos
                if any(photo in page for page in step.photos_by_pages)
            ]

            if photos_not_in_pages:
                print(
                    f"ℹ️ A photo is present in the PolarSteps export but not in '{trip.get_formatted_name()}{PHOTOS_BY_PAGES_FILE_NAME}' file. Using default layout for the step '{step.get_name_for_photos_by_pages_export()}'..."
                )
                step.compute_default_photos_by_pages()

    def load_from_polarsteps_export(
        self, data_path: Path, output_path_for_photos: Path, trip: Trip
    ):
        output_path_for_photos.mkdir(parents=True, exist_ok=True)

        for step in trip.steps:
            photo_directory = data_path.joinpath(step.get_photo_directory_name())
            if os.path.exists(photo_directory):
                index = 1
                for photo_filename in os.listdir(photo_directory):
                    photo_path = photo_directory.joinpath(photo_filename)
                    destination_path = output_path_for_photos.joinpath(photo_filename)
                    shutil.copy(photo_path, destination_path)
                    photo = Photo(
                        id=photo_filename,
                        index=index,
                        path=destination_path,
                    )
                    step.photos.append(photo)
                    index += 1
