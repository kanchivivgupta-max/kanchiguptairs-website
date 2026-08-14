import os
import re
import sys
import shutil
import json
import subprocess
import urllib.request

# Milestone topics for autonomous, localized AI generation
MILESTONES = [
    {
        "topic": "Potty Training",
        "title": "Potty Time Adventures",
        "desc": "A cheerful, encouraging printable storybook supporting parents and toddlers through potty training milestones with confidence!",
        "icon": "🚽",
        "keywords": ["potty", "toilet", "bathroom", "diaper"]
    },
    {
        "topic": "Fussy Eating",
        "title": "The Picnic Pigs",
        "desc": "An interactive, printable storybook helping toddlers understand and enjoy healthy eating habits and overcome fussy eating!",
        "icon": "🥗",
        "keywords": ["eat", "fussy", "food", "healthy"]
    },
    {
        "topic": "Sharing Toys",
        "title": "The Sharing Squirrels",
        "desc": "A printable, interactive storybook teaching toddlers about sharing toys, taking turns, and the joy of cooperative play!",
        "icon": "🤝",
        "keywords": ["share", "sharing", "toys", "friends"]
    },
    {
        "topic": "Bedtime Routines",
        "title": "Bella Sleepy Moon",
        "desc": "A warm, gentle printable storybook designed to help toddlers settle down, follow bedtime routines, and fall asleep peacefully!",
        "icon": "🌙",
        "keywords": ["sleep", "bed", "night", "sleeping"]
    },
    {
        "topic": "Brushing Teeth",
        "title": "The Happy Toothbrush",
        "desc": "A happy, printable storybook designed to encourage toddlers to brush their teeth daily and enjoy healthy smiles!",
        "icon": "🪥",
        "keywords": ["brush", "teeth", "mouth", "smile"]
    }
]

