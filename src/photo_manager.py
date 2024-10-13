import os
from pathlib import Path
import shutil
from typing import Set
from models.photo import Photo
from models.photo_layout import PhotoLayout
from models.trip import Trip


class PhotoManager:
    def compute_photos_layouts(self, trip: Trip):
        for step in trip.steps:
            step.photo_layouts = []
            used_photos: Set[str] = set()  # Keep track of photos that have already been paired
            
            for i, photo in enumerate(step.photos):
                if photo.id in used_photos:
                    continue  # Skip if this photo is already used in a layout

                if photo.must_be_in_fullscreen():
                    step.photo_layouts.append(
                        (PhotoLayout.FULLSCREEN, [photo.path])
                    )
                    used_photos.add(photo.id)
                    continue

                # Try to find a matching photo for side-by-side layout
                pair_found = False
                for j in range(i + 1, len(step.photos)):
                    candidate = step.photos[j]
                    if candidate.id not in used_photos and photo.can_be_side_by_side(candidate):
                        # We found a matching pair for side-by-side layout
                        step.photo_layouts.append(
                            (PhotoLayout.TWO_PHOTOS_SIDE_BY_SIDE, [photo.path, candidate.path])
                        )
                        used_photos.update({photo.id, candidate.id})
                        pair_found = True
                        break

                if not pair_found:
                    # If no pair found, place the photo in fullscreen layout
                    step.photo_layouts.append(
                        (PhotoLayout.FULLSCREEN, [photo.path])
                    )
                    used_photos.add(photo.id)

    def load(self, data_path: str, output_path_for_photos: str, trip: Trip):
        Path(output_path_for_photos).mkdir(parents=True, exist_ok=True)

        for step in trip.steps:
            photo_directory = os.path.join(data_path, step.get_photo_directory_name())

            if os.path.exists(photo_directory):
                for photo_filename in os.listdir(photo_directory):
                    photo_path = os.path.join(photo_directory, photo_filename)
                    destination_path = os.path.join(
                        output_path_for_photos, photo_filename
                    )
                    shutil.copy(photo_path, destination_path)
                    photo = Photo(id=photo_filename, path=destination_path)
                    step.photos.append(photo)
