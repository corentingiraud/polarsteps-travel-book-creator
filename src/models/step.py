from datetime import datetime
import random
from typing import Any, Dict, List

from models.photo import Photo, PhotoRatio
from translations import (
    COUNTRIES,
    UNKNOWN_COUNTRY,
    UNKNOWN_WEATHER,
    WEATHER_CONDITION,
)

DESCRIPTION_MAX_CHAR_COVER_PHOTO = 800


class Step:
    def __init__(
        self,
        name: str,
        description: str | None,
        country: str,
        country_code: str,
        weather_condition: str,
        weather_temperature: float,
        start_time: float,
        lat: float,
        lon: float,
        slug: str,
        id: int,
        elevation: int | None = None,
        position_percentage: tuple[float, float] | None = None,
    ):
        self.name = name
        self.description = description
        self.country = COUNTRIES[country] if country else UNKNOWN_COUNTRY
        self.country_code = country_code
        self.weather_condition = (
            WEATHER_CONDITION[weather_condition]
            if weather_condition
            else UNKNOWN_WEATHER
        )
        self.weather_temperature = weather_temperature
        self.start_time = datetime.fromtimestamp(start_time)
        self.lat = lat
        self.lon = lon
        self.elevation = elevation
        self.position_percentage: tuple[float, float] | None = position_percentage
        self.photos: list[Photo] = []
        self.slug: str = slug
        self.id: int = id
        self.photos_by_pages: List[List[Photo]] = []
        self.cover_photo: Photo | None = None

    def should_use_cover_photo(self) -> bool:
        return (
            not self.description
            or len(self.description) < DESCRIPTION_MAX_CHAR_COVER_PHOTO
        )

    def compute_default_photos_by_pages(self):
        self.photos_by_pages = []
        candidates = self.photos.copy()

        # Handle cover photo if needed
        if self.should_use_cover_photo():
            self.cover_photo = next(
                (photo for photo in self.photos if photo.ratio == PhotoRatio.PORTRAIT),
                next(
                    (
                        photo
                        for photo in self.photos
                        if photo.ratio == PhotoRatio.LANDSCAPE
                    ),
                    None,
                ),
            )
            if self.cover_photo:
                candidates.remove(self.cover_photo)

        landscape_candidates = [
            photo for photo in candidates if photo.ratio == PhotoRatio.LANDSCAPE
        ]
        portrait_candidates = [
            photo for photo in candidates if photo.ratio == PhotoRatio.PORTRAIT
        ]
        other_candidates = [
            photo
            for photo in candidates
            if photo.ratio not in {PhotoRatio.PORTRAIT, PhotoRatio.LANDSCAPE}
        ]

        # Priority 1: 4 photos, must be 4 landscape
        while len(landscape_candidates) >= 4:
            self.photos_by_pages.append(landscape_candidates[:4])
            landscape_candidates = landscape_candidates[4:]

        # Priority 2: 3 photos, must be 2 landscape + 1 portrait
        while len(landscape_candidates) >= 2 and len(portrait_candidates) >= 1:
            self.photos_by_pages.append(
                landscape_candidates[:2] + [portrait_candidates[0]]
            )
            landscape_candidates = landscape_candidates[2:]
            portrait_candidates = portrait_candidates[1:]

        # Priority 3: 2 photos, must be 2 portrait
        while len(portrait_candidates) >= 2:
            self.photos_by_pages.append(portrait_candidates[:2])
            portrait_candidates = portrait_candidates[2:]

        # Priority 4: 1 photo
        while len(portrait_candidates) > 0:
            self.photos_by_pages.append([portrait_candidates[0]])
            portrait_candidates = portrait_candidates[1:]
        while len(landscape_candidates) > 0:
            self.photos_by_pages.append([landscape_candidates[0]])
            landscape_candidates = landscape_candidates[1:]
        while len(other_candidates) > 0:
            self.photos_by_pages.append([other_candidates[0]])
            other_candidates = other_candidates[1:]

        random.shuffle(self.photos_by_pages)

    def get_name_for_photos_by_pages_export(self):
        return f"{self.start_time.strftime("%d/%m/%Y")} {self.name} ({self.id})"

    def get_photo_directory_name(self):
        return f"{self.slug}_{self.id}/photos"

    def get_lat_lon_as_tuple(self):
        return (self.lat, self.lon)

    def get_day_number(self, trip_start_date: datetime):
        return (self.start_time - trip_start_date).days + 1

    def get_trip_percentage(
        self,
        trip_start_date: datetime,
        trip_duration_in_days: int,
    ):
        return self.get_day_number(trip_start_date) * 100 / trip_duration_in_days

    def get_template_vars(
        self, trip_start_date: datetime, trip_duration_in_days: int
    ) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "country": self.country,
            "country_code": self.country_code,
            "weather_condition": self.weather_condition,
            "weather_temperature": self.weather_temperature,
            "start_time": self.start_time,
            "day_number": self.get_day_number(trip_start_date),
            "trip_percentage": self.get_trip_percentage(
                trip_start_date, trip_duration_in_days
            ),
            "elevation": self.elevation,
            "position_percentage": self.position_percentage,
            "photos_by_pages": [
                [photo.get_template_vars() for photo in page]
                for page in self.photos_by_pages
            ],
            "cover_photo": self.cover_photo.get_template_vars() if self.cover_photo else None,
        }