def generate_pdf_slides(title, description, pages, output_path):
    # Dynamically import inside the function to prevent linter/compile issues on machines without reportlab!
    try:
        from reportlab.lib.pagesizes import letter, landscape
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
    except ImportError:
        print("[PDF Compiler] reportlab not found locally. Skipping local PDF generation. (Cloud runner will compile this!)")
        return False

    print(f"[PDF Compiler] Generating printable landscape PDF Storybook at {output_path}...")
    try:
        # A4 Landscape size (842 x 595 points)
        doc = SimpleDocTemplate(
            output_path,
            pagesize=landscape(letter),
            leftMargin=50,
            rightMargin=50,
            topMargin=50,
            bottomMargin=50
        )
        
        styles = getSampleStyleSheet()
        
        # Color Palette variables (Playful Kids Pastels)
        color_cream = colors.HexColor("#FAF6F0")
        color_charcoal = colors.HexColor("#4A3B32")
        color_muted = colors.HexColor("#8C786C")
        color_pink = colors.HexColor("#FFD5D2")
        color_blue = colors.HexColor("#D0EBF5")
        color_yellow = colors.HexColor("#FDF1D6")
        color_green = colors.HexColor("#E2F3E4")
        color_accent = colors.HexColor("#E29578")
        
        # Typography styles
        style_cover_title = ParagraphStyle(
            'CoverTitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=34,
            leading=42,
            textColor=color_accent,
            alignment=1, # Center
            spaceAfter=15
        )
        
        style_cover_sub = ParagraphStyle(
            'CoverSub',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=16,
            leading=22,
            textColor=color_muted,
            alignment=1,
            spaceAfter=40
        )
        
        style_cover_author = ParagraphStyle(
            'CoverAuthor',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=12,
            leading=16,
            textColor=color_charcoal,
            alignment=1
        )
        
        style_quote = ParagraphStyle(
            'Quote',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=22,
            leading=28,
            textColor=color_charcoal,
            alignment=1,
            spaceAfter=25
        )
        
        style_card_title = ParagraphStyle(
            'CardTitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=12,
            textColor=color_charcoal,
            spaceAfter=6
        )
        
        style_card_body = ParagraphStyle(
            'CardBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=12,
            leading=16,
            textColor=color_charcoal
        )

        story = []
        
        # ==================== SLIDE 1: COVER PAGE ====================
        story.append(Spacer(1, 100))
        story.append(Paragraph(title, style_cover_title))
        story.append(Paragraph(description, style_cover_sub))
        story.append(Spacer(1, 40))
        story.append(Paragraph("<b>Compiled by Kanchi Gupta · Kids' Corner</b>", style_cover_author))
        story.append(Paragraph("An Interactive Learning Guide for Parents & Toddlers", ParagraphStyle('CoverSub2', parent=style_cover_sub, fontSize=11, leading=15)))
        story.append(PageBreak())
        
        # ==================== SLIDES 2+: STORY PAGES ====================
        page_num = 1
        for page in pages:
            story.append(Spacer(1, 30))
            # Big story quote
            story.append(Paragraph(f"\"{page['quote']}\"", style_quote))
            story.append(Spacer(1, 15))
            
            # Action and Sound Cards side-by-side Table
            p_action_title = Paragraph("<b>🫵 ACTION</b>", ParagraphStyle('AT', parent=style_card_title, textColor=colors.HexColor("#D4AF37")))
            p_action_body = Paragraph(page['action'], style_card_body)
            action_cell = [p_action_title, Spacer(1, 5), p_action_body]
            
            p_sound_title = Paragraph("<b>🔊 SOUND</b>", ParagraphStyle('ST', parent=style_card_title, textColor=colors.HexColor("#2D9CDB")))
            p_sound_body = Paragraph(page['sound'], style_card_body)
            sound_cell = [p_sound_title, Spacer(1, 5), p_sound_body]
            
            data = [[action_cell, sound_cell]]
            
            # Create interactive card table
            table = Table(data, colWidths=[340, 340])
            table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('BACKGROUND', (0,0), (0,0), color_yellow),
                ('BACKGROUND', (1,0), (1,0), color_blue),
                ('BOX', (0,0), (0,0), 1.5, colors.HexColor("#FDF1D6")),
                ('BOX', (1,0), (1,0), 1.5, colors.HexColor("#D0EBF5")),
                ('TOPPADDING', (0,0), (-1,-1), 15),
                ('BOTTOMPADDING', (0,0), (-1,-1), 15),
                ('LEFTPADDING', (0,0), (-1,-1), 15),
                ('RIGHTPADDING', (0,0), (-1,-1), 15),
                ('INNERGRID', (0,0), (-1,-1), 15, colors.white),
            ]))
            
            story.append(table)
            
            # Slide Footer
            story.append(Spacer(1, 45))
            p_footer = Paragraph(f"<b>Kanchi Gupta · Kids' Corner</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Page {page_num}", ParagraphStyle('F', parent=style_card_body, fontSize=8, textColor=color_muted))
            story.append(p_footer)
            
            story.append(PageBreak())
            page_num += 1
            
        doc.build(story)
        print(f"[PDF Compiler] SUCCESS! Deployed printable storybook PDF at: {output_path}")
        return True
    except Exception as e:
        print(f"[PDF Compiler] Error compiling storybook: {e}")
        return False

def call_local_ollama(prompt_text):
    """Query her local Ollama server if it is active, with fallback to standard templates if offline."""
    print("[Ollama] Contacting local Ollama server at http://localhost:11434...")
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "qwen", # Use her local Qwen or fall back gracefully
        "prompt": prompt_text,
        "stream": False,
        "format": "json"
    }
    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=5) as response:
            res = json.loads(response.read().decode('utf-8'))
            return json.loads(res.get('response', '{}'))
    except Exception as e:
        print(f"[Ollama] Local Ollama server currently offline or loading (Detail: {e}). Utilizing smart local generator pool instead!")
        return None

