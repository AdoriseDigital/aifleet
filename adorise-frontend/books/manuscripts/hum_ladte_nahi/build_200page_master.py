import os
import sys
import re
from pathlib import Path
import fitz  # PyMuPDF
import ebooklib
from ebooklib import epub
import markdown

from reportlab.lib.pagesizes import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

from text_front_matter import FRONT_MATTER
from text_part1 import PART1_TEXT
from text_part2 import PART2_TEXT
from text_part3 import PART3_TEXT
from text_part4 import PART4_TEXT

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

BASE_DIR = Path(r"C:\Users\HOME_PC\Documents\antigravity\calm-carson\adorise-frontend\books\manuscripts\hum_ladte_nahi")
COMPLETE_MD = BASE_DIR / "book_manuscript_complete.md"
COVER_IMG = Path(r"C:\Users\HOME_PC\Documents\antigravity\calm-carson\adorise-frontend\books\previews\Care Collection Lead magnets\Hum_Ladte_Nahi_Real_Cover.jpg")

PDF_OUT_FULL = BASE_DIR / "Hum_Ladte_Nahi_Par_Baat_Hi_Nahi_Karte.pdf"
EPUB_OUT = BASE_DIR / "Hum_Ladte_Nahi_Par_Baat_Hi_Nahi_Karte.epub"
PDF_OUT_PREVIEW = BASE_DIR / "Hum_Ladte_Nahi_3_Chapter_Preview.pdf"

PAGE_W = 6.0 * 72.0  # 432 pt
PAGE_H = 9.0 * 72.0  # 648 pt
MARGIN = 42.0

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber <= 4:
            return
        self.saveState()
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#666666"))
        
        # Running Header
        if self._pageNumber % 2 == 0:
            self.drawString(MARGIN, PAGE_H - 32, "HUM LADTE NAHI, PAR BAAT NAHI KARTE")
        else:
            self.drawRightString(PAGE_W - MARGIN, PAGE_H - 32, "SANJAY SHHARMA • THE CARE COLLECTION")
            
        self.setStrokeColor(colors.HexColor("#D8D2C4"))
        self.setLineWidth(0.5)
        self.line(MARGIN, PAGE_H - 36, PAGE_W - MARGIN, PAGE_H - 36)
        
        # Running Footer
        self.drawCentredString(PAGE_W / 2.0, 26, f"- {self._pageNumber} -")
        self.restoreState()

