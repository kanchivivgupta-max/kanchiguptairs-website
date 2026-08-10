import os
import re
import sys
import json
import subprocess

def generate_pdf_slides(title, description, pages, output_path):
    try:
        from reportlab.lib.pagesizes import letter, landscape
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.pdfgen import canvas
    except ImportError:
        print("[PDF Compiler] reportlab not available. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])
        from reportlab.lib.pagesizes import letter, landscape
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.pdfgen import canvas

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

def parse_markdown_storybook(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", content, re.DOTALL)
    if not frontmatter_match:
        print("Error: Storybook draft is missing YAML frontmatter.")
        return None

    frontmatter_raw = frontmatter_match.group(1)
    body = frontmatter_match.group(2)

    title = re.search(r"^title:\s*\"?(.*?)\"?$", frontmatter_raw, re.MULTILINE).group(1).strip()
    description = re.search(r"^description:\s*\"?(.*?)\"?$", frontmatter_raw, re.MULTILINE).group(1).strip()
    icon = re.search(r"^icon:\s*\"?(.*?)\"?$", frontmatter_raw, re.MULTILINE).group(1).strip()

    pages = []
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

def cloud_publish_storybook():
    path = os.getcwd()
    drafts_pool_dir = os.path.join(path, 'storybooks_pool')
    log_file_path = os.path.join(path, 'published_storybooks_log.txt')
    mom_corner_path = os.path.join(path, 'kids-corner.html')

    # Create directories if missing
    os.makedirs(drafts_pool_dir, exist_ok=True)
    os.makedirs(os.path.join(path, 'notes/storybooks'), exist_ok=True)

    # Read published log
    published_files = []
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r', encoding='utf-8') as f:
            published_files = [line.strip() for line in f.read().split("\n") if line.strip()]

    # Scan pool
    all_drafts = sorted([f for f in os.listdir(drafts_pool_dir) if f.endswith('.md')])
    
    selected_draft_file = None
    for draft in all_drafts:
        if draft not in published_files:
            selected_draft_file = draft
            break

    if not selected_draft_file:
        print("[Cloud Storybook Factory] WARNING: All storybooks in pool published! Drop more markdown drafts in kanchivivgupta-max/kanchiguptairs-website/storybooks_pool/ to continue.")
        sys.exit(0)

    draft_full_path = os.path.join(drafts_pool_dir, selected_draft_file)
    print(f"[Cloud Storybook Factory] Processing Draft: {selected_draft_file}")

    book_data = parse_markdown_storybook(draft_full_path)
    if not book_data:
        sys.exit(1)

    pdf_filename = f"notes/storybooks/Master_{book_data['id']}_Storybook.pdf"
    pdf_full_path = os.path.join(path, pdf_filename)

    # Compile PDF
    if generate_pdf_slides(book_data['title'], book_data['desc'], book_data['pages'], pdf_full_path):
        # Update kids-corner.html to add a simple download card!
        with open(mom_corner_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Check if already registered
        if f'href="{pdf_filename}"' in html_content:
            print("Book already registered. Skipping link insertion.")
        else:
            # Construct a beautiful card with download button
            new_card = f"""      <!-- Storybook Card: {book_data['title']} -->
      <div class="book-card" style="cursor: default;">
        <div>
          <div class="book-icon">{book_data['icon']}</div>
          <h3 class="book-title">{book_data['title']}</h3>
          <p class="book-desc">{book_data['desc']}</p>
        </div>
        <a href="{pdf_filename}" download class="book-btn" style="background: var(--accent); color: white;">Download Printable PDF 📥</a>
      </div>

"""
            # Find the grid: <div class="books-grid" id="books-container">
            grid_pos = html_content.find('<div class="books-grid" id="books-container">')
            if grid_pos == -1:
                print("Error: Could not find books-grid in kids-corner.html")
                sys.exit(1)

            insert_pos = html_content.find('\n', grid_pos) + 1
            updated_html = html_content[:insert_pos] + new_card + html_content[insert_pos:]

            with open(mom_corner_path, 'w', encoding='utf-8') as f:
                f.write(updated_html)
            print(f"Success: Registered and updated kids-corner.html sitemaps!")

        # Append to log
        with open(log_file_path, 'a', encoding='utf-8') as f:
            f.write(selected_draft_file + "\n")
        print(f"Success: Logged {selected_draft_file} as published.")

if __name__ == '__main__':
    cloud_publish_storybook()
