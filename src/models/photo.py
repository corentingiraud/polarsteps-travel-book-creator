from enum import Enum
from pathlib import Path
from typing import Any, Dict, Self
from PIL import Image


class PhotoRatio(Enum):
    SMARTPHONE_PORTRAIT = (9, 16)
    SMARTPHONE_LANDSCAPE = (16, 9)
    FULLSCREEN_PORTRAIT = (3, 4)
    FULLSCREEN_LANDSCAPE = (4, 3)
    UNKNOWN = (0, 0)


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
        side_by_side_ratios = {
            PhotoRatio.SMARTPHONE_PORTRAIT,
            PhotoRatio.FULLSCREEN_PORTRAIT,
        }
        return (
            self.ratio in side_by_side_ratios
            and other_photo.ratio in side_by_side_ratios
        )
    
    def is_portrait_ratio(self) -> bool:
        return self.ratio in {
            PhotoRatio.SMARTPHONE_PORTRAIT,
            PhotoRatio.FULLSCREEN_PORTRAIT,
        }

    def is_landscape_ratio(self) -> bool:
        return self.ratio in {
            PhotoRatio.SMARTPHONE_LANDSCAPE,
            PhotoRatio.FULLSCREEN_LANDSCAPE,
        }

    def compute_photo_ratio(self) -> PhotoRatio:
        try:
            with Image.open(self.path) as img:
                width, height = img.size

                if self.is_ratio(
                    width,
                    height,
                    PhotoRatio.SMARTPHONE_PORTRAIT.value[0],
                    PhotoRatio.SMARTPHONE_PORTRAIT.value[1],
                ):
                    return PhotoRatio.SMARTPHONE_PORTRAIT
                elif self.is_ratio(
                    width,
                    height,
                    PhotoRatio.SMARTPHONE_LANDSCAPE.value[0],
                    PhotoRatio.SMARTPHONE_LANDSCAPE.value[1],
                ):
                    return PhotoRatio.SMARTPHONE_LANDSCAPE
                elif self.is_ratio(
                    width,
                    height,
                    PhotoRatio.FULLSCREEN_PORTRAIT.value[0],
                    PhotoRatio.FULLSCREEN_PORTRAIT.value[1],
                ):
                    return PhotoRatio.FULLSCREEN_PORTRAIT
                elif self.is_ratio(
                    width,
                    height,
                    PhotoRatio.FULLSCREEN_LANDSCAPE.value[0],
                    PhotoRatio.FULLSCREEN_LANDSCAPE.value[1],
                ):
                    return PhotoRatio.FULLSCREEN_LANDSCAPE
                return PhotoRatio.UNKNOWN
        except Exception as e:
            print(f"⚠️ Error computing photo ratio for {self.path}: {e}")
            return PhotoRatio.UNKNOWN

    def get_template_vars(self):
        return {"path": self.path}

    @staticmethod
    def is_ratio(width: int, height: int, ratio_width: int, ratio_height: int) -> bool:
        return abs((width / height) - (ratio_width / ratio_height)) < 0.01

    def __eq__(self, other: Any):
        if isinstance(other, Photo):
            return self.id == other.id and self.path == other.path
        return False
    
    def __hash__(self):
        return hash((self.id, self.path))