def get_book_styles():
    styles = getSampleStyleSheet()
    c_primary = colors.HexColor("#1A202C")
    c_accent = colors.HexColor("#8C2D19")
    c_sub = colors.HexColor("#4A5568")
    
    styles.add(ParagraphStyle('BookTitle', fontName='Helvetica-Bold', fontSize=22, leading=26, textColor=c_accent, alignment=1, spaceAfter=8))
    styles.add(ParagraphStyle('BookSubtitle', fontName='Helvetica', fontSize=12, leading=16, textColor=c_sub, alignment=1, spaceAfter=15))
    styles.add(ParagraphStyle('BookAuthor', fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=c_primary, alignment=1, spaceAfter=4))
    styles.add(ParagraphStyle('BookCredentials', fontName='Helvetica-Oblique', fontSize=9, leading=13, textColor=c_sub, alignment=1, spaceAfter=25))
    styles.add(ParagraphStyle('PartHeader', fontName='Helvetica-Bold', fontSize=16, leading=20, textColor=colors.HexColor("#2D3748"), alignment=1, spaceBefore=15, spaceAfter=15))
    styles.add(ParagraphStyle('ChapterHeader', fontName='Helvetica-Bold', fontSize=15, leading=19, textColor=c_accent, spaceBefore=18, spaceAfter=6, keepWithNext=True))
    styles.add(ParagraphStyle('ChapterSubtitle', fontName='Helvetica-Oblique', fontSize=10, leading=14, textColor=c_sub, spaceAfter=12, keepWithNext=True))
    styles.add(ParagraphStyle('SectionHeader', fontName='Helvetica-Bold', fontSize=11.5, leading=15, textColor=colors.HexColor("#2C3E50"), spaceBefore=14, spaceAfter=6, keepWithNext=True))
    styles.add(ParagraphStyle('BookBody', fontName='Helvetica', fontSize=9.5, leading=14.0, textColor=c_primary, spaceAfter=8))
    styles.add(ParagraphStyle('BookBodyBold', fontName='Helvetica-Bold', fontSize=9.5, leading=14.0, textColor=c_primary, spaceAfter=8))
    styles.add(ParagraphStyle('BookBullet', fontName='Helvetica', fontSize=9.5, leading=13.5, textColor=c_primary, leftIndent=15, firstLineIndent=-10, spaceAfter=4))
    styles.add(ParagraphStyle('CalloutText', fontName='Helvetica-Oblique', fontSize=9.0, leading=13.5, textColor=colors.HexColor("#2D3748"), spaceAfter=4))
    styles.add(ParagraphStyle('CalloutBold', fontName='Helvetica-Bold', fontSize=9.5, leading=14.0, textColor=c_accent, spaceAfter=4))
    styles.add(ParagraphStyle('TableHead', fontName='Helvetica-Bold', fontSize=8.5, leading=11.5, textColor=colors.white, alignment=0))
    styles.add(ParagraphStyle('TableCell', fontName='Helvetica', fontSize=8.0, leading=11.0, textColor=c_primary, alignment=0))
    styles.add(ParagraphStyle('TableCellBold', fontName='Helvetica-Bold', fontSize=8.0, leading=11.0, textColor=c_primary, alignment=0))
    styles.add(ParagraphStyle('SmallLegal', fontName='Helvetica', fontSize=7.5, leading=10.5, textColor=colors.HexColor("#555555"), spaceAfter=6))
    return styles

