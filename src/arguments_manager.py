import argparse

class ArgumentManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ArgumentManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.parser = argparse.ArgumentParser(description="Manage application arguments")
        self.parser.add_argument('--debug', action='store_true', help='Enable DEBUG mode')
        self.args = self.parser.parse_args()

    def get_args(self):
        return self.args
