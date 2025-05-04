# scripts/generate_html.py
import argparse
import os
import sys
import shutil
from markdown_it import MarkdownIt
from bs4 import BeautifulSoup, NavigableString # <--- החזרת NavigableString

# --- קוד קודם ללא שינוי... ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DEFAULT_INPUT_MD = os.path.join(PROJECT_ROOT, 'src', 'content', 'book.md')
DEFAULT_OUTPUT_HTML = os.path.join(PROJECT_ROOT, 'output', 'book.html')
DEFAULT_CSS_SOURCE = os.path.join(PROJECT_ROOT, 'src', 'assets', 'css', 'book_style.css')
DEFAULT_COVER_IMAGE_SOURCE = os.path.join(PROJECT_ROOT, 'src', 'assets', 'images', 'cover.png')
BOOK_TITLE_FOR_HEADER = "הקופסה הפתוחה"

def get_front_matter_html(book_title="הקופסה הפתוחה: להבין את המוח שמאחורי הבינה", author_name="nhlocal"):
    """Generates the HTML for the front matter pages (Image Cover, Blank, Author)."""
    # --- קוד זה ללא שינוי מהגרסה הקודמת ---
    author_page_html = f"""
<!-- Author Info / Colophon Page -->
<div class="page author-page">
  <div class="author-content">
    <div class="book-info-section">
      <h2 class="book-title-on-author-page">{book_title}</h2>
      <p class="author-name">{author_name}</p>
      <p class="version-info">מהדורת בדיקה | אפריל 2025</p>
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
    """

    front_matter = f"""
<!-- Cover Page with Image -->
<div class="page cover-image-page">
  <img src="cover.png" alt="Book Cover: {book_title}" class="cover-image">
</div>

<!-- Blank Page -->
<div class="page blank-page"></div>

{author_page_html}
"""
    return front_matter


def improve_html_structure(html_fragment):
    """
    Parses the HTML fragment and restructures H1 tags for title/subtitle spans,
    and adds a class for CSS targeting.
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

        # Add a class to H1 to help CSS target chapter start pages
        current_classes = h1.get('class', [])
        if 'chapter-start-heading' not in current_classes:
            current_classes.append('chapter-start-heading')
        h1['class'] = current_classes
        print(f"Processed H1: {original_text[:30]}... Added class 'chapter-start-heading'.")

    return str(soup)


# --- החזרת הפונקציה להוספת דף ריק ---
def add_blank_pages_before_chapters(html_content):
    """
    Parses the main content HTML and inserts a blank page before each H1.
    """
    print("Adding blank pages before chapter starts (H1 tags)...")
    soup = BeautifulSoup(html_content, 'lxml')
    h1_tags = soup.find_all('h1', class_='chapter-start-heading')

    if not h1_tags:
        print("No H1 tags found in main content to add blank pages before.")
        return str(soup)

    for h1 in h1_tags:
        blank_page_div = soup.new_tag('div', attrs={'class': 'page blank-page'})
        h1.insert_before(blank_page_div)
        h1.insert_before(NavigableString("\n")) # למען הסדר בקוד ה-HTML
        print(f"Inserted blank page before H1: {h1.get_text(strip=True)[:30]}...")

    return str(soup)


def generate_book_html(md_file_path, html_file_path, css_source_path, cover_image_source_path):
    """
    Converts Markdown to a full HTML book file with image cover, front matter,
    embedded CSS, page numbers/headers, and blank pages before chapters (via Python).
    """
    print(f"--- Starting HTML Book Generation (Python blank pages, simplified H1 CSS) ---")
    # --- לוגיקה קודמת ללא שינוי עד שלב 7 ---
    print(f"Project Root:   {PROJECT_ROOT}")
    print(f"Input Markdown: {md_file_path}")
    print(f"Source CSS:     {css_source_path}")
    print(f"Source Cover:   {cover_image_source_path}")
    print(f"Output HTML:    {html_file_path}")

    output_dir = os.path.dirname(html_file_path)
    cover_image_filename = os.path.basename(cover_image_source_path)
    cover_image_dest_path = os.path.join(output_dir, cover_image_filename)

    print(f"Output Dir:     {output_dir}")
    print(f"Cover Dest:     {cover_image_dest_path}")

    # --- בדיקת קבצים, יצירת תיקייה, העתקת תמונה, קריאת CSS, קריאת MD (ללא שינוי) ---
    if not os.path.exists(md_file_path): print(f"ERROR: MD not found: '{md_file_path}'"); return False
    if not os.path.exists(css_source_path): print(f"WARNING: CSS not found: '{css_source_path}'")
    if not os.path.exists(cover_image_source_path): print(f"WARNING: Cover not found: '{cover_image_source_path}'")
    try: os.makedirs(output_dir, exist_ok=True); print(f"Ensured output dir: {output_dir}")
    except Exception as e: print(f"ERROR creating dir '{output_dir}': {e}"); return False
    if os.path.exists(cover_image_source_path):
        try: shutil.copy2(cover_image_source_path, cover_image_dest_path); print(f"Copied cover: '{cover_image_dest_path}'")
        except Exception as e: print(f"WARNING copying cover: {e}")
    css_content = ""
    if os.path.exists(css_source_path):
        try:
            with open(css_source_path, 'r', encoding='utf-8') as f_css: css_content = f_css.read(); print("Read CSS.")
        except Exception as e: print(f"WARNING reading CSS: {e}"); css_content = "/* CSS load failed */"
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f: md_content = f.read(); print("Read Markdown.")
    except Exception as e: print(f"ERROR reading MD: {e}"); return False

    # --- 5. Convert Markdown to HTML Fragment ---
    try:
        md = MarkdownIt('commonmark', {'breaks': False, 'html': True, 'linkify': True, 'typographer': True}).enable(['table', 'strikethrough'])
        html_fragment_raw = md.render(md_content)
        print("Converted Markdown to HTML fragment.")
    except Exception as e:
        print(f"*** ERROR during Markdown parsing: {e} ***")
        return False

    # --- 6. Improve H1 Structure (Adds class 'chapter-start-heading') ---
    try:
        html_fragment_improved_h1 = improve_html_structure(html_fragment_raw)
    except Exception as e:
        print(f"*** ERROR improving HTML structure: {e}. Using raw fragment. ***")
        html_fragment_improved_h1 = html_fragment_raw

    # --- 7. Add Blank Pages Before Chapters (via Python) ---
    try:
        html_fragment_final = add_blank_pages_before_chapters(html_fragment_improved_h1) # <--- החזרת הקריאה
    except Exception as e:
        print(f"*** ERROR adding blank pages before chapters: {e}. Using fragment without added blanks. ***")
        html_fragment_final = html_fragment_improved_h1


    # --- 8. Generate Front Matter ---
    book_main_title = "הקופסה הפתוחה: להבין את המוח שמאחורי הבינה"
    static_preamble = get_front_matter_html(book_title=book_main_title, author_name="nhlocal")
    page_title_short = book_main_title.split(':')[0].strip()

    # --- 9. Construct Full HTML Document (Embedding CSS) ---
    lang = "he"
    direction = "rtl"
    css_content_with_vars = f":root {{ --book-title-header: '{BOOK_TITLE_FOR_HEADER}'; }}\n\n{css_content}"

    html_full = f"""<!DOCTYPE html>
