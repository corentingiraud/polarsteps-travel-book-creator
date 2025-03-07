from enum import Enum
import os
from pathlib import Path
from typing import Any, Dict, Self
from PIL import Image

from constants import OUTPUT_PATH


class PhotoRatio(Enum):
    PORTRAIT = [(9, 16), (3, 4)]
    LANDSCAPE = [(16, 9), (4, 3)]
    UNKNOWN = []

    @staticmethod
    def get_ratio(width: int, height: int):
        for photo_ratio in PhotoRatio:
            for ratio in photo_ratio.value:
                ratio_width = ratio[0]
                ratio_height = ratio[1]
                if abs((width / height) - (ratio_width / ratio_height)) < 0.1:
                    return photo_ratio
        return PhotoRatio.UNKNOWN

class Photo:
    def __init__(self, id: str, index: int, path: Path):
        self.id = id
        self.index = index
        self.path = path
        self.ratio = self.compute_photo_ratio()
    
    @staticmethod
    def from_dict(data: Dict[str, Any]):
        return Photo(
            id=data.get("id", ""),
            index=data.get("index", 0),
            path=Path(data.get("path", "")),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "index": self.index,
            "path": str(self.path),
        }

    def can_be_side_by_side(self, other_photo: Self) -> bool:
        return self.ratio == PhotoRatio.PORTRAIT and other_photo.ratio == PhotoRatio.PORTRAIT

    def compute_photo_ratio(self) -> PhotoRatio:
        try:
            with Image.open(self.path) as img:
                width, height = img.size
                return PhotoRatio.get_ratio(width, height)
        except Exception:
            print(f"Unknown photo ratio for '{self.id}'.")
            return PhotoRatio.UNKNOWN

    def get_relative_path(self):
        return os.path.relpath(self.path, OUTPUT_PATH)

    def get_template_vars(self):
        return {"path": self.get_relative_path() }

    def __eq__(self, other: Any):
        if isinstance(other, Photo):
            return self.id == other.id and self.path == other.path
        return False
    
    def __hash__(self):
        return hash((self.id, self.path))
