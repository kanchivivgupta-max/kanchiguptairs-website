import json
import os
import re
import sys

PROJECT = '/Users/kanchigupta/Desktop/AI_PROJECTS/handhold'
CTARA = 'https://www.ctara.iitb.ac.in/alumni/kanchi-gupta'
FILES = ['index.html', 'about.html', 'kanchi-gupta.html']
AI_CRAWLERS = ['GPTBot', 'ClaudeBot', 'PerplexityBot', 'OAI-SearchBot', 'Google-Extended']


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

            if not data.get('@id'):
                print(f'FAIL {name}: Person missing @id (entity anchoring)')
                ok = False
            if not data.get('hasOccupation'):
                print(f'FAIL {name}: Person missing hasOccupation')
                ok = False
            if not data.get('knowsAbout'):
                print(f'FAIL {name}: Person missing knowsAbout')
                ok = False

            same_as = data.get('sameAs', [])
            if CTARA in same_as:
                print(f'OK   {name}: C-TARA url present in sameAs')
            else:
                print(f'FAIL {name}: C-TARA url missing from sameAs')
                ok = False

        visible = len(re.findall(re.escape(CTARA), content))
        schema_hits = len(re.findall(re.escape(CTARA), ''.join(blocks)))
        if visible - schema_hits < 1 and name != 'kanchi-gupta.html':
            print(f'FAIL {name}: no visible link to the C-TARA profile')
            ok = False

    # llms.txt
    llms = f'{PROJECT}/llms.txt'
    if os.path.exists(llms):
        with open(llms, 'r', encoding='utf-8') as f:
            text = f.read()
        needed = ['Kanchi Gupta', 'kanchi-gupta.html', 'nacin.gov.in', CTARA]
        missing = [n for n in needed if n not in text]
        if missing:
            print(f'FAIL llms.txt: missing references -> {missing}')
            ok = False
        else:
            print('OK   llms.txt: present with canonical profile + official citations')
        if '## Optional' in text:
            print('WARN llms.txt: "## Optional" section should come last if used')
    else:
        print('FAIL llms.txt: missing')
        ok = False

    # robots.txt AI crawler allowances
    with open(f'{PROJECT}/robots.txt', 'r', encoding='utf-8') as f:
        robots = f.read()
    missing_bots = [b for b in AI_CRAWLERS if f'User-agent: {b}' not in robots]
    if missing_bots:
        print(f'FAIL robots.txt: no explicit rule for {missing_bots}')
        ok = False
    else:
        print(f'OK   robots.txt: explicit Allow rules for {len(AI_CRAWLERS)} AI crawlers')

    # sitemap contains the fact sheet
    with open(f'{PROJECT}/sitemap.xml', 'r', encoding='utf-8') as f:
        sitemap = f.read()
    if 'kanchi-gupta.html' in sitemap:
        print('OK   sitemap.xml: fact sheet submitted')
    else:
        print('FAIL sitemap.xml: fact sheet not listed')
        ok = False

    print('RESULT:', 'ALL CHECKS PASSED' if ok else 'CHECKS FAILED')
    return ok


if __name__ == '__main__':
    sys.exit(0 if run_verify() else 1)
