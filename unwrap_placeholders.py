import os
import re

def unwrap_html_placeholders():
    notes_dir = "/Users/kanchigupta/Desktop/AI_PROJECTS/handhold/notes/"
    if not os.path.exists(notes_dir):
        return

    # Pattern to match the entire image-placeholder block
    # Looks for <div class="image-placeholder"> ... </div>
    placeholder_pattern = re.compile(
        r'<div class="image-placeholder">.*?<div class="placeholder-title">(.*?)</div>.*?<div class="placeholder-filename">File:\s*(.*?)</div>.*?</div>',
        re.DOTALL | re.IGNORECASE
    )

    for f in os.listdir(notes_dir):
        if f.endswith(".html") and "Storybook" in f:
            path = os.path.join(notes_dir, f)
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()

            def replacer(match):
                title = match.group(1).strip()
                filename_raw = match.group(2).strip()
                # Clean filename (strip images/ or ../images/ prefix)
                filename = filename_raw.replace("images/", "").replace("../", "").strip().lower()
                
                # We return a beautiful, standard img tag!
                return f'<img src="{filename}" alt="{title}">'

            updated_content, count = placeholder_pattern.subn(replacer, content)
            if count > 0:
                with open(path, "w", encoding="utf-8") as file:
                    file.write(updated_content)
                print(f"[Placeholder Unwrapper] Unwrapped {count} placeholders inside: {f}")

if __name__ == "__main__":
    unwrap_html_placeholders()