def parse_markdown_to_story(md_text, styles):
    lines = md_text.splitlines()
    story = []
    
    in_table = False
    table_data = []
    in_callout = False
    callout_lines = []
    in_mermaid = False
    
    def flush_callout():
        nonlocal in_callout, callout_lines
        if callout_lines:
            c_pars = []
            for cl in callout_lines:
                cl_clean = cl.strip().lstrip(">").strip()
                if not cl_clean:
                    continue
                cl_clean = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', cl_clean)
                cl_clean = re.sub(r'\*(.*?)\*', r'<i>\1</i>', cl_clean)
                if cl_clean.startswith("<b>") and ":" in cl_clean:
                    c_pars.append(Paragraph(cl_clean, styles['CalloutBold']))
                else:
                    c_pars.append(Paragraph(cl_clean, styles['CalloutText']))
            
            box_table = Table([[c_pars]], colWidths=[PAGE_W - 2 * MARGIN])
            box_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F9F7F2")),
                ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#D1C7B7")),
                ('LINELEFT', (0,0), (-1,-1), 3.5, colors.HexColor("#8C2D19")),
                ('TOPPADDING', (0,0), (-1,-1), 8),
                ('BOTTOMPADDING', (0,0), (-1,-1), 8),
                ('LEFTPADDING', (0,0), (-1,-1), 12),
                ('RIGHTPADDING', (0,0), (-1,-1), 12),
            ]))
            story.append(Spacer(1, 6))
            story.append(box_table)
            story.append(Spacer(1, 8))
            callout_lines = []
        in_callout = False

    def flush_table():
        nonlocal in_table, table_data
        if table_data:
            num_cols = len(table_data[0])
            total_w = PAGE_W - 2 * MARGIN
            if num_cols == 2:
                col_w = [total_w * 0.70, total_w * 0.30] if "Score" in str(table_data[0]) else [total_w * 0.35, total_w * 0.65]
            elif num_cols == 3:
                col_w = [total_w * 0.28, total_w * 0.36, total_w * 0.36]
            elif num_cols == 4:
                col_w = [total_w * 0.16, total_w * 0.22, total_w * 0.50, total_w * 0.12]
            else:
                col_w = [total_w / num_cols] * num_cols
                
            formatted_data = []
            for r_idx, row in enumerate(table_data):
                f_row = []
                for c_idx, cell in enumerate(row):
                    cell_text = cell.strip()
                    cell_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', cell_text)
                    cell_text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', cell_text)
                    if r_idx == 0:
                        p = Paragraph(cell_text, styles['TableHead'])
                    elif c_idx == 0 or cell_text.startswith("<b>") or "Total" in cell_text:
                        p = Paragraph(cell_text, styles['TableCellBold'])
                    else:
                        p = Paragraph(cell_text, styles['TableCell'])
                    f_row.append(p)
                formatted_data.append(f_row)
                
            tbl = Table(formatted_data, colWidths=col_w, repeatRows=1)
            tbl.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2C3E50")),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('TOPPADDING', (0,0), (-1,-1), 4),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                ('LEFTPADDING', (0,0), (-1,-1), 5),
                ('RIGHTPADDING', (0,0), (-1,-1), 5),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D5D8DC")),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8F9F9")]),
            ]))
            story.append(Spacer(1, 6))
            story.append(tbl)
            story.append(Spacer(1, 8))
            table_data = []
        in_table = False

    i = 0
    while i < len(lines):
        line = lines[i]
        raw_s = line.strip()
        
        if raw_s.startswith("```mermaid"):
            in_mermaid = True
            i += 1
            continue
        if in_mermaid:
            if raw_s.startswith("```"):
                in_mermaid = False
            i += 1
            continue

        if raw_s.startswith(">"):
            in_callout = True
            callout_lines.append(raw_s)
            i += 1
            continue
        elif in_callout:
            flush_callout()

        if raw_s.startswith("|") and raw_s.endswith("|"):
            if not in_table:
                in_table = True
            if re.match(r'^\|[\s\-:]+\|$', raw_s):
                i += 1
                continue
            cells = [c.strip() for c in raw_s.strip("|").split("|")]
            table_data.append(cells)
            i += 1
            continue
        elif in_table:
            flush_table()

        if not raw_s:
            i += 1
            continue

        if raw_s == "---":
            story.append(Spacer(1, 8))
            story.append(HRFlowable(width="85%", thickness=0.5, color=colors.HexColor("#D8D2C4"), spaceAfter=14, spaceBefore=8))
            i += 1
            continue

        if raw_s.startswith("# PART") or raw_s.startswith("# BONUS") or raw_s.startswith("# EPILOGUE") or raw_s.startswith("# BACK MATTER"):
            story.append(PageBreak())
            story.append(Spacer(1, 35))
            part_title = raw_s.lstrip("#").strip()
            story.append(Paragraph(part_title, styles['PartHeader']))
            story.append(HRFlowable(width="50%", thickness=1.5, color=colors.HexColor("#8C2D19"), spaceAfter=18, spaceBefore=8))
            i += 1
            continue

        if raw_s.startswith("## Chapter") or raw_s.startswith("## Bonus Toolkit") or raw_s.startswith("## 50 Hinglish"):
            story.append(PageBreak())
            ch_title = raw_s.lstrip("#").strip()
            sub_text = ""
            if i + 1 < len(lines) and lines[i+1].strip().startswith("*(") and lines[i+1].strip().endswith(")*"):
                sub_text = lines[i+1].strip().strip("*()").strip()
                i += 1
            story.append(Spacer(1, 14))
            story.append(Paragraph(ch_title, styles['ChapterHeader']))
            if sub_text:
                story.append(Paragraph(f"<i>({sub_text})</i>", styles['ChapterSubtitle']))
            i += 1
            continue

        if raw_s.startswith("## "):
            h2_text = raw_s.lstrip("#").strip()
            if "Copyright" in h2_text or "Dedication" in h2_text or "Author's Personal" in h2_text or "Introduction" in h2_text or "About the Author" in h2_text or "Connect with" in h2_text or "The 48-Book" in h2_text:
                story.append(PageBreak())
            story.append(Spacer(1, 10))
            story.append(Paragraph(h2_text, styles['SectionHeader']))
            i += 1
            continue

        if raw_s.startswith("### "):
            h3_text = raw_s.lstrip("#").strip()
            story.append(Spacer(1, 8))
            story.append(Paragraph(h3_text, styles['SectionHeader']))
            i += 1
            continue

        if raw_s.startswith("# Hum Ladte Nahi"):
            story.append(Spacer(1, 45))
            story.append(Paragraph("Hum Ladte Nahi, Par Baat Nahi Karte", styles['BookTitle']))
            i += 1
            continue
        if raw_s.startswith("### A 4-Phase Framework"):
            story.append(Paragraph("A 4-Phase Framework for the Silent Indian Marriage", styles['BookSubtitle']))
            story.append(Spacer(1, 35))
            i += 1
            continue
        if raw_s.startswith("**Authored by Sanjay Shharma**"):
            story.append(Paragraph("Sanjay Shharma", styles['BookAuthor']))
            i += 1
            continue
        if raw_s.startswith("*M.Sc., MBA, APSCM"):
            story.append(Paragraph("M.Sc., MBA, APSCM (IIM Calcutta Alumni)<br/>Author of <i>The Care Collection</i>", styles['BookCredentials']))
            story.append(Spacer(1, 40))
            story.append(Paragraph("Published by Adorise Digital<br/>Trendy DigiStore LLC, Wyoming, USA", styles['BookCredentials']))
            story.append(PageBreak())
            i += 1
            continue

        if raw_s.startswith("- ") or raw_s.startswith("* "):
            b_text = raw_s[2:].strip()
            b_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', b_text)
            b_text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', b_text)
            b_text = f"&bull;&nbsp; {b_text}"
            story.append(Paragraph(b_text, styles['BookBullet']))
            i += 1
            continue
            
        m_num = re.match(r'^(\d+)\.\s+(.*)$', raw_s)
        if m_num:
            n_num, n_text = m_num.groups()
            n_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', n_text)
            n_text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', n_text)
            formatted_n = f"<b>{n_num}.</b>&nbsp; {n_text}"
            story.append(Paragraph(formatted_n, styles['BookBullet']))
            i += 1
            continue

        p_text = raw_s
        p_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', p_text)
        p_text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', p_text)
        p_text = re.sub(r'\[(.*?)\]\(.*?\)', r'<font color="#8C2D19"><u>\1</u></font>', p_text)

        if "Copyright ©" in p_text or "All rights reserved" in p_text or "Disclaimer:" in p_text or "Confidential Helplines" in p_text:
            story.append(Paragraph(p_text, styles['SmallLegal']))
        elif p_text.startswith("<b>") and len(p_text) < 80 and ":" not in p_text:
            story.append(Paragraph(p_text, styles['BookBodyBold']))
        else:
            story.append(Paragraph(p_text, styles['BookBody']))

        i += 1

    if in_callout:
        flush_callout()
    if in_table:
        flush_table()

    return story

