import os
import sys

def verify_title():
    paths = [
        '/Users/kanchigupta/Desktop/AI_PROJECTS/Note maker/docs/notes/software_engineering_nptel/Master_Software_Engineering_NPTEL_Notes.html',
        '/Users/kanchigupta/Desktop/AI_PROJECTS/handhold/notes/Master_Software_Engineering_NPTEL_Notes.html'
    ]

    for path in paths:
        if not os.path.exists(path):
            print(f"Error: {path} does not exist.")
            return False
            
        with open(path, 'r', encoding='utf-8') as f:
            for i in range(10): # Check first 10 lines
                line = f.readline()
                if '<title>' in line:
                    if 'NPTEL Software Engineering Study Notes' in line:
                        print(f"Success: Title verified for {path}")
                        break
                    else:
                        print(f"Error: Title in {path} is incorrect: {line.strip()}")
                        return False
            else:
                print(f"Error: No <title> tag found in first 10 lines of {path}")
                return False
    return True

if __name__ == '__main__':
    success = verify_title()
    sys.exit(0 if success else 1)
