# scripts/generate_html.py
import argparse
import os
import sys
from markdown_it import MarkdownIt
from bs4 import BeautifulSoup

# --- Determine Project Root ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# --- Default Paths ---
DEFAULT_INPUT_MD = os.path.join(PROJECT_ROOT, 'src', 'content', 'book.md')
DEFAULT_OUTPUT_HTML = os.path.join(PROJECT_ROOT, 'output', 'book.html')
DEFAULT_CSS_SOURCE = os.path.join(PROJECT_ROOT, 'src', 'assets', 'css', 'book_style.css')


def get_front_matter_html(book_title="הקופסה הפתוחה: להכיר את המוח שמאחורי המסך", author_name="nhlocal"):
    """Generates the HTML for the front matter pages (Cover, Blank, Author, Blank)."""

    main_cover_title = book_title
    sub_cover_title = ""
    if ':' in book_title:
        parts = book_title.split(':', 1)
        main_cover_title = parts[0].strip()
        sub_cover_title = parts[1].strip()

    # --- Author Page Structure with Sections ---
    front_matter = f"""
<!-- Cover Page -->
<div class="page cover-page">
  <div class="cover-content">
     <span class="cover-title">{main_cover_title}</span>
     {'<span class="cover-subtitle">' + sub_cover_title + '</span>' if sub_cover_title else ''}
     <span class="cover-author">{author_name}</span>
  </div>
</div>

<!-- Blank Page -->
<div class="page blank-page"></div>

<!-- Author Info / Colophon Page -->
<div class="page author-page">
  <div class="author-content">

    <div class="book-info-section">
      <h2 class="book-title-on-author-page">{book_title}</h2>
      <p class="author-name">{author_name}</p>
      <p class="version-info">מהדורה ראשונה | אפריל 2025</p>
    </div>

    <hr class="author-separator">

    <div class="contact-section">
      <p class="contact-info-heading">יצירת קשר ומידע נוסף:</p>
      <p class="contact-detail">GitHub: <a class="author-link" href="https://github.com/NHLOCAL" target="_blank" rel="noopener noreferrer">https://github.com/NHLOCAL</a></p>
      <p class="contact-detail">אתר פרויקטים: <a class="author-link" href="https://nhlocal.github.io" target="_blank" rel="noopener noreferrer">https://nhlocal.github.io</a></p>
      <p class="contact-detail">דוא"ל: <a class="author-link" href="mailto:nh.local11@gmail.com">nh.local11@gmail.com</a></p>
    </div>

    <hr class="author-separator">

    <div class="legal-section">
      <p class="rights-notice">כל הזכויות שמורות למחבר, {author_name} © 2025.</p>
      <p class="rights-notice">ניתן להפיץ ולשכפל בחופשיות תוך מתן קרדיט (ייחוס) למחבר המקורי.</p>
      <p class="disclaimer">תוכן הספר מובא כפי שהוא (AS IS). אין המחבר אחראי לכל נזק ישיר או עקיף שעלול להיגרם כתוצאה מהשימוש במידע המופיע בספר זה.</p>
    </div>

   </div>
</div>

<!-- Blank Page -->
<div class="page blank-page"></div>
"""
    return front_matter


def improve_html_structure(html_fragment):
    """
    Parses the HTML fragment and restructures H1 tags for title/subtitle spans.
    """
    print("Improving HTML structure (Processing H1 titles)...")
    soup = BeautifulSoup(html_fragment, 'lxml')
    h1_tags = soup.find_all('h1')

    for h1 in h1_tags:
        original_text = h1.get_text(strip=True)
        colon_index = original_text.find(':')
        h1.clear() # Clear existing content

        if colon_index > 0:
            main_title_text = original_text[:colon_index].strip()
            sub_title_text = original_text[colon_index+1:].strip()
            main_span = soup.new_tag('span', attrs={'class': 'main-title'})
            main_span.string = main_title_text
            sub_span = soup.new_tag('span', attrs={'class': 'sub-title'})
            sub_span.string = sub_title_text
            h1.append(main_span)
            h1.append(sub_span)
        else:
            full_span = soup.new_tag('span', attrs={'class': 'main-title full-title'})
            full_span.string = original_text
            h1.append(full_span)
    return str(soup)


