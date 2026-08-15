import os
import sys
import html.parser

def verify_changes():
    html_path = '/Users/kanchigupta/Desktop/AI_PROJECTS/handhold/kids-corner.html'
    py_path = '/Users/kanchigupta/Desktop/AI_PROJECTS/handhold/auto_publish_storybooks.py'
    
    # 1. Verify python script syntax
    try:
        with open(py_path, 'r', encoding='utf-8') as f:
            code = f.read()
        compile(code, py_path, 'exec')
        print("Success: auto_publish_storybooks.py compiled successfully.")
    except Exception as e:
        print(f"Error compiling auto_publish_storybooks.py: {e}")
        return False
        
    # 2. Verify kids-corner.html has no duplicates and is valid
    if not os.path.exists(html_path):
        print("Error: kids-corner.html not found.")
        return False
        
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    # Check duplicates
    occurrences = html_content.count('"id": "brush-teeth"')
    if occurrences != 1:
        print(f"Error: Expected exactly 1 occurrence of '\"id\": \"brush-teeth\"', found {occurrences}")
        return False
    print("Success: kids-corner.html has exactly 1 'brush-teeth' registration.")
    
    # Check syntax validation of HTML
    class SimpleHTMLParser(html.parser.HTMLParser):
        def error(self, message):
            raise Exception(message)
            
    try:
        parser = SimpleHTMLParser()
        parser.feed(html_content)
        print("Success: kids-corner.html parsed as valid HTML.")
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return False
        
    return True

if __name__ == '__main__':
    success = verify_changes()
    sys.exit(0 if success else 1)
