import argparse
import os
from markdown_it import MarkdownIt
from weasyprint import HTML, CSS
# ייבוא שהזכרת - הוא כבר היה קיים בקוד הקודם והוא חיוני
from weasyprint.text.fonts import FontConfiguration

def convert_md_to_pdf(md_file_path, pdf_file_path):
    """
    Converts a Markdown file to a styled PDF using markdown-it-py and WeasyPrint.
    Features modern Google Font (Rubik) and refined styling for Hebrew.

    Args:
        md_file_path (str): Path to the input Markdown file.
        pdf_file_path (str): Path for the output PDF file.
    """
    print(f"Starting conversion: {md_file_path} -> {pdf_file_path}")

    if not os.path.exists(md_file_path):
        print(f"Error: Input Markdown file not found at {md_file_path}")
        return

    # --- 1. Read Markdown Content ---
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        print("Successfully read Markdown file.")
    except Exception as e:
        print(f"Error reading Markdown file: {e}")
        return

    # --- 2. Define Modern CSS Styling with Google Fonts ---
    # !!! >>> CRITICAL: Download and install the 'Rubik' font family <<< !!!
    # from Google Fonts (https://fonts.google.com/specimen/Rubik)
    # for WeasyPrint to render the PDF correctly.
    # Also ensure 'Consolas' or 'Courier New' are available for code blocks.
    css_style = """
    /* Optional: @font-face can help if WeasyPrint doesn't find the font automatically,
       but usually installing it system-wide is enough. Uncomment and adjust path if needed. */
    /*
    @font-face {
        font-family: 'Rubik';
        src: url('/path/to/your/fonts/Rubik-VariableFont_wght.ttf');
    }
    @font-face {
        font-family: 'Rubik';
        font-weight: bold;
        src: url('/path/to/your/fonts/Rubik-Bold.ttf'); // Example if variable font not used
    }
    */

    @page {
        size: A4;
        margin: 2.5cm 2cm; /* Generous margins */

        @bottom-center {
            content: "עמוד " counter(page);
            font-size: 9pt;
            color: #555; /* Slightly darker footer text */
            /* Use the modern font here too */
            font-family: 'Rubik', Arial, sans-serif;
            font-weight: 300; /* Lighter weight for footer */
        }
    }

    body {
        /* Using Rubik as the main font */
        font-family: 'Rubik', 'Noto Sans Hebrew', Arial, sans-serif;
        font-weight: 400; /* Regular weight for body */
        font-size: 11pt; /* Slightly smaller font size for sans-serif is often okay */
        line-height: 1.7;  /* Adjusted line height for Rubik */
        direction: rtl;
        text-align: justify;
        color: #2d3436; /* Very dark gray, almost black */
        widows: 3;
        orphans: 3;
    }

    /* --- Headings (using Rubik with heavier weights) --- */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Rubik', 'Noto Sans Hebrew', Arial, sans-serif; /* Consistent font */
        margin-top: 1.8em;
        margin-bottom: 0.9em;
        color: #0984e3; /* Modern blue color */
        page-break-after: avoid;
        page-break-inside: avoid;
    }

    h1 { /* Chapter Title */
        font-size: 2.5em;
        font-weight: 700; /* Bold Rubik */
        color: #0984e3; /* Primary blue */
        text-align: center;
        margin-bottom: 1.5em; /* More space after main title */
        border-bottom: 2px solid #74b9ff; /* Lighter blue accent line */
        padding-bottom: 0.5em;
        page-break-before: always;
    }

    body > h1:first-of-type {
        page-break-before: auto;
        margin-top: 0;
    }

    h2 {
        font-size: 1.9em;
        font-weight: 600; /* Semi-bold Rubik */
        color: #0984e3; /* Consistent blue */
        border-bottom: 1px solid #dfe6e9;
        padding-bottom: 0.3em;
    }

    h3 {
        font-size: 1.5em;
        font-weight: 500; /* Medium Rubik */
        color: #636e72; /* Darker gray for sub-sub headings */
    }

    /* --- Paragraphs and Text Elements --- */
    p {
        margin-top: 0;
        margin-bottom: 1em;
    }

    strong, b {
        font-weight: 600; /* Use semi-bold for emphasis with Rubik */
    }

    em, i {
        /* Italic might look different in Rubik, check if you like it */
        font-style: italic;
        /* Or use a slightly lighter weight/color for emphasis */
        /* color: #636e72; */
    }

    /* --- Lists --- */
    ul, ol {
        margin-bottom: 1em;
        padding-right: 2.5em;
    }

    li {
        margin-bottom: 0.5em;
    }

    /* --- Links --- */
    a {
        color: #0984e3; /* Use the primary blue */
        text-decoration: none;
        border-bottom: 1px dashed #74b9ff; /* Dashed underline */
        transition: color 0.2s, border-bottom-color 0.2s; /* Smooth hover effect */
        page-break-inside: avoid;
    }

    a:hover {
        color: #0056b3; /* Darker blue on hover */
        border-bottom-color: #0056b3; /* Solid underline on hover */
        border-bottom-style: solid;
    }

    /* --- Code Blocks --- */
    pre {
        background-color: #f6f8fa; /* GitHub-like light background */
        border: 1px solid #dfe6e9;
        border-radius: 5px;
        padding: 1em 1.2em;
        overflow-x: auto;
        direction: ltr;
        text-align: left;
        font-family: 'Consolas', 'Courier New', monospace; /* Keep monospace for code */
        font-size: 10pt;
        line-height: 1.5;
        color: #2d3436;
        page-break-inside: avoid;
    }

    code { /* Inline code */
        font-family: 'Consolas', 'Courier New', monospace;
        background-color: #dfe6e9;
        padding: 0.2em 0.5em;
        border-radius: 4px;
        font-size: 0.9em;
        color: #2d3436;
        direction: ltr;
        word-wrap: break-word;
    }

    /* --- Blockquotes --- */
    blockquote {
        border-right: 5px solid #74b9ff; /* Accent color border */
        padding-right: 1.5em;
        margin-right: 0;
        margin-left: 0;
        margin-top: 1.5em;
        margin-bottom: 1.5em;
        color: #636e72; /* Gray text */
        /* No italics by default, let Markdown handle emphasis */
        page-break-inside: avoid;
    }

    blockquote p { /* Style paragraphs inside blockquote if needed */
        margin-bottom: 0.5em;
    }
    """

    # --- 3. Convert Markdown to HTML ---
    try:
        md = MarkdownIt()
        html_fragment = md.render(md_content)
        print("Successfully converted Markdown to HTML fragment.")

        html_full = f"""
        <!DOCTYPE html>
        <html lang="he" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <title>{os.path.basename(pdf_file_path)}</title>
            <style>
                {css_style}
            </style>
        </head>
        <body>
            {html_fragment}
        </body>
        </html>
        """
    except Exception as e:
        print(f"Error converting Markdown to HTML: {e}")
        return

    # --- 4. Render HTML+CSS to PDF ---
    try:
        print("Rendering PDF... This might take a moment.")
        font_config = FontConfiguration() # FontConfiguration is used here
        css = CSS(string=css_style, font_config=font_config)
        html_doc = HTML(string=html_full, base_url=os.path.dirname(os.path.abspath(md_file_path)), encoding='utf-8')

        html_doc.write_pdf(
            pdf_file_path,
            stylesheets=[css],
            font_config=font_config # Pass the config here
        )
        print(f"Successfully created PDF: {pdf_file_path}")
    except Exception as e:
        print(f"Error rendering PDF with WeasyPrint: {e}")
        print("\nDebugging Tips:")
        print("- *** Did you download and install the 'Rubik' font from Google Fonts? ***")
        print("- Are WeasyPrint and its dependencies (Pango/Cairo/etc.) installed correctly?")
        print("- Check the console output for specific font errors (Pango/WeasyPrint).")
        print("See WeasyPrint installation guide: https://doc.weasyprint.org/en/stable/install.html")

# --- Main Execution Logic ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert a Markdown file to a styled PDF using Rubik font.')
    parser.add_argument('input_md_file', help='Path to the input Markdown file.')
    parser.add_argument('-o', '--output', dest='output_pdf_file',
                        help='Path for the output PDF file (optional). Defaults to input filename with .pdf extension.')

    args = parser.parse_args()

    if args.output_pdf_file:
        output_file = args.output_pdf_file
    else:
        base_name, _ = os.path.splitext(args.input_md_file)
        output_file = base_name + ".pdf"

    abs_md_path = os.path.abspath(args.input_md_file)
    convert_md_to_pdf(abs_md_path, output_file)