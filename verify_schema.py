import json
import re
import sys

PROJECT = '/Users/kanchigupta/Desktop/AI_PROJECTS/handhold'
CTARA = 'https://www.ctara.iitb.ac.in/alumni/kanchi-gupta'
FILES = ['index.html', 'about.html']


def run_verify():
    ok = True
    for name in FILES:
        path = f'{PROJECT}/{name}'
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        blocks = re.findall(
            r'<script type="application/ld\+json">(.*?)</script>', content, re.S
        )
        if not blocks:
            print(f'FAIL {name}: no JSON-LD block found')
            ok = False
            continue

        for i, block in enumerate(blocks):
            try:
                data = json.loads(block)
            except json.JSONDecodeError as e:
                print(f'FAIL {name} block {i}: invalid JSON -> {e}')
                ok = False
                continue
            print(f'OK   {name} block {i}: valid JSON-LD ({data.get("@type")})')

            same_as = data.get('sameAs', [])
            if CTARA in same_as:
                print(f'OK   {name}: C-TARA url present in sameAs')
            else:
                print(f'FAIL {name}: C-TARA url missing from sameAs')
                ok = False

            alumni = data.get('alumniOf', [])
            iit = [a for a in alumni if 'IIT' in a.get('name', '')]
            if iit and iit[0].get('url') == CTARA:
                print(f'OK   {name}: IIT Bombay alumniOf entry carries the C-TARA url')
            else:
                print(f'FAIL {name}: IIT Bombay alumniOf entry missing/without C-TARA url')
                ok = False

        visible = len(re.findall(re.escape(CTARA), content))
        schema_hits = len(re.findall(re.escape(CTARA), ''.join(blocks)))
        print(f'OK   {name}: C-TARA url appears {visible}x in file '
              f'({visible - schema_hits}x in visible body)')
        if visible - schema_hits < 1:
            print(f'FAIL {name}: no visible link to the C-TARA profile')
            ok = False

    print('RESULT:', 'ALL CHECKS PASSED' if ok else 'CHECKS FAILED')
    return ok


if __name__ == '__main__':
    sys.exit(0 if run_verify() else 1)
