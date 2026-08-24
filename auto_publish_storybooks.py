import os
import re
import sys
import shutil
import json
import subprocess

# Emoji and description mapping dictionaries for smart, automatic metadata inference
EMOJI_MAPPING = {
    "eat": "🥗",
    "fussy": "🥗",
    "food": "🥗",
    "healthy": "🥗",
    "toy": "🧸",
    "play": "🧸",
    "clean": "🧸",
    "share": "🤝",
    "sharing": "🤝",
    "potty": "🚽",
    "toilet": "🚽",
    "sleep": "🌙",
    "bed": "🌙",
    "night": "🌙",
    "bath": "🛁",
    "brush": "🪥",
    "teeth": "🪥",
    "brave": "🦋",
    "butterfly": "🦋",
    "pig": "🐷",
    "animal": "🐶"
}

DESC_MAPPING = {
    "eat": "An interactive, printable storybook helping toddlers understand and enjoy healthy eating habits and overcome fussy eating!",
    "fussy": "An interactive, printable storybook helping toddlers understand and enjoy healthy eating habits and overcome fussy eating!",
    "toy": "An interactive, printable storybook helping toddlers understand and enjoy cleaning up their toys and organizing their play spaces!",
    "clean": "An interactive, printable storybook helping toddlers understand and enjoy cleaning up their toys and organizing their play spaces!",
    "share": "A printable, interactive storybook teaching toddlers about sharing toys, taking turns, and the joy of cooperative play!",
    "potty": "A playful, encouraging printable storybook supporting parents and toddlers through potty training milestones with confidence!",
    "sleep": "A warm, gentle printable storybook designed to help toddlers settle down, follow bedtime routines, and fall asleep peacefully!",
    "bath": "A splashy, fun printable storybook helping toddlers enjoy bath time routines and water play safety!",
    "brush": "A happy, printable storybook designed to encourage toddlers to brush their teeth daily and enjoy healthy smiles!"
}

def infer_metadata(filename):
    clean_name = filename.lower().replace("_", " ").replace("-", " ").replace(".pdf", "").replace("storybook", "").strip()
    title = clean_name.title()
    
    # Infer Emoji Icon
    icon = "📖" # Default
    for key, value in EMOJI_MAPPING.items():
        if key in clean_name:
            icon = value
            break
            
    # Infer Description
    desc = f"An interactive, printable storybook designed for parents and toddlers to read and enjoy milestones together!" # Default
    for key, value in DESC_MAPPING.items():
        if key in clean_name:
            desc = value
            break
            
    slug = clean_name.replace(" ", "-").strip()
    return title, desc, icon, slug

