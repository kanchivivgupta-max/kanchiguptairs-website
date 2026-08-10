import os
import re
import sys
import json
import subprocess

def parse_markdown_storybook(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not frontmatter_match:
        print("Error: Storybook draft is missing YAML frontmatter.")
        return None

    frontmatter_raw = frontmatter_match.group(1)
    body = frontmatter_match.group(2)

    # Parse metadata
    title = re.search(r"^title:\s*\"?(.*?)\"?$", frontmatter_raw, re.MULTILINE).group(1).strip()
    description = re.search(r"^description:\s*\"?(.*?)\"?$", frontmatter_raw, re.MULTILINE).group(1).strip()
    icon = re.search(r"^icon:\s*\"?(.*?)\"?$", frontmatter_raw, re.MULTILINE).group(1).strip()

    pages = []
    # Parse slides
    slides_raw = body.strip().split("---")
    for slide in slides_raw:
        slide = slide.strip()
        if not slide:
            continue
        
        quote_match = re.search(r"^Quote:\s*\"?(.*?)\"?$", slide, re.MULTILINE)
        action_match = re.search(r"^Action:\s*\"?(.*?)\"?$", slide, re.MULTILINE)
        sound_match = re.search(r"^Sound:\s*\"?(.*?)\"?$", slide, re.MULTILINE)

        if quote_match and action_match and sound_match:
            pages.append({
                "quote": quote_match.group(1).strip(),
                "action": action_match.group(1).strip(),
                "sound": sound_match.group(1).strip()
            })

    slug = title.lower().replace(":", "").replace(" ", "-").replace("&", "and").strip()
    
    return {
        "id": slug,
        "title": title,
        "desc": description,
        "icon": icon,
        "pages": pages
    }

def publish_storybook():
    path = '/Users/kanchigupta/Desktop/AI_PROJECTS/handhold'
    draft_path = os.path.join(path, 'draft_storybook.md')
    mom_corner_path = os.path.join(path, 'mom-corner.html')

    if not os.path.exists(draft_path):
        print("Error: draft_storybook.md file not found in the project root.")
        return False

    book_data = parse_markdown_storybook(draft_path)
    if not book_data:
        return False

    with open(mom_corner_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Check if book already exists in file
    if f'id: "{book_data["id"]}"' in html_content or f'id: \'{book_data["id"]}\'' in html_content:
        print(f"Book with id '{book_data['id']}' is already registered in mom-corner.html.")
        return True

    # Construct the JSON string to inject
    new_book_json = json.dumps(book_data, indent=6, ensure_ascii=False)
    
    # We find the beginning of the array: const storybooks = [
    array_pos = html_content.find('const storybooks = [')
    if array_pos == -1:
        print("Error: Could not find const storybooks array in mom-corner.html.")
        return False

    insert_pos = html_content.find('\n', array_pos) + 1
    # Inject the new book as the second element (keeping the Pigs at the start or top)
    updated_html = html_content[:insert_pos] + "      " + new_book_json + ",\n" + html_content[insert_pos:]

    with open(mom_corner_path, 'w', encoding='utf-8') as f:
        f.write(updated_html)
    print(f"Success! Autonomously published and registered storybook: {book_data['title']} ({book_data['icon']})")

    # Clean up local draft_storybook.md to prevent repeating
    os.remove(draft_path)
    print("Success: Sanitized local draft_storybook.md after compiling.")
    return True

if __name__ == '__main__':
    publish_storybook()