def main():
    print("=== ASSEMBLING COMPLETE 200-PAGE BESTSELLER MANUSCRIPT ===")
    full_manuscript = f"{FRONT_MATTER.strip()}\n\n---\n\n{PART1_TEXT.strip()}\n\n---\n\n{PART2_TEXT.strip()}\n\n---\n\n{PART3_TEXT.strip()}\n\n---\n\n{PART4_TEXT.strip()}\n"
    COMPLETE_MD.write_text(full_manuscript, encoding="utf-8")
    
    words = len(full_manuscript.split())
    chars = len(full_manuscript)
    lines = len(full_manuscript.splitlines())
    print(f"Total Words: {words} | Total Chars: {chars} | Total Lines: {lines}")
    
    # 1. Compile Full PDF
    styles = get_book_styles()
    story = parse_markdown_to_story(full_manuscript, styles)
    
    temp_body_pdf = BASE_DIR / "temp_master_body.pdf"
    doc = SimpleDocTemplate(
        str(temp_body_pdf),
        pagesize=(PAGE_W, PAGE_H),
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN
    )
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Body PDF compiled.")
    
    # Prepend full-bleed cover
    cover_doc = fitz.open()
    cover_page = cover_doc.new_page(width=PAGE_W, height=PAGE_H)
    cover_page.insert_image(fitz.Rect(0, 0, PAGE_W, PAGE_H), filename=str(COVER_IMG))
    
    body_doc = fitz.open(str(temp_body_pdf))
    cover_doc.insert_pdf(body_doc)
    cover_doc.save(str(PDF_OUT_FULL))
    final_pages = len(cover_doc)
    cover_doc.close()
    body_doc.close()
    
    if temp_body_pdf.exists():
        temp_body_pdf.unlink()
        
    print(f"✨ MASTER PUBLICATION PDF GENERATED: {PDF_OUT_FULL} ({final_pages} pages).")
    
    # 2. Compile EPUB
    book = epub.EpubBook()
    book.set_identifier("urn:isbn:adorise-hum-ladte-nahi-bestseller-2026")
    book.set_title("Hum Ladte Nahi, Par Baat Nahi Karte")
    book.set_language("hi-Latn")
    book.add_author("Sanjay Shharma")
    book.add_metadata('DC', 'description', 'Complete Trade Bestseller Edition by Sanjay Shharma (IIM Calcutta Alumni). Published by Adorise Digital.')
    book.add_metadata('DC', 'publisher', 'Adorise Digital')
    
    with open(COVER_IMG, 'rb') as f:
        book.set_cover("cover.jpg", f.read())
        
    raw_sections = re.split(r'\n(?=## Chapter|## Bonus Toolkit|## 50 Hinglish|# PART|# BONUS|# EPILOGUE|# BACK MATTER|## Copyright|## Author|## Introduction)', full_manuscript)
    spine = ['nav']
    toc = []
    
    for idx, sec in enumerate(raw_sections):
        sec = sec.strip()
        if not sec:
            continue
        first_line = sec.splitlines()[0].strip("# ").strip()
        title = first_line.split("\n")[0].strip("*()")
        if not title:
            title = f"Section {idx+1}"
            
        html_content = markdown.markdown(sec, extensions=['tables', 'fenced_code'])
        styled_html = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