<html lang="{lang}" dir="{direction}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title_short}</title>
    <style>
{css_content_with_vars}
    </style>
</head>
<body>

{static_preamble}
<div class="main-content">
{html_fragment_final}
</div>

</body>
</html>
"""

    # --- 10. Write HTML to File ---
    try:
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(html_full)
        print(f"Successfully created HTML file (Python blank pages, simplified H1): {html_file_path}")
        print(f"Check '{cover_image_filename}' in the output directory.")
        return True
    except Exception as e:
        print(f"*** ERROR writing HTML file: {e} ***")
        return False

# --- Main Execution Logic (ללא שינוי מהגרסה הקודמת) ---
if __name__ == "__main__":
    try: import bs4
    except ImportError: print("Dependency Error: `pip install beautifulsoup4 lxml`"); sys.exit(1)
    try: import markdown_it
    except ImportError: print("Dependency Error: `pip install markdown-it-py`"); sys.exit(1)
    try: import lxml
    except ImportError: print("Dependency Error: `pip install lxml`"); sys.exit(1)
    try: import shutil
    except ImportError: print("Standard library 'shutil' not found? This is unexpected."); sys.exit(1)

    parser = argparse.ArgumentParser(
        description='Convert Markdown book content to a single HTML file with enhancements.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('input_md_file', nargs='?', default=DEFAULT_INPUT_MD,
                        help='Path to the input Markdown file.')
    parser.add_argument('-o', '--output', dest='output_html_file', default=DEFAULT_OUTPUT_HTML,
                        help='Path for the output HTML file.')
    parser.add_argument('--cover-image', dest='cover_image', default=DEFAULT_COVER_IMAGE_SOURCE,
                        help='Path to the cover image file.')

    args = parser.parse_args()
    css_source_to_use = DEFAULT_CSS_SOURCE
    cover_image_to_use = args.cover_image

    success = generate_book_html(
        md_file_path=args.input_md_file,
        html_file_path=args.output_html_file,
        css_source_path=css_source_to_use,
        cover_image_source_path=cover_image_to_use
    )

    if not success:
        sys.exit(1)
