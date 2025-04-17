# --- START OF FILE html_to_pdf_weasyprint_outline.py ---

from weasyprint import HTML, CSS
# from weasyprint.fonts import FontConfiguration # Uncomment if using custom font config
import pathlib
import sys

def html_to_pdf_with_outline(input_html: str, output_pdf: str):
    """
    Converts HTML to PDF using WeasyPrint, automatically generating
    a document outline (bookmarks) from valid h1-h6 tags.
    This version DOES NOT inject a visual Table of Contents.
    """
    print(f"Attempting conversion with WeasyPrint:")
    print(f"Input HTML: {input_html}")
    print(f"Output PDF: {output_pdf}")

    html_path = pathlib.Path(input_html).resolve()
    if not html_path.is_file():
        print(f"Error: Input HTML file not found at {html_path}")
        sys.exit(1)

    print(f"Reading HTML file: {html_path}")
    try:
        # WeasyPrint reads the HTML file directly and parses linked CSS
        html = HTML(filename=str(html_path))
        
        # Optional: Define CSS for pagination, margins etc. if not in HTML/CSS file
        # Add @page rules here if needed
        # css = CSS(string='''
        #     @page { 
        #         size: A4; 
        #         margin: 1cm; 
        #     }
        #     body { font-family: sans-serif; } /* Ensure fonts are available */
        # ''')

        print(f"Generating PDF '{output_pdf}' with document outline using WeasyPrint...")

        # The 'write_pdf' method automatically creates bookmarks from h1-h6 tags by default.
        html.write_pdf(
            output_pdf,
            # stylesheets=[css] # Uncomment if using the CSS string above
        )
        
        print("-" * 30)
        print(f"PDF generation with outline potentially complete: {output_pdf}")
        print("IMPORTANT:")
        print("1. Check the generated PDF in different viewers (Adobe Reader, Chrome/Firefox PDF Viewer).")
        print("2. Look for the 'Bookmarks' or 'Outline' panel in the viewer.")
        print("3. Ensure your original HTML file contains valid, non-empty <h1> to <h6> tags.")
        print("4. Verify WeasyPrint and its dependencies (Pango, Cairo, etc.) are correctly installed.")
        print("-" * 30)

    except Exception as e:
        print(f"\nError during WeasyPrint PDF generation: {e}")
        print("\nPossible causes:")
        print("- WeasyPrint or its dependencies (Pango, Cairo, etc.) might not be installed correctly.")
        print("- The HTML file might be invalid, inaccessible, or not UTF-8 encoded.")
        print("- There might be issues with linked CSS or image files.")
        print("Please consult the WeasyPrint documentation for installation and troubleshooting.\n")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python html_to_pdf_weasyprint_outline.py <input_html_path> <output_pdf_path>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Before running, make sure WeasyPrint and its dependencies are correctly installed!
    # On Debian/Ubuntu: sudo apt-get install python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
    # On Fedora: sudo dnf install python3-pip python3-setuptools python3-wheel python3-cffi cairo pango gdk-pixbuf2 libffi-devel
    # On macOS (using Homebrew): brew install pango cairo libffi gdk-pixbuf
    # Then: pip install WeasyPrint
    html_to_pdf_with_outline(input_file, output_file)
    # Example usage from terminal:
    # python html_to_pdf_weasyprint_outline.py "C:\path\to\your\book.html" "book_weasy_outline.pdf"