def query_or_generate_storybook(topic_meta):
    prompt_text = f"""
    You are an expert child psychologist and early development storybook author. Write a 5-page interactive toddler development storybook about "{topic_meta['topic']}".
    The story must help a 1-2 year old toddler hit their behavioral milestone.
    Return ONLY a JSON object with this EXACT structure (do not return any other text, notes, or markdown):
    {{
        "title": "{topic_meta['title']}",
        "desc": "{topic_meta['desc']}",
        "pages": [
            {{
                "quote": "Page 1 Storyline quote here",
                "action": "Page 1 parent-child sensory action instruction",
                "sound": "Page 1 fun sound cue"
            }},
            ...
        ]
    }}
    """
    ai_data = call_local_ollama(prompt_text)
    if ai_data and "pages" in ai_data:
        return ai_data
        
    # Standard high-quality local templates fallback (100% stable!)
    print(f"[Generator] Compiling template for: {topic_meta['topic']}")
    if "Potty" in topic_meta["topic"]:
        return {
            "title": "Leo's Potty Time Adventure",
            "desc": "A cheerful, encouraging printable storybook supporting parents and toddlers through potty training milestones with confidence!",
            "pages": [
                {"quote": "Look! Leo has a shiny, bright green potty chair. It is just for him!", "action": "Point to the chair and tap the page together.", "sound": "\"Hooray, my potty!\""},
                {"quote": "Leo is sitting on his cozy potty chair. We wait, wait, wait.", "action": "Wiggle your feet and tap your knees patiently.", "sound": "\"Tick-tock, tick-tock.\""},
                {"quote": "Listen! Splash, splash, tinkle! The potty catches the water!", "action": "Clap your hands together happily: \"You did it!\"", "sound": "\"Clap, clap, clap!\""},
                {"quote": "Press the button! Watch the water go flush, flush, flush!", "action": "Pretend to press a button and wave goodbye to the water.", "sound": "\"Swoosh, flush, swoosh!\""},
                {"quote": "Wash, wash, wash! We rub our hands with warm, bubbly soap.", "action": "Rub your palms together and pretend to wash.", "sound": "\"Splash, splash, scrub!\""}
            ]
        }
    elif "Eating" in topic_meta["topic"]:
        return {
            "title": "The Picnic Pigs & Sweet Apples",
            "desc": "An interactive, printable storybook helping toddlers understand and enjoy healthy eating habits and overcome fussy eating!",
            "pages": [
                {"quote": "Look at the happy little pigs setting up a sunny red picnic blanket!", "action": "Tap the floor to make a cozy picnic spot.", "sound": "\"Oink, oink, oink!\""},
                {"quote": "Crunch! The pig is biting into a sweet, juicy green apple.", "action": "Pretend to bite into a crisp apple and chew.", "sound": "\"Crunch, crunch, yum!\""},
                {"quote": "Yum! Look at the cool, sweet orange carrots. They are so crunchy!", "action": "Point to your nose and wiggle it like a bunny.", "sound": "\"Munch, munch, munch!\""},
                {"quote": "Sip, sip, sip! We drink a cup of cold, fresh white milk.", "action": "Pretend to hold a tiny cup and drink slowly.", "sound": "\"Gulp, gulp, ahhh!\""},
                {"quote": "Rub your tummy! The little pigs are full, strong, and ready to play!", "action": "Rub your tummy and stretch your arms up high.", "sound": "\"Hooray for healthy food!\""}
            ]
        }
    else: # Default/Sharing template
        return {
            "title": "Milo the Monkey Learns to Share",
            "desc": "A printable, interactive storybook teaching toddlers about sharing toys, taking turns, and the joy of cooperative play!",
            "pages": [
                {"quote": "Look! Milo has a shiny red ball. Roll, roll, roll!", "action": "Pretend to roll a ball back and forth.", "sound": "\"Bounce, bounce, bounce!\""},
                {"quote": "Milo's friend wants to play. Milo says: \"Your turn!\" and passes the ball.", "action": "Gently tap your toddler's hand: \"Your turn!\"", "sound": "\"Here you go!\""},
                {"quote": "Now Milo catches the ball! Milo says: \"My turn!\"", "action": "Clapping your hands together to catch the ball.", "sound": "\"Catch, catch, wheee!\""},
                {"quote": "Look! Milo and his friend are laughing and wiggling together.", "action": "Tickle your toddler's tummy gently: \"We are wiggling!\"", "sound": "\"Giggle, giggle, zoom!\""},
                {"quote": "Sharing makes Milo so happy. Good job sharing, Milo!", "action": "Give your toddler a big warm hug: \"You are so kind!\"", "sound": "\"Hooray, high-five!\""}
            ]
        }

