import json
import os
from pathlib import Path
import shutil
from typing import Any, Dict, List, Set
from models.photo import Photo
from models.trip import Trip


class PhotoManager:
    def save_photos_pages(self, trip: Trip, save_path: Path):
        data: List[List[List[Dict[str, Any]]]] = []
        for step in trip.steps:
            photos_by_pages = [
                [photo.to_dict() for photo in page] for page in step.photos_by_pages
            ]
            data.append(photos_by_pages)

        with open(save_path.joinpath(f"{trip.name}_photos.json"), "w") as f:
            json.dump(data, f, indent=4)

    def load_photos_pages(self, trip: Trip, save_path: Path):
        try:
            with open(save_path.joinpath(f"{trip.name}_photos.json"), "r") as f:
                data = json.load(f)

            for step, photos_by_pages in zip(trip.steps, data):
                # Convert dictionaries back into Photo objects
                step.photos_by_pages = [
                    [Photo.from_dict(photo_dict) for photo_dict in page]
                    for page in photos_by_pages
                ]
        except FileNotFoundError:
            print("⚠️ No saved photo pages found.")

    def compute_photos_pages(self, trip: Trip):
        for step in trip.steps:
            step.photos_by_pages = []
            used_photos: Set[str] = (
                set()
            )  # Keep track of photos that have already been paired

            for i, photo in enumerate(step.photos):
                if photo.id in used_photos:
                    continue  # Skip if this photo is already used in a page

                if photo.must_be_in_fullscreen():
                    step.photos_by_pages.append([photo])
                    used_photos.add(photo.id)
                    continue

                # Try to find a matching photo for side-by-side layout
                pair_found = False
                for j in range(i + 1, len(step.photos)):
                    candidate = step.photos[j]
                    if candidate.id not in used_photos and photo.can_be_side_by_side(
                        candidate
                    ):
                        # We found a matching pair for side-by-side layout
                        step.photos_by_pages.append([photo, candidate])
                        used_photos.update({photo.id, candidate.id})
                        pair_found = True
                        break

                if not pair_found:
                    # If no pair found, place the photo in fullscreen layout
                    step.photos_by_pages.append([photo])
                    used_photos.add(photo.id)

    def load(self, data_path: Path, output_path_for_photos: Path, trip: Trip):
        output_path_for_photos.mkdir(parents=True, exist_ok=True)

        for step in trip.steps:
            photo_directory = data_path.joinpath(step.get_photo_directory_name())

            if os.path.exists(photo_directory):
                for photo_filename in os.listdir(photo_directory):
                    photo_path = photo_directory.joinpath(photo_filename)
                    destination_path = output_path_for_photos.joinpath(photo_filename)
                    shutil.copy(photo_path, destination_path)
                    photo = Photo(id=photo_filename, path=destination_path)
                    step.photos.append(photo)
