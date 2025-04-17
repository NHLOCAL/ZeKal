import argparse
import os
import sys
import shutil # For copying files
from markdown_it import MarkdownIt
from bs4 import BeautifulSoup

# --- Determine Project Root ---
# Assumes the script is located in project_root/scripts/
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# --- Default Paths ---
DEFAULT_INPUT_MD = os.path.join(PROJECT_ROOT, 'src', 'content', 'book.md')
DEFAULT_OUTPUT_HTML = os.path.join(PROJECT_ROOT, 'output', 'book.html')
DEFAULT_CSS_SOURCE = os.path.join(PROJECT_ROOT, 'src', 'assets', 'css', 'book_style.css')


def get_front_matter_html(book_title="הקופסה הפתוחה: להכיר את המוח שמאחורי המסך", author_name="nhlocal"):
    """Generates the HTML for the front matter pages (Cover, Blank, Author, Blank)."""
    # (Function content remains the same as before)
    main_cover_title = book_title
    sub_cover_title = ""
    if ':' in book_title:
        parts = book_title.split(':', 1)
        main_cover_title = parts[0].strip()
        sub_cover_title = parts[1].strip()

    front_matter = f"""
<!-- Cover Page -->
<div class="page cover-page">
  <div class="cover-content">
     <span class="cover-title">{main_cover_title}</span>
     {'<span class="cover-subtitle">' + sub_cover_title + '</span>' if sub_cover_title else ''}
  </div>
</div>

<!-- Blank Page -->
<div class="page blank-page"></div>

<!-- Author Info Page -->
<div class="page author-page">
  <div class="author-content">
    <h2>על המחבר</h2>
    <p class="author-name">{author_name}</p>
    <p>GitHub: <a href="https://github.com/NHLOCAL" target="_blank" rel="noopener noreferrer">https://github.com/NHLOCAL</a></p>
    <p>אתר פרויקטים: <a href="https://nhlocal.github.io" target="_blank" rel="noopener noreferrer">https://nhlocal.github.io</a></p>
    <p>דוא"ל: <a href="mailto:nh.local11@gmail.com">nh.local11@gmail.com</a></p>
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
    # (Function content remains the same as before)
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

    Args:
        md_file_path (str): Path to the input Markdown file.
        html_file_path (str): Path for the output HTML file.
        css_source_path (str): Path to the source CSS file to copy.
    """
    print(f"--- Starting HTML Book Generation ---")
    print(f"Project Root:   {PROJECT_ROOT}")
    print(f"Input Markdown: {md_file_path}")
    print(f"Source CSS:     {css_source_path}")
    print(f"Output HTML:    {html_file_path}")

    output_dir = os.path.dirname(html_file_path)
    css_file_name = os.path.basename(css_source_path) # e.g., "book_style.css"
    css_dest_path = os.path.join(output_dir, css_file_name)

    print(f"Output Dir:     {output_dir}")
    print(f"CSS Filename:   {css_file_name}")
    print(f"CSS Dest Path:  {css_dest_path}")


    if not os.path.exists(md_file_path):
        print(f"*** ERROR: Input Markdown file not found: '{md_file_path}' ***")
        return False

    if not os.path.exists(css_source_path):
        print(f"*** WARNING: Source CSS file not found: '{css_source_path}'. HTML will be generated without styling. ***")
        # Decide if you want to continue or fail here. Continuing for now.
        # return False

    # --- 1. Create Output Directory ---
    try:
        os.makedirs(output_dir, exist_ok=True)
        print(f"Ensured output directory exists: {output_dir}")
    except Exception as e:
        print(f"*** ERROR: Could not create output directory '{output_dir}': {e} ***")
        return False

    # --- 2. Copy CSS File ---
    if os.path.exists(css_source_path):
        try:
            shutil.copy2(css_source_path, css_dest_path) # copy2 preserves metadata
            print(f"Successfully copied CSS to '{css_dest_path}'")
        except Exception as e:
            print(f"*** ERROR: Could not copy CSS from '{css_source_path}' to '{css_dest_path}': {e} ***")
            return False # Fail if CSS copy fails

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

    # --- 6. Generate Front Matter (Always included) ---
    book_main_title = "הקופסה הפתוחה: להכיר את המוח שמאחורי המסך" # Default book title
    static_preamble = get_front_matter_html(book_title=book_main_title, author_name="nhlocal")
    # Use the book title for the HTML <title> tag
    page_title = book_main_title.split(':')[0].strip()

    # --- 7. Construct Full HTML Document ---
    lang = "he"
    direction = "rtl"

    # Link to the *local* CSS file name
    html_full = f"""<!DOCTYPE html>
<html lang="{lang}" dir="{direction}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <link rel="stylesheet" href="{css_file_name}">
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
        print(f"HTML links to '{css_file_name}' (copied to the same directory).")
        return True
    except Exception as e:
        print(f"*** ERROR writing HTML file: {e} ***")
        return False

# --- Main Execution Logic ---
if __name__ == "__main__":
    # --- Dependency Check ---
    # (Keep the dependency checks for bs4, markdown_it, lxml as before)
    try: import bs4
    except ImportError: print("Dependency Error: `pip install beautifulsoup4 lxml`"); sys.exit(1)
    try: import markdown_it
    except ImportError: print("Dependency Error: `pip install markdown-it-py`"); sys.exit(1)
    try: import lxml
    except ImportError: print("Dependency Error: `pip install lxml`"); sys.exit(1)


    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(
        description='Convert Markdown book content (src/content/book.md) to a styled HTML file (output/book.html) with front matter, copying CSS.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter # Show defaults in help
    )
    # Input is now optional positional, defaulting to the standard location
    parser.add_argument('input_md_file', nargs='?', default=DEFAULT_INPUT_MD,
                        help='Path to the input Markdown file.')
    parser.add_argument('-o', '--output', dest='output_html_file', default=DEFAULT_OUTPUT_HTML,
                        help='Path for the output HTML file.')
    # We don't need an argument for CSS source anymore, using the default
    # parser.add_argument('--css-source', default=DEFAULT_CSS_SOURCE, help='Path to the source CSS file.')

    args = parser.parse_args()

    # Use the fixed default CSS source path
    css_source_to_use = DEFAULT_CSS_SOURCE

    # --- Run Conversion ---
    success = generate_book_html(
        md_file_path=args.input_md_file,
        html_file_path=args.output_html_file,
        css_source_path=css_source_to_use
    )

    if not success:
        sys.exit(1) # Exit with error code if generation failed