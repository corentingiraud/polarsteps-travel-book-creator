from playwright.sync_api import sync_playwright


class PDFGenerator:
    def generate(self, html_file_path: str, pdf_file_path: str):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context()
            page = context.new_page()
            page.goto(f"file://{html_file_path}")
            page.pdf(
                path=pdf_file_path,
                format="A4",
                landscape=True,
                print_background=True,
                page_ranges="1-50"
            )
            browser.close()
