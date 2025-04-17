import argparse
import os
import sys
import shutil # For copying files
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
    """Generates the HTML for the front matter pages (Cover, Blank, Author/Info, Blank)."""

    # Split book title if needed for cover styling
    main_cover_title = book_title
    sub_cover_title = ""
    if ':' in book_title:
        parts = book_title.split(':', 1)
        main_cover_title = parts[0].strip()
        sub_cover_title = parts[1].strip()

    # Placeholder for edition - you might want to generate this dynamically later
    current_year = 2024
    current_month = "יוני" # Or dynamically get month name in Hebrew
    book_edition_text = f"מהדורה ראשונה | {current_month} {current_year}"

    front_matter = f"""
<!-- Cover Page -->
<div class="page cover-page">
  <div class="cover-content">
     <span class="cover-title">{main_cover_title}</span>
     {'<span class="cover-subtitle">' + sub_cover_title + '</span>' if sub_cover_title else ''}
     <p class="cover-author">{author_name}</p>
  </div>
</div>

<!-- Blank Page -->
<div class="page blank-page"></div>

<!-- Author/Info Page -->
<div class="page author-page">
  <div class="author-content">
    <h2>פרטי הספר והמחבר</h2>
    <p class="book-edition">{book_edition_text}</p>
    <p class="author-name">מאת: {author_name}</p>
    <div class="contact-info">
        <p>GitHub: <a href="https://github.com/NHLOCAL" target="_blank" rel="noopener noreferrer">github.com/NHLOCAL</a></p>
        <p>אתר פרויקטים: <a href="https://nhlocal.github.io" target="_blank" rel="noopener noreferrer">nhlocal.github.io</a></p>
        <p>דוא"ל: <a href="mailto:nh.local11@gmail.com">nh.local11@gmail.com</a></p>
    </div>
    <hr>
    <p class="rights-notice">כל הזכויות שמורות למחבר, {author_name}.</p>
    <p class="rights-notice">ניתן להפיץ ולשכפל בחופשיות תוך מתן קרדיט (ייחוס) למחבר המקורי.</p>
    <p class="disclaimer">תוכן הספר מובא כפי שהוא (AS IS). אין המחבר אחראי לכל נזק ישיר או עקיף שעלול להיגרם כתוצאה מהשימוש במידע המופיע בספר זה.</p>
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
    # (Function content remains the same)
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
    Converts Markdown to a full HTML book file with front matter,
    copies the CSS file, and links it locally.
    """
    # (Function logic remains largely the same, only the final HTML string construction changes slightly)
    print(f"--- Starting HTML Book Generation ---")
    # ... (rest of the initial checks and setup) ...

    output_dir = os.path.dirname(html_file_path)
    css_file_name = os.path.basename(css_source_path)
    css_dest_path = os.path.join(output_dir, css_file_name)

    print(f"Output Dir:     {output_dir}")
    print(f"CSS Filename:   {css_file_name}")
    print(f"CSS Dest Path:  {css_dest_path}")


    if not os.path.exists(md_file_path):
        print(f"*** ERROR: Input Markdown file not found: '{md_file_path}' ***")
        return False
    # ... (rest of the checks, directory creation, css copy) ...

    if os.path.exists(css_source_path):
        try:
            shutil.copy2(css_source_path, css_dest_path)
            print(f"Successfully copied CSS to '{css_dest_path}'")
        except Exception as e:
            print(f"*** ERROR: Could not copy CSS: {e} ***")
            return False
    else:
         print(f"*** WARNING: Source CSS file not found: '{css_source_path}'. HTML generated without styling link. ***")
         css_file_name = None # Prevent linking if CSS wasn't found/copied

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

    # --- 5. Improve HTML Structure (Split H1) ---
    try:
        html_fragment_improved = improve_html_structure(html_fragment_raw)
    except Exception as e:
        print(f"*** ERROR improving HTML structure: {e}. Using raw fragment. ***")
        html_fragment_improved = html_fragment_raw

    # --- 6. Generate Front Matter ---
    book_main_title = "הקופסה הפתוחה: להכיר את המוח שמאחורי המסך"
    static_preamble = get_front_matter_html(book_title=book_main_title, author_name="nhlocal")
    page_title = book_main_title.split(':')[0].strip()

    # --- 7. Construct Full HTML Document ---
    lang = "he"
    direction = "rtl"

    # Conditionally add the CSS link tag
    css_link_tag = f'<link rel="stylesheet" href="{css_file_name}">' if css_file_name else "<!-- CSS file not found or not copied -->"

    html_full = f"""<!DOCTYPE html>
<html lang="{lang}" dir="{direction}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    {css_link_tag}
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
        print(f"Successfully created HTML file: {html_file_path}")
        if css_file_name:
            print(f"HTML links to '{css_file_name}' (copied to the same directory).")
        return True
    except Exception as e:
        print(f"*** ERROR writing HTML file: {e} ***")
        return False

# --- Main Execution Logic ---
if __name__ == "__main__":
    # (Dependency Checks remain the same)
    try: import bs4
    except ImportError: print("Dependency Error: `pip install beautifulsoup4 lxml`"); sys.exit(1)
    try: import markdown_it
    except ImportError: print("Dependency Error: `pip install markdown-it-py`"); sys.exit(1)
    try: import lxml
    except ImportError: print("Dependency Error: `pip install lxml`"); sys.exit(1)

    # (Argument Parsing remains the same)
    parser = argparse.ArgumentParser(
        description='Convert Markdown book content to a styled HTML file with front matter, copying CSS.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('input_md_file', nargs='?', default=DEFAULT_INPUT_MD,
                        help='Path to the input Markdown file.')
    parser.add_argument('-o', '--output', dest='output_html_file', default=DEFAULT_OUTPUT_HTML,
                        help='Path for the output HTML file.')

    args = parser.parse_args()
    css_source_to_use = DEFAULT_CSS_SOURCE

    # --- Run Conversion ---
    success = generate_book_html(
        md_file_path=args.input_md_file,
        html_file_path=args.output_html_file,
        css_source_path=css_source_to_use
    )

    if not success:
        sys.exit(1)