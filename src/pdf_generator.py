from pathlib import Path
from playwright.sync_api import sync_playwright

from arguments_manager import ArgumentManager


class PDFGenerator:
    def generate(self, html_file_path: Path, pdf_file_path: Path):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context()
            page = context.new_page()
            page.goto(f"file://{html_file_path}")
            page.pdf(
                path=pdf_file_path,
                format=ArgumentManager().paper_format,
                landscape=True,
                print_background=True,
                page_ranges=ArgumentManager().page_ranges
            )
            browser.close()