def generate_book_html(md_file_path, html_file_path, css_source_path):
    """
    Converts Markdown to a full HTML book file with front matter
    and *embeds* the CSS styles directly within the HTML head.
    """
    print(f"--- Starting HTML Book Generation (with Embedded CSS) ---")
    print(f"Project Root:   {PROJECT_ROOT}")
    print(f"Input Markdown: {md_file_path}")
    print(f"Source CSS:     {css_source_path}")
    print(f"Output HTML:    {html_file_path}")

    output_dir = os.path.dirname(html_file_path)
    print(f"Output Dir:     {output_dir}")

    if not os.path.exists(md_file_path):
        print(f"*** ERROR: Input Markdown file not found: '{md_file_path}' ***")
        return False

    if not os.path.exists(css_source_path):
        print(f"*** WARNING: Source CSS file not found: '{css_source_path}'. HTML will be generated without styles. ***")

    # --- 1. Create Output Directory ---
    try:
        os.makedirs(output_dir, exist_ok=True)
        print(f"Ensured output directory exists: {output_dir}")
    except Exception as e:
        print(f"*** ERROR: Could not create output directory '{output_dir}': {e} ***")
        return False

    # --- 2. Read CSS Content (Instead of Copying) ---
    css_content = ""
    if os.path.exists(css_source_path):
        try:
            with open(css_source_path, 'r', encoding='utf-8') as f_css:
                css_content = f_css.read()
            print(f"Successfully read CSS content from '{css_source_path}' for embedding.")
        except Exception as e:
            print(f"*** WARNING: Could not read CSS file '{css_source_path}': {e}. Proceeding without embedded styles. ***")
            css_content = "/* CSS could not be loaded */"

    # --- 3. Read Markdown Content ---
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        print("Successfully read Markdown file.")
    except Exception as e:
        print(f"*** ERROR reading Markdown file: {e} ***")
        return False

    # --- 4. Convert Markdown to HTML Fragment ---
    try:
        md = MarkdownIt('commonmark', {'breaks': False, 'html': True, 'linkify': True, 'typographer': True}).enable(['table', 'strikethrough'])
        html_fragment_raw = md.render(md_content)
        print("Successfully converted Markdown to HTML fragment.")
    except Exception as e:
        print(f"*** ERROR during Markdown parsing: {e} ***")
        return False

    # --- 5. Improve HTML Structure (Split H1 on Markdown Content Only) ---
    try:
        html_fragment_improved = improve_html_structure(html_fragment_raw)
    except Exception as e:
        print(f"*** ERROR improving HTML structure: {e}. Using raw fragment. ***")
        html_fragment_improved = html_fragment_raw # Fallback

    # --- 6. Generate Front Matter ---
    book_main_title = "הקופסה הפתוחה: להכיר את המוח שמאחורי המסך"
    static_preamble = get_front_matter_html(book_title=book_main_title, author_name="nhlocal")
    page_title = book_main_title.split(':')[0].strip()

    # --- 7. Construct Full HTML Document (Embedding CSS) ---
    lang = "he"
    direction = "rtl"

    html_full = f"""<!DOCTYPE html>
<html lang="{lang}" dir="{direction}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <style>
{css_content}
    </style>
</head>
<body>

{static_preamble}
<div class="main-content">
{html_fragment_improved}
</div>

</body>
</html>
"""

    # --- 8. Write HTML to File ---
    try:
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(html_full)
        print(f"Successfully created HTML file with embedded styles: {html_file_path}")
        return True
    except Exception as e:
        print(f"*** ERROR writing HTML file: {e} ***")
        return False

# --- Main Execution Logic ---
if __name__ == "__main__":
    # --- Dependency Check ---
    try: import bs4
    except ImportError: print("Dependency Error: `pip install beautifulsoup4 lxml`"); sys.exit(1)
    try: import markdown_it
    except ImportError: print("Dependency Error: `pip install markdown-it-py`"); sys.exit(1)
    try: import lxml
    except ImportError: print("Dependency Error: `pip install lxml`"); sys.exit(1)

    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(
        description='Convert Markdown book content to a single HTML file with embedded styles and front matter.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('input_md_file', nargs='?', default=DEFAULT_INPUT_MD,
                        help='Path to the input Markdown file.')
    parser.add_argument('-o', '--output', dest='output_html_file', default=DEFAULT_OUTPUT_HTML,
                        help='Path for the output HTML file.')

    args = parser.parse_args()
    css_source_to_use = DEFAULT_CSS_SOURCE # Still needed to know *where* to read CSS from

    # --- Run Conversion ---
    success = generate_book_html(
        md_file_path=args.input_md_file,
        html_file_path=args.output_html_file,
        css_source_path=css_source_to_use
    )

    if not success:
        sys.exit(1)