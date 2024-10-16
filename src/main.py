import locale
import os
import shutil
from pathlib import Path
import argparse


from arguments_manager import ArgumentManager
from data_parser import DataParser
from elevation_api import ElevationAPI
from html_generator import HTMLGenerator
from map_manager import MapManager
from pdf_generator import PDFGenerator
from photo_manager import PhotoManager


CURRENT_FILE_PATH = Path(__file__).resolve().parent
TMP_FOLDER = CURRENT_FILE_PATH.joinpath("tmp")
TMP_HTML_FILE_NAME = "travel_book.html"
PDF_FILE_NAME = "travel_book.pdf"
OUTPUT_PATH = CURRENT_FILE_PATH.parent
DATA_PATH = CURRENT_FILE_PATH.parent.joinpath("data")
TRIP_DATA_PATH = DATA_PATH.joinpath("polarsteps-trip")

locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")


def main():
    shutil.rmtree(TMP_FOLDER, ignore_errors=True)
    os.mkdir(TMP_FOLDER)

    arg_manager = ArgumentManager()
    data_parser = DataParser()
    html_generator = HTMLGenerator()
    map_manager = MapManager()
    pdf_generator = PDFGenerator()
    elevation_api = ElevationAPI()
    photo_manager = PhotoManager()

    # Parse data
    trip = data_parser.load(TRIP_DATA_PATH)

    # Load photo
    photo_manager.load_from_polarsteps_export(
        TRIP_DATA_PATH, Path(TMP_FOLDER).joinpath("assets/images/photos"), trip
    )
    photo_manager.load_photos_pages(trip, DATA_PATH)
    photo_manager.compute_photos_pages(trip)
    photo_manager.save_photos_pages(trip, DATA_PATH)

    # Get elevation
    locations = [step.get_lat_lon_as_tuple() for step in trip.steps]
    elevations = elevation_api.get_elevation(locations)

    for step, elevation in zip(trip.steps, elevations):
        if elevation is not None:
            step.elevation = int(elevation)

    # Maps managment
    map_manager.download_maps_from_trip(trip, TMP_FOLDER.joinpath("assets/images/maps"))
    map_manager.update_style(TMP_FOLDER.joinpath("assets/images/maps"))

    for step in trip.steps:
        step.position_percentage = map_manager.calculate_position_percentage(step)

    # HTML generation
    html_generator.generate(trip, TMP_FOLDER.joinpath(TMP_HTML_FILE_NAME))

    # PDF generation
    # pdf_generator.generate(
    #     TMP_FOLDER.joinpath(TMP_HTML_FILE_NAME),
    #     OUTPUT_PATH.joinpath(PDF_FILE_NAME),
    # )

    if not arg_manager.get_args().debug:
        shutil.rmtree(TMP_FOLDER)

    print("✅ Travel book has been successfully generated !")


main()