<title>{title}</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #2D3748; padding: 4%; }}
h1, h2, h3 {{ color: #8C2D19; }}
blockquote {{ border-left: 3px solid #8C2D19; padding-left: 12px; margin-left: 0; color: #4A5568; font-style: italic; background: #F7FAFC; padding: 8px 12px; }}
table {{ border-collapse: collapse; width: 100%; margin: 16px 0; }}
th, td {{ border: 1px solid #CBD5E0; padding: 6px 8px; text-align: left; font-size: 0.85em; }}
th {{ background-color: #2C3E50; color: #FFFFFF; }}
tr:nth-child(even) {{ background-color: #F7FAFC; }}
</style>
</head>
<body>
{html_content}
</body>
</html>
"""
        c_item = epub.EpubHtml(title=title, file_name=f"section_{idx:02d}.xhtml", lang="hi-Latn")
        c_item.content = styled_html.encode('utf-8')
        book.add_item(c_item)
        spine.append(c_item)
        toc.append(c_item)

    book.toc = tuple(toc)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = spine
    epub.write_epub(str(EPUB_OUT), book, {})
    print(f"REFLOWABLE EPUB GENERATED: {EPUB_OUT}")

    # 3. Compile Lead Magnet Preview (Chapters 1-3 + CTA)
    build_preview_pdf(styles)

def build_preview_pdf(styles):
    from text_front_matter import FRONT_MATTER
    from text_part1 import PART1_TEXT
    
    idx_ch4 = PART1_TEXT.find("## Chapter 4:")
    p1_preview = PART1_TEXT[:idx_ch4].strip() if idx_ch4 != -1 else PART1_TEXT
    
    cta_text = """
---

# GET THE COMPLETE 14-CHAPTER BESTSELLER EDITION

## Unlock the Full 4-Phase System, Epilogue & 4 Reconnection Toolkits

Aapne abhi *Hum Ladte Nahi, Par Baat Nahi Karte* ke pehle 3 chapters padhe hain. Yeh sirf shuruat hai. 

Rishte ko sach mein theek karne ke liye, aage ki kitaab aapko step-by-step un muddo par le jaati hai jinse har Indian parivar guzar raha hai:

### What's Inside the Complete Edition:
- **Part 2: DECODE**
  - **Chapter 5:** Sasural, Mayka aur WhatsApp Family Dynamics (The Mother-Son-Wife Triad & Primary Shielding Protocol).
  - **Chapter 6:** The 4 Horsemen of Indian Marriages (Taane, Criticism, Defensiveness, Stonewalling — and the 8 healing sentences).
- **Part 3: REPAIR — The 30-Day Reconnection Protocol**
  - **Chapter 7:** Sirf Pyaar Kaafi Kyun Nahi Hota? (The 4 Engines: Physical, Intellectual, Emotional, Spiritual).
  - **Chapter 8:** Panch Micro-Conversations Jo Rishte Ko Zinda Rakhti Hain (10-minute daily rituals).
  - **Chapter 9:** Hafte Ke Teen Rituals Jo Rishte Ko Bachate Hain (Balcony chai, walks, date nights without guilt).
  - **Chapter 10:** 7-Day Physical Reconnection & The Touch Ladder (Safe affection to intimacy).
  - **Chapter 11:** Bharosa Dobara Banane Ka Tareeka & The 4-Part Clean Apology.
  - **Chapter 12:** Clean Fighting (Mudde par ladna, insaan ko zaleel kiye bina).
- **Part 4: FUTURE-PROOF**
  - **Chapter 13:** The Sandwich Generation Dilemma (Elderly parents, teenage kids, and marriage).
  - **Chapter 14:** The Forever Plan (Saath budhe hone ka 10-year roadmap).
- **Epilogue:** What Comes After the Last Page.
- **4 Comprehensive Bonus Toolkits:**
  - **Toolkit I:** The Re-Entry Menu & 30-Day Daily Protocol (Day 1 to 30 matrix).
  - **Toolkit II:** The Talking Points Repair Manual (10 Word-for-Word Desi Living Room Scripts).
  - **Toolkit III:** The Lie Map (The 10 unspoken lies Indian couples tell themselves and the truth).
  - **Toolkit IV:** The Forever Plan Workbook (Guided worksheets).
- **50 Hinglish Conversation Starters** with detailed instructions.
- **Complete Author & Ecosystem Showcase** (All 48 books catalog).

---

### Instant Download & Full Access:
- **Official Bookstore & Previews:** [books.adorisedigital.com](https://books.adorisedigital.com)
- **Direct Gumroad Link:** [adorisedigital.gumroad.com/l/hum-ladte-nahi](https://adorisedigital.gumroad.com/l/hum-ladte-nahi)
- **Includes:** Full Publication PDF + EPUB for Kindle/Apple Books + Printable Trackers & HD Covers.
"""
    preview_md = f"{FRONT_MATTER.strip()}\n\n---\n\n{p1_preview}\n\n{cta_text}"
    story = parse_markdown_to_story(preview_md, styles)
    
    temp_body_pdf = BASE_DIR / "temp_preview_body.pdf"
    doc = SimpleDocTemplate(
        str(temp_body_pdf),
        pagesize=(PAGE_W, PAGE_H),
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN
    )
    doc.build(story, canvasmaker=NumberedCanvas)
    
    cover_doc = fitz.open()
    cover_page = cover_doc.new_page(width=PAGE_W, height=PAGE_H)
    cover_page.insert_image(fitz.Rect(0, 0, PAGE_W, PAGE_H), filename=str(COVER_IMG))
    
    body_doc = fitz.open(str(temp_body_pdf))
    cover_doc.insert_pdf(body_doc)
    cover_doc.save(str(PDF_OUT_PREVIEW))
    prev_pages = len(cover_doc)
    cover_doc.close()
    body_doc.close()
    
    if temp_body_pdf.exists():
        temp_body_pdf.unlink()
        
    print(f"LEAD MAGNET PREVIEW PDF GENERATED: {PDF_OUT_PREVIEW} ({prev_pages} pages).")

if __name__ == "__main__":
    main()
