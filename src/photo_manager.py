import os
from pathlib import Path
import shutil
from models.photo import Photo
from models.trip import Trip


class PhotoManager:
    def load(self, data_path: str, output_path_for_photos: str, trip: Trip):
        Path(output_path_for_photos).mkdir(parents=True, exist_ok=True)

        for step in trip.steps[0:5]:
            photo_directory = os.path.join(data_path, step.get_photo_directory_name())

            if os.path.exists(photo_directory):
                for photo_filename in os.listdir(photo_directory):
                    photo_path = os.path.join(photo_directory, photo_filename)
                    destination_path = os.path.join(
                        output_path_for_photos, photo_filename
                    )
                    shutil.copy(photo_path, destination_path)
                    photo = Photo(path=destination_path)
                    step.photos.append(photo)
