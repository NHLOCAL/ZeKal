# --- START OF FILE html_to_pdf_no_toc.py ---

from playwright.sync_api import sync_playwright
import pathlib
import sys

def html_to_pdf_plain(input_html: str, output_pdf: str):
    """
    Converts HTML to PDF using Playwright.
    NOTE: This method DOES NOT add a visual Table of Contents.
          It also typically DOES NOT generate a PDF Document Outline (Bookmarks).
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        html_resolved_path = pathlib.Path(input_html).resolve()
        print(f"Navigating to HTML file: file://{html_resolved_path}")
        # Ensure the page is fully loaded, including network resources if any
        page.goto(f"file://{html_resolved_path}", wait_until='networkidle') 

        # --- קוד יצירת תוכן העניינים הויזואלי הוסר/הופעל כהערה ---
        # page.evaluate("""
        # () => { ... קוד ה-TOC שהיה פה ... }
        # """)
        # ---------------------------------------------------------

        # לחכות לטעינת פונטים (אם יש) - חשוב לתצוגה נכונה
        print("Waiting for fonts to load...")
        try:
            # Increasing timeout just in case fonts take long
            page.evaluate("() => document.fonts.ready", timeout=60000) 
            print("Fonts loaded.")
        except Exception as e:
            # This might happen if there are no external fonts or they load extremely fast
            print(f"Could not explicitly wait for fonts (might be okay): {e}")

        print(f"Generating PDF '{output_pdf}' from '{input_html}' using Playwright...")
        try:
            page.pdf(
                path=output_pdf,
                format="A4",
                margin={"top": "1cm", "bottom": "1cm", "left": "1cm", "right": "1cm"},
                print_background=True,
                # tagged=False # Setting tagged=True rarely helps with outline and adds overhead
            )
            print(f"PDF generation complete (Playwright): {output_pdf}")
        except Exception as e:
             print(f"Error during Playwright PDF generation: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python html_to_pdf.py <input_html_path> <output_pdf_path>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Example usage from terminal:
    # python html_to_pdf_no_toc.py "C:\path\to\your\book.html" "book_plain.pdf"
    html_to_pdf_plain(input_file, output_file)