def run_local_storybook_sync():
    print("[Local Sync] Starting local storybook auto-publishing scan...")
    source_dir = "/Users/kanchigupta/Desktop/AI_PROJECTS/kids storybooks/publish_ready"
    project_root = "/Users/kanchigupta/Desktop/AI_PROJECTS/handhold"
    dest_dir = os.path.join(project_root, "notes") # Point directly to notes/ directory
    kids_html_path = os.path.join(project_root, "kids-corner.html")

    if not os.path.exists(source_dir):
        print(f"[Local Sync] ERROR: Source folder not found at {source_dir}. Skipping scan.")
        return

    os.makedirs(dest_dir, exist_ok=True)

    # C: SCAN AND SYNC IMAGES/ILLUSTRATIONS DIRECTLY TO NOTES/ FOLDER
    source_images_dir = "/Users/kanchigupta/Desktop/AI_PROJECTS/kids storybooks/images"
    dest_images_dir = os.path.join(project_root, "notes")
    if os.path.exists(source_images_dir):
        for img in os.listdir(source_images_dir):
            if img.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp')):
                src_img_path = os.path.join(source_images_dir, img)
                dest_img_path = os.path.join(dest_images_dir, img)
                if not os.path.exists(dest_img_path):
                    shutil.copy(src_img_path, dest_img_path)
                    print(f"[Local Sync] Copied NEW illustration: {img}")

    with open(kids_html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    new_books_found = False

    # SCAN MANUAL PDFs IN publish_ready
    all_pdfs = [f for f in os.listdir(source_dir) if f.endswith('.pdf')]
    print(f"[Local Sync] Found {len(all_pdfs)} total PDFs in publish_ready directory.")

    for pdf in all_pdfs:
        title, desc, icon, slug = infer_metadata(pdf)
        pdf_public_name = f"Master_{slug}_Storybook.pdf"
        pdf_dest_path = os.path.join(dest_dir, pdf_public_name)
        pdf_source_path = os.path.join(source_dir, pdf)

        # Check if already registered in kids-corner.html
        if f'id: "{slug}"' in html_content or f'id: \'{slug}\'' in html_content or f'"id": "{slug}"' in html_content or f'"id": \'{slug}\'' in html_content:
            continue

        print(f"[Local Sync] Found NEW manual PDF storybook: {pdf}")
        print(f"            Title: {title} | Icon: {icon}")

        # 1. Copy the PDF file to her public website notes folder
        shutil.copy(pdf_source_path, pdf_dest_path)
        print(f"            Copied PDF to public path: notes/{pdf_public_name}")

        # 2. Check and copy matching HTML file if exists, stripping relative ../images/ paths
        html_public_name = f"Master_{slug}_Storybook.html"
        html_dest_path = os.path.join(dest_dir, html_public_name)
        html_source_name = pdf.replace(".pdf", ".html")
        html_source_path = os.path.join(source_dir, html_source_name)
        
        has_html = False
        if os.path.exists(html_source_path):
            with open(html_source_path, 'r', encoding='utf-8') as file:
                html_body = file.read()
            # Strip relative paths so images sit in the same notes/ folder cleanly!
            html_body_updated = html_body.replace("../images/", "").replace("./images/", "")
            
            # Unwrap any image-placeholder divs into real img tags
            placeholder_pattern = re.compile(
                r'<div class="image-placeholder">.*?<div class="placeholder-title">(.*?)</div>.*?<div class="placeholder-filename">File:\s*(.*?)</div>.*?</div>',
                re.DOTALL | re.IGNORECASE
            )
            def replacer(match):
                title = match.group(1).strip()
                filename_raw = match.group(2).strip()
                filename = filename_raw.replace("images/", "").replace("../", "").strip().lower()
                return f'<img src="{filename}" alt="{title}">'
            
            html_body_updated = placeholder_pattern.sub(replacer, html_body_updated)
            
            with open(html_dest_path, 'w', encoding='utf-8') as file:
                file.write(html_body_updated)
            print(f"            Copied, processed and unwrapped HTML to public path: notes/{html_public_name}")
            has_html = True

        # 3. Ingest the book metadata in her HTML database list
        new_book_obj = {
            "id": slug,
            "title": title,
            "desc": desc,
            "icon": icon,
            "pdfUrl": f"notes/{pdf_public_name}"
        }
        if has_html:
            new_book_obj["htmlUrl"] = f"notes/{html_public_name}"
            
        new_book_obj["pages"] = [
            {
                "quote": f"\"Look at the happy story about {title}!\"",
                "action": "Read the printed pages together and follow the action prompts.",
                "sound": "\"Hooray, yum, zoom!\""
            }
        ]
        
        # Inject into storybooks array inside kids-corner.html
        new_book_json = json.dumps(new_book_obj, indent=6, ensure_ascii=False)
        
        # Find const storybooks = [
        array_pos = html_content.find('const storybooks = [')
        if array_pos == -1:
            print("[Local Sync] ERROR: Could not find const storybooks array in kids-corner.html")
            return
            
        insert_pos = html_content.find('\n', array_pos) + 1
        html_content = html_content[:insert_pos] + "      " + new_book_json + ",\n" + html_content[insert_pos:]
        new_books_found = True

    if new_books_found:
        # Write back updated kids-corner.html
        with open(kids_html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("[Local Sync] Successfully updated and registered new books in kids-corner.html!")

        # 3. Commit and push the updates live to GitHub and Hostinger automatically!
        try:
            print("[Local Sync] Running git push to deploy changes live...")
            subprocess.run(["git", "add", "."], cwd=project_root, check=True)
            subprocess.run(["git", "commit", "-m", "chore(kids): autonomously index and publish newly discovered local storybook PDFs and HTMLs"], cwd=project_root, check=True)
            subprocess.run(["git", "pull", "origin", "main", "--rebase"], cwd=project_root, check=True)
            subprocess.run(["git", "push", "origin", "main"], cwd=project_root, check=True)
            print("[Local Sync] SUCCESS! New storybooks deployed to production automatically!")
        except Exception as e:
            print(f"[Local Sync] Git deployment error: {e}")
    else:
        print("[Local Sync] All storybooks are already indexed up-to-date. No action needed.")

if __name__ == '__main__':
    run_local_storybook_sync()
