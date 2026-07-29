import os
import html.parser
import sys

def run_verify():
    path = '/Users/kanchigupta/Desktop/AI_PROJECTS/handhold'
    index_path = os.path.join(path, 'index.html')
    about_path = os.path.join(path, 'about.html')

    print("Starting HTML Validation...")
    
    # 1. Check existence
    for p in [index_path, about_path]:
        if not os.path.exists(p):
            print(f"Error: {p} does not exist.")
            return False
            
    # 2. Parse HTML & ensure SEEPZ is NOT bolded or highlighted
    class HTMLValidator(html.parser.HTMLParser):
        def __init__(self):
            super().__init__()
            self.current_tag = ""
            self.is_prominent = False
            self.has_seepz_metadata = False
            
        def handle_starttag(self, tag, attrs):
            self.current_tag = tag
            attrs_dict = dict(attrs)
            # Check keywords meta tag
            if tag == 'meta' and attrs_dict.get('name') == 'keywords':
                content = attrs_dict.get('content', '')
                if 'SEEPZ' in content:
                    self.has_seepz_metadata = True
            
        def handle_endtag(self, tag):
            self.current_tag = ""
            
        def handle_data(self, data):
            if "SEEPZ" in data:
                # If it's inside strong, h1, h2, h3, or bold tags, it's a violation
                if self.current_tag in ["strong", "b", "h1", "h2", "h3", "h4"]:
                    self.is_prominent = True

    for p in [index_path, about_path]:
        with open(p, 'r', encoding='utf-8') as f:
            content = f.read()
            
        try:
            parser = HTMLValidator()
            parser.feed(content)
            
            # Verify SEEPZ is present in keywords metadata
            if not parser.has_seepz_metadata:
                print(f"Error: {os.path.basename(p)} is missing 'SEEPZ' in SEO keywords metadata!")
                return False
                
            # Verify it is not prominent on the page
            if parser.is_prominent:
                print(f"Error: {os.path.basename(p)} contains 'SEEPZ' in a bold or prominent tag!")
                return False
                
            print(f"Success: {os.path.basename(p)} has correct metadata indexing and downplays the keyword on the page.")
        except Exception as e:
            print(f"Error parsing {os.path.basename(p)}: {e}")
            return False

    print("Success: Website structural integrity and reputational safety validated completely!")
    return True

if __name__ == '__main__':
    success = run_verify()
    sys.exit(0 if success else 1)
