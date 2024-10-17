import argparse
from typing import Set


class ArgumentManager():
    _instance = None
    debug = False
    step_indices: Set[int] | None = None
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
            "--step_ranges",
            default=None,
            type=str,
            help='Specify step ranges to be generated. Example: "1-20" to generate from step 1 to step 20',
        )
        self.parser.add_argument(
            "--paper_format",
            default="A4",
            type=str,
            help="Specify paper format for the PDF. See https://playwright.dev/python/docs/api/class-page#page-pdf",
        )
        self.args = self.parser.parse_args()
        self.__dict__.update(vars(self.args))

        if self.args.step_ranges:
            self.step_indices = self.parse_step_ranges(self.args.step_ranges)

    def parse_step_ranges(self, step_ranges: str) -> Set[int]:
        """Parses step ranges string and returns a set of indices."""
        ranges: Set[int] = set()
        
        # Split the ranges by comma (if multiple ranges are provided)
        parts = step_ranges.split(',')
        
        for part in parts:
            if '-' in part:
                # Handle range like 1-20
                start, end = map(int, part.split('-'))
                ranges.update(range(start, end + 1))
            else:
                # Handle single step like '5'
                ranges.add(int(part))
        
        return ranges

    def get_args(self):
        return self.args
