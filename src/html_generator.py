from pathlib import Path
import shutil
from jinja2 import Environment, FileSystemLoader, select_autoescape

from models.trip import Trip


class HTMLGenerator:
    CURRENT_FILE_PATH = Path(__file__).resolve().parent
    TEMPLATE_VARS = {"project_root": CURRENT_FILE_PATH.parent}

    def __init__(self):

        env = Environment(
            loader=FileSystemLoader(self.CURRENT_FILE_PATH.joinpath("templates")),
            autoescape=select_autoescape(),
        )
        self.template = env.get_template("index.html")

    def generate(self, trip: Trip, output_file_path: Path):
        template_vars = trip.get_template_vars() | self.TEMPLATE_VARS

        html_as_str = self.template.render(template_vars)

        with open(output_file_path, "w") as out_file:
            out_file.write(html_as_str)

        shutil.copytree(
            self.CURRENT_FILE_PATH.parent.joinpath("assets"),
            Path(output_file_path).parent.joinpath("assets"),
            dirs_exist_ok=True,
        )
