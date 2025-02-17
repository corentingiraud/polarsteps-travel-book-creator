from pathlib import Path


CURRENT_FILE_PATH = Path(__file__).resolve().parent
OUTPUT_PATH = CURRENT_FILE_PATH.parent.joinpath("travel_book")
HTML_FILE_NAME = "travel_book.html"
PDF_FILE_NAME = "travel_book.pdf"
DATA_PATH = CURRENT_FILE_PATH.parent.joinpath("data")
TRIP_DATA_PATH = DATA_PATH.joinpath("polarsteps-trip")
