from enum import Enum
from PIL import Image


class PhotoRatio(Enum):
    SMARTPHONE = "9:16"
    FULLSCREEN = "3:4"
    UNKNOWN = "unknown"


class PhotoOrientation(Enum):
    LANDSCAPE = 1
    PORTRAIT = 2
    UNKNOWN = 3


class Photo:
    def __init__(self, path: str):
        self.path = path
        self.ratio = self.compute_photo_ratio()
        self.orientation = self.compute_orientation()

    def compute_orientation(self) -> PhotoOrientation:
        try:
            # Open the image to get dimensions
            with Image.open(self.path) as img:
                width, height = img.size

                # Determine orientation
                if width > height:
                    return PhotoOrientation.LANDSCAPE
                elif height > width:
                    return PhotoOrientation.PORTRAIT
                else:
                    return PhotoOrientation.UNKNOWN
        except Exception as e:
            print(f"Error computing orientation for {self.path}: {e}")
            return PhotoOrientation.UNKNOWN

    def compute_photo_ratio(self) -> PhotoRatio:
        try:
            with Image.open(self.path) as img:
                width, height = img.size

                if self.is_ratio(width, height, 9, 16):
                    return PhotoRatio.SMARTPHONE
                elif self.is_ratio(width, height, 3, 4):
                    return PhotoRatio.FULLSCREEN
                else:
                    return PhotoRatio.UNKNOWN
        except Exception as e:
            print(f"⚠️ Error computing photo ratio for {self.path}: {e}")
            return PhotoRatio.UNKNOWN

    def get_template_vars(self):
        return {
            "path": self.path
        }

    @staticmethod
    def is_ratio(width: int, height: int, ratio_width: int, ratio_height: int) -> bool:
        return abs((width / height) - (ratio_width / ratio_height)) < 0.01
