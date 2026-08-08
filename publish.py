import os
import re
import sys
import subprocess

def generate_notes_html(title, category, snippet, md_content, slug):
    # Convert markdown to basic HTML structures
    html_lines = []
    paragraphs = md_content.strip().split("\n\n")
    
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        # Headers
        if p.startswith("## "):
            html_lines.append(f"    <h2>{p[3:]}</h2>")
        elif p.startswith("### "):
            html_lines.append(f"    <h3>{p[4:]}</h3>")
        # Bullet list
        elif p.startswith("- ") or p.startswith("* "):
            list_items = []
            for line in p.split("\n"):
                line = line.strip()
                if line.startswith("- ") or line.startswith("* "):
                    line_content = line[2:]
                    line_content = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", line_content)
                    list_items.append(f"        <li>{line_content}</li>")
            html_lines.append("    <ul>\n" + "\n".join(list_items) + "\n    </ul>")
        # Paragraph
        else:
            p_content = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", p)
            p_content = p_content.replace("\n", "<br>")
            html_lines.append(f"    <p>{p_content}</p>")

    html_body = "\n".join(html_lines)

    template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{title}: Technical Notes</title>
    <style>
    @page {{
        size: A4;
        margin: 2cm;
        @bottom-right {{
            content: "Page " counter(page) " of " counter(pages);
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            font-size: 9pt;
            color: #666;
        }}
    }}
    body {{
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #24292e;
        line-height: 1.6;
        max-width: 900px;
        margin: 0 auto;
        padding: 40px 20px;
        background-color: #ffffff;
    }}
    h1, h2, h3, h4 {{
        color: #111;
        font-weight: 600;
        margin-top: 1.5em;
        margin-bottom: 0.5em;
        border-bottom: 1px solid #eaecef;
        padding-bottom: 0.3em;
    }}
    h1 {{ font-size: 26pt; color: #7C5CFF; border-bottom: 2px solid #7C5CFF; }}
    h2 {{ font-size: 20pt; color: #333; }}
    h3 {{ font-size: 15pt; border-bottom: none; color: #555; }}
    a {{ color: #7C5CFF; text-decoration: none; }}
    pre {{
        background-color: #f6f8fa;
        border-radius: 6px;
        padding: 16px;
        overflow: auto;
        font-family: 'Courier New', Courier, monospace;
        font-size: 9.5pt;
        border: 1px solid #e1e4e8;
    }}
    code {{
        font-family: 'Courier New', Courier, monospace;
        background-color: #f6f8fa;
        padding: 0.2em 0.4em;
        border-radius: 3px;
        font-size: 90%;
    }}
    pre code {{
        background-color: transparent;
        padding: 0;
    }}
    table {{
        border-collapse: collapse;
        width: 100%;
        margin: 20px 0;
    }}
    th, td {{
        border: 1px solid #dfe2e5;
        padding: 10px 14px;
        text-align: left;
    }}
    th {{
        background-color: #f6f8fa;
        font-weight: 600;
    }}
    tr:nth-child(2n) {{
        background-color: #f8f9fa;
    }}
    blockquote {{
        margin: 0;
        padding: 0 1em;
        color: #6a737d;
        border-left: 0.25em solid #dfe2e5;
    }}
    .callout {{
        margin: 20px 0;
        padding: 15px;
        border-radius: 6px;
        border-left: 5px solid #ccc;
    }}
    .callout-title {{
        font-weight: bold;
        margin-bottom: 8px;
        font-size: 11pt;
    }}
    .callout-important {{ background-color: #f4f0ff; border-left-color: #7C5CFF; color: #7C5CFF; }}
    .callout-important .callout-body {{ color: #24292e; }}
    .callout-warning {{ background-color: #fffbdd; border-left-color: #d73a49; color: #d73a49; }}
    .callout-warning .callout-body {{ color: #24292e; }}
    .callout-tip {{ background-color: #e6ffed; border-left-color: #28a745; color: #28a745; }}
    .callout-tip .callout-body {{ color: #24292e; }}
    .callout-note {{ background-color: #f6f8fa; border-left-color: #6a737d; color: #6a737d; }}
    .meta-info {{
        font-size: 10pt;
        color: #6a737d;
        margin-top: -10px;
        margin-bottom: 30px;
    }}
    </style>
</head>
<body>

    <h1>{title}</h1>
    <div class="meta-info">Compiled by Kanchi Gupta · Technical Study Series</div>

    <div class="callout callout-important">
        <div class="callout-title">Core Theme</div>
        <div class="callout-body">
            {snippet}
        </div>
    </div>

{html_body}

    <div style="margin-top: 50px; border-top: 1px solid #eaecef; padding-top: 20px; text-align: center;">
        <a href="../index.html">← Back to Homepage</a>
    </div>

</body>
</html>
"""
    return template

def copy_to_macos_clipboard(text):
    try:
        # Use pbcopy on macOS to inject text directly to system clipboard
        process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        process.communicate(text.encode('utf-8'))
        return True
    except Exception as e:
        print(f"Error copying to clipboard: {e}")
        return False

def open_medium_draft_page():
    try:
        # Open Google Chrome directly to Medium draft page
        subprocess.run(['open', '-a', 'Google Chrome', 'https://medium.com/new-story'])
        print("[Medium] SUCCESS! Google Chrome has opened your Medium Story Draft Creator.")
        return True
    except Exception as e:
        print(f"Error opening Chrome: {e}")
        return False

def update_sitemap(slug_url):
    sitemap_path = "/Users/kanchigupta/Desktop/AI_PROJECTS/handhold/sitemap.xml"
    if not os.path.exists(sitemap_path):
        return False
    with open(sitemap_path, "r", encoding="utf-8") as f:
        data = f.read()
    
    full_url = f"https://kanchiguptairs.com/{slug_url}"
    if full_url in data:
        return True
        
    new_url_entry = f"""  <url>
    <loc>{full_url}</loc>
    <lastmod>2026-08-08</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>
</urlset>"""
    data = data.replace("</urlset>", new_url_entry)
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(data)
    print("Success: Updated sitemap.xml with the new URL!")
    return True

def publish():
    path = '/Users/kanchigupta/Desktop/AI_PROJECTS/handhold'
    draft_path = os.path.join(path, 'draft.md')
    index_path = os.path.join(path, 'index.html')

    if not os.path.exists(draft_path):
        print("Error: draft.md file not found in the project root.")
        return False

    with open(draft_path, 'r', encoding='utf-8') as f:
        content = f.read()

    frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not frontmatter_match:
        print("Error: draft.md is missing YAML frontmatter.")
        return False

    frontmatter_raw = frontmatter_match.group(1)
    md_content = frontmatter_match.group(2)

    title = re.search(r"^title:\s*(.*?)$", frontmatter_raw, re.MULTILINE).group(1).strip()
    category = re.search(r"^category:\s*(.*?)$", frontmatter_raw, re.MULTILINE).group(1).strip()
    snippet = re.search(r"^snippet:\s*(.*?)$", frontmatter_raw, re.MULTILINE).group(1).strip()

    slug = title.replace(":", "").replace(" ", "_").replace("&", "and").strip()
    slug_url = f"notes/Master_{slug}.html"
    note_file_path = os.path.join(path, slug_url)

    print(f"Publishing Article: {title}")
    
    html_content = generate_notes_html(title, category, snippet, md_content, slug)

    with open(note_file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("Success: Generated standalone HTML notes page.")

    # macOS Clipboard & Chrome Auto-Opening Pipeline (No Token Required!)
    clipboard_text = f"{title}\n\nOriginally compiled by Kanchi Gupta · Technical Study Series\n\n{md_content}"
    if copy_to_macos_clipboard(clipboard_text):
        print("Success: Copied entire article content and title to your macOS Clipboard.")
        open_medium_draft_page()
        print("[Medium] Your article is on your clipboard. Simply press Cmd+V (Paste) in your newly opened Medium editor!")

    # Update sitemap.xml automatically!
    update_sitemap(slug_url)

    # Update index.html
    with open(index_path, 'r', encoding='utf-8') as f:
        index_content = f.read()

    if slug_url in index_content:
        print("Note already linked on index.html. Skipping link insertion.")
    else:
        new_card = f"""        <!-- Note Card: {title} -->
        <div class="resource-card">
          <span class="resource-category">{category}</span>
          <h3>{title}</h3>
          <p>{snippet}</p>
          <div style="display: flex; gap: 1rem; margin-top: auto; padding-top: 1.25rem;">
            <a href="{slug_url}" target="_blank" class="resource-link">HTML Version →</a>
          </div>
        </div>

"""
        grid_pos = index_content.find('<div class="resource-grid">')
        if grid_pos == -1:
            print("Error: Could not find <div class=\"resource-grid\"> in index.html.")
            return False
            
        insert_index = index_content.find('\n', grid_pos) + 1
        updated_index_content = index_content[:insert_index] + new_card + index_content[insert_index:]
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(updated_index_content)
        print("Success: Injected new card link inside index.html's My Notes grid!")

    verify_script_path = os.path.join(path, 'verify_html.py')
    if os.path.exists(verify_script_path):
        print("Running HTML validation check...")
        verify_result = subprocess.run([sys.executable, verify_script_path], capture_output=True, text=True)
        if verify_result.returncode != 0:
            print("HTML Validation Error:")
            return False
        print("Success: HTML Validation checks passed cleanly.")

    print("\n" + "="*50)
    print("🚀 CONTENT GENERATED & COPIED TO CLIPBOARD 🚀")
    print("="*50)
    return True

if __name__ == '__main__':
    publish()
