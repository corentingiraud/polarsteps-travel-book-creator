import argparse


class ArgumentManager():
    _instance = None
    debug = False
    page_ranges: str | None = None
    paper_format: str | None = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ArgumentManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(
            "--debug", action="store_true", help="Enable DEBUG mode"
        )
        self.parser.add_argument(
            "--page_ranges",
            default=None,
            type=str,
            help='Specify page ranges to be printed. Example: "1-20" to print from page 1 to page 20',
        )
        self.parser.add_argument(
            "--paper_format",
            default="A4",
            type=str,
            help="Specify paper format for the PDF. See https://playwright.dev/python/docs/api/class-page#page-pdf",
        )
        self.args = self.parser.parse_args()
        self.__dict__.update(vars(self.args))

    def get_args(self):
        return self.args
