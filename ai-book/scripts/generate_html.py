import argparse
import os
from markdown_it import MarkdownIt
# <<< תלות חדשה >>>
from bs4 import BeautifulSoup
import shutil # For checking dependency

def get_front_matter_html(book_title="הקופסה הפתוחה: להכיר את המוח שמאחורי המסך", author_name="nhlocal"):
    """Generates the HTML for the front matter pages (Cover, Blank, Author, Blank)."""

    # Split book title if needed for cover styling
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
    Parses the HTML fragment and restructures H1 tags to split titles based on the first ':'.
    Also wraps the original H1 text in spans for consistent targeting, even if no colon is found.

    Args:
        html_fragment (str): The raw HTML fragment from markdown-it.

    Returns:
        str: The modified HTML fragment with restructured H1 tags.
    """
    print("Improving HTML structure (Processing H1 titles)...")
    soup = BeautifulSoup(html_fragment, 'lxml')
    h1_tags = soup.find_all('h1')

    for h1 in h1_tags:
        original_text = h1.get_text(strip=True)
        colon_index = original_text.find(':')

        # Clear the original content of H1
        h1.clear()

        if colon_index > 0:
            # Split text if colon exists and is not at the start
            main_title_text = original_text[:colon_index].strip()
            sub_title_text = original_text[colon_index+1:].strip()

            # Create new spans for main and sub titles
            main_span = soup.new_tag('span', attrs={'class': 'main-title'})
            main_span.string = main_title_text

            sub_span = soup.new_tag('span', attrs={'class': 'sub-title'})
            sub_span.string = sub_title_text

            h1.append(main_span)
            h1.append(sub_span)
        else:
            # If no colon or it's at the start, wrap the whole text in a single span
            # This helps apply consistent styling (like centering) defined on the spans
            full_span = soup.new_tag('span', attrs={'class': 'main-title full-title'}) # Use main-title class plus specific one
            full_span.string = original_text
            h1.append(full_span)

    return str(soup)


def convert_md_to_linked_html(md_file_path, html_file_path, css_file_name="book_style.css", add_front_matter=False):
    """
    Converts Markdown to an HTML file linked to an external CSS stylesheet.
    Includes H1 title splitting and optional front matter pages.

    Args:
        md_file_path (str): Path to the input Markdown file.
        html_file_path (str): Path for the output HTML file.
        css_file_name (str): Name of the external CSS file to link.
        add_front_matter (bool): Whether to prepend cover/author pages.
    """
    print(f"--- Starting Advanced HTML Conversion (Linking External CSS) ---")
    print(f"Input Markdown: {md_file_path}")
    print(f"Output HTML:    {html_file_path}")
    print(f"Linking CSS:    {css_file_name}")
    print(f"Add Front Matter: {'Yes' if add_front_matter else 'No'}")

    if not os.path.exists(md_file_path):
        print(f"*** ERROR: Input Markdown file not found: '{md_file_path}' ***")
        return False

    # --- 1. Read Markdown Content ---
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        print("Successfully read Markdown file.")
    except Exception as e:
        print(f"Error reading Markdown file: {e}")
        return False

    # --- 2. Convert Markdown to HTML Fragment ---
    try:
        md = MarkdownIt('commonmark', {'breaks': False, 'html': True, 'linkify': True, 'typographer': True}).enable(['table', 'strikethrough'])
        html_fragment_raw = md.render(md_content)
        print("Successfully converted Markdown to HTML fragment.")
    except Exception as e:
        print(f"Error during Markdown parsing: {e}")
        return False

    # --- 3. Improve HTML Structure (Split H1 on Markdown Content Only) ---
    try:
        html_fragment_improved = improve_html_structure(html_fragment_raw)
    except Exception as e:
        print(f"Error improving HTML structure with BeautifulSoup: {e}")
        print("Falling back to raw HTML fragment.")
        html_fragment_improved = html_fragment_raw # Fallback

    # --- 4. Generate Front Matter (Optional) ---
    static_preamble = ""
    page_title = os.path.basename(html_file_path).replace('.html', '') # Default title
    book_main_title = "הקופסה הפתוחה: להכיר את המוח שמאחורי המסך" # Define default book title

    if add_front_matter:
        static_preamble = get_front_matter_html(book_title=book_main_title, author_name="nhlocal")
        # Use the book title for the HTML <title> tag if front matter is added
        page_title = book_main_title.split(':')[0].strip() # Use main part of book title

    # --- 5. Construct Full HTML Document (Linking CSS) ---
    lang = "he"
    direction = "rtl"

    # Try to extract title from *original* H1 fragment for <title> tag *if* front matter isn't added
    if not add_front_matter:
        try:
            soup_title = BeautifulSoup(html_fragment_raw, 'lxml')
            first_h1 = soup_title.find('h1')
            if first_h1:
                page_title = first_h1.get_text(strip=True)
        except Exception: pass

    # <<< Link to external CSS file instead of embedding styles >>>
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
{html_fragment_improved}

</body>
</html>
"""

    # --- 6. Write HTML to File ---
    try:
        os.makedirs(os.path.dirname(html_file_path), exist_ok=True) # Ensure output directory exists
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(html_full)
        print(f"Successfully created HTML file linking to '{css_file_name}': {html_file_path}")
        print(f"IMPORTANT: Ensure the CSS file '{css_file_name}' exists in the same directory or provide the correct path.")
        return True
    except Exception as e:
        print(f"Error writing HTML file: {e}")
        return False

# --- Main Execution Logic ---
if __name__ == "__main__":
    # --- Dependency Check ---
    try:
        import bs4
    except ImportError:
        print("\n*** DEPENDENCY ERROR: 'beautifulsoup4' library not found. ***")
        print("Please install it using: pip install beautifulsoup4 lxml")
        exit()
    try:
        import markdown_it
    except ImportError:
         print("\n*** DEPENDENCY ERROR: 'markdown-it-py' library not found. ***")
         print("Please install it using: pip install markdown-it-py")
         exit()
    # Check for lxml parser too
    try:
        import lxml
    except ImportError:
        print("\n*** DEPENDENCY ERROR: 'lxml' library not found (used by BeautifulSoup). ***")
        print("Please install it using: pip install lxml")
        exit()


    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(description='Convert Markdown to enhanced HTML linking external CSS, with optional front matter.')
    parser.add_argument('input_md_file', help='Path to the input Markdown file.')
    parser.add_argument('-o', '--output', dest='output_html_file',
                        help='Path for the output HTML file (optional). Defaults to input filename with .html extension.')
    parser.add_argument('--css', dest='css_file', default='book_style.css',
                        help='Filename/path for the external CSS file to link (default: book_style.css).')
    parser.add_argument('-f', '--add-front-matter', action='store_true',
                        help='Add standard front matter (Cover, Author info, Blank pages).')


    args = parser.parse_args()

    # --- Determine Output HTML Path ---
    if args.output_html_file:
        output_file = args.output_html_file
    else:
        # Place output in the same directory as the input by default
        output_dir = os.path.dirname(args.input_md_file)
        base_name, _ = os.path.splitext(os.path.basename(args.input_md_file))
        output_file = os.path.join(output_dir, base_name + ".html")


    # --- Run Conversion ---
    convert_md_to_linked_html(
        md_file_path=args.input_md_file,
        html_file_path=output_file,
        css_file_name=args.css_file,
        add_front_matter=args.add_front_matter
    )