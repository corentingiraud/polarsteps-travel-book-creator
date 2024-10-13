from datetime import datetime
from typing import Any, Dict, List, Tuple

from models.photo import Photo
from models.photo_layout import PhotoLayout

WEATHER_CONDITION_FRENCH = {
    "partly-cloudy-day": "Partiellement couvert",
    "rain": "Pluvieux",
    "clear-day": "Ensoleille",
}
COUNTRIES_FRENCH = {
    "Montenegro": "Montenegro",
    "Albania": "Albanie",
    "Bosnia and Herzegovina": "Bosnie-Herzegovine",
    "Bulgaria": "Bulgarie",
    "Italy": "Italie",
    "Turkey": "Turquie",
    "North Macedonia": "Macedoine du Nord",
    "Pays inconnu": "Pays inconnu",
    "France": "France",
    "Slovenia": "Slovenie",
    "Croatia": "Croatie",
    "Greece": "Grece",
}
UNKNOWN_WEATHER_FRENCH = "Meteo inconnue"
UNKNOWN_COUNTRY_FRENCH = "Pays inconnu"


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
        self.country = COUNTRIES_FRENCH[country] if country else UNKNOWN_COUNTRY_FRENCH
        self.country_code = country_code
        self.weather_condition = (
            WEATHER_CONDITION_FRENCH[weather_condition]
            if weather_condition
            else UNKNOWN_WEATHER_FRENCH
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
        self.photo_layouts : List[Tuple[PhotoLayout, List[str]]] | None = None

    def get_photo_directory_name(self):
        return f"{self.slug}_{self.id}/photos"

    def get_lat_lon_as_tuple(self) -> tuple[float, float]:
        return (self.lat, self.lon)

    def get_day_number(self, trip_start_date: datetime):
        return (self.start_time - trip_start_date).days + 1

    def get_trip_percentage(
        self,
        trip_start_date: datetime,
        trip_duration_in_days: int,
    ):
        return self.get_day_number(trip_start_date) * 100 / trip_duration_in_days

    def get_template_vars(self, trip_start_date: datetime, trip_duration_in_days: int) -> Dict[str, Any]:
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
            "photo_layouts": self.photo_layouts
        }