def run_local_storybook_sync():
    print("[Local Sync] Starting local storybook auto-publishing scan...")
    source_dir = "/Users/kanchigupta/Desktop/AI_PROJECTS/kids storybooks/publish_ready"
    project_root = "/Users/kanchigupta/Desktop/AI_PROJECTS/handhold"
    dest_dir = os.path.join(project_root, "notes/storybooks")
    kids_html_path = os.path.join(project_root, "kids-corner.html")

    os.makedirs(dest_dir, exist_ok=True)

    with open(kids_html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    new_books_found = False

    # A: SCAN MANUAL PDFs
    if os.path.exists(source_dir):
        all_pdfs = [f for f in os.listdir(source_dir) if f.endswith('.pdf')]
        for pdf in all_pdfs:
            # Check if already registered
            clean_name = pdf.lower().replace("_", " ").replace("-", " ").replace(".pdf", "").replace("storybook", "").strip()
            slug = clean_name.replace(" ", "-").strip()
            if f'id: "{slug}"' in html_content or f'id: \'{slug}\'' in html_content:
                continue

            print(f"[Local Sync] Found NEW manual PDF storybook: {pdf}")
            # Run metadata inference
            clean_name = pdf.lower().replace("_", " ").replace("-", " ").replace(".pdf", "").replace("storybook", "").strip()
            title = clean_name.title()
            icon = "🧸" if "toy" in clean_name or "clean" in clean_name else "🥗"
            desc = "An interactive, printable storybook helping toddlers master key stages!"
            
            pdf_public_name = f"Master_{slug}_Storybook.pdf"
            shutil.copy(os.path.join(source_dir, pdf), os.path.join(dest_dir, pdf_public_name))

            new_book_obj = {
                "id": slug,
                "title": title,
                "desc": desc,
                "icon": icon,
                "pdfUrl": f"notes/storybooks/{pdf_public_name}",
                "pages": [{"quote": "Printed pages are ready to read!", "action": "Follow actions together.", "sound": "Hooray!"}]
            }
            new_book_json = json.dumps(new_book_obj, indent=6, ensure_ascii=False)
            array_pos = html_content.find('const storybooks = [')
            if array_pos != -1:
                insert_pos = html_content.find('\n', array_pos) + 1
                html_content = html_content[:insert_pos] + "      " + new_book_json + ",\n" + html_content[insert_pos:]
                new_books_found = True

    # B: AUTONOMOUS GENERATOR ENGINE
    # Find next milestone topic that hasn't been published yet
    selected_milestone = None
    for m in MILESTONES:
        slug = m["title"].lower().replace(" ", "-").strip()
        if f'id: "{slug}"' not in html_content and f'id: \'{slug}\'' not in html_content:
            selected_milestone = m
            break

    if selected_milestone:
        print(f"[Local Sync] AUTONOMOUS TRIGGER! Creating Storybook: {selected_milestone['title']}")
        book_data = query_or_generate_storybook(selected_milestone)
        
        slug = selected_milestone["title"].lower().replace(" ", "-").strip()
        pdf_filename = f"Master_{slug}_Storybook.pdf"
        pdf_dest_path = os.path.join(dest_dir, pdf_filename)
        
        # Compile PDF on MacBook
        if generate_pdf_slides(book_data['title'], book_data['desc'], book_data['pages'], pdf_dest_path):
            new_book_obj = {
                "id": slug,
                "title": book_data['title'],
                "desc": book_data['desc'],
                "icon": selected_milestone["icon"],
                "pdfUrl": f"notes/storybooks/{pdf_filename}",
                "pages": book_data['pages']
            }
            new_book_json = json.dumps(new_book_obj, indent=6, ensure_ascii=False)
            array_pos = html_content.find('const storybooks = [')
            if array_pos != -1:
                insert_pos = html_content.find('\n', array_pos) + 1
                html_content = html_content[:insert_pos] + "      " + new_book_json + ",\n" + html_content[insert_pos:]
                new_books_found = True

    if new_books_found:
        with open(kids_html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("[Local Sync] Successfully updated and registered new books in kids-corner.html!")

        # Push updates live to production!
        try:
            print("[Local Sync] Running git push to deploy changes live...")
            subprocess.run(["git", "add", "."], cwd=project_root, check=True)
            subprocess.run(["git", "commit", "-m", "chore(kids): autonomously compile, index, and publish scheduled toddler development PDF"], cwd=project_root, check=True)
            subprocess.run(["git", "pull", "origin", "main", "--rebase"], cwd=project_root, check=True)
            subprocess.run(["git", "push", "origin", "main"], cwd=project_root, check=True)
            print("[Local Sync] SUCCESS! New storybooks deployed to production automatically!")
        except Exception as e:
            print(f"[Local Sync] Git deployment error: {e}")
    else:
        print("[Local Sync] All storybooks are already indexed up-to-date. No action needed.")

if __name__ == '__main__':
    run_local_storybook_sync()
