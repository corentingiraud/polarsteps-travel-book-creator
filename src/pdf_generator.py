from playwright.sync_api import sync_playwright


class PDFGenerator:
    def generate(self, html_file_path: str, pdf_file_path: str):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context()
            page = context.new_page()
            page.goto(f"file://{html_file_path}.html")

            try:
                page.pdf(
                    path=f"{pdf_file_path}.pdf",
                    format="A4",
                    landscape=True,
                    print_background=True,
                    # page_ranges="999998-999999"
                )
            except Exception as e:
                if e.message and "Page range exceeds page count" in str(e.message): # type: ignore
                    # Try again with a new index
                    raise e
            browser.close()
