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

BASE_DIR = Path(r"C:\Users\HOME_PC\Documents\antigravity\calm-carson\adorise-frontend\books\manuscripts\hum_ladte_nahi")
COMPLETE_MD = BASE_DIR / "book_manuscript_complete.md"
COVER_IMG = Path(r"C:\Users\HOME_PC\Documents\antigravity\calm-carson\adorise-frontend\books\previews\Care Collection Lead magnets\Hum_Ladte_Nahi_Real_Cover.jpg")
SQUARE_IMG = Path(r"C:\Users\HOME_PC\Documents\antigravity\calm-carson\adorise-frontend\books\previews\Care Collection Lead magnets\Hum_Ladte_Nahi_Real_Square_Thumbnail.jpg")

PDF_OUT_FULL = BASE_DIR / "Hum_Ladte_Nahi_Par_Baat_Hi_Nahi_Karte.pdf"
EPUB_OUT = BASE_DIR / "Hum_Ladte_Nahi_Par_Baat_Hi_Nahi_Karte.epub"
PDF_OUT_PREVIEW = BASE_DIR / "Hum_Ladte_Nahi_3_Chapter_Preview.pdf"

PAGE_W = 6.0 * 72.0  # 432 pt
PAGE_H = 9.0 * 72.0  # 648 pt
MARGIN = 44.0

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
        # Front matter (pages 1 to 4): no header/footer
        if self._pageNumber <= 3:
            return
        self.saveState()
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#666666"))
        
        # Running Header
        if self._pageNumber % 2 == 0:
            self.drawString(MARGIN, PAGE_H - 34, "HUM LADTE NAHI, PAR BAAT NAHI KARTE")
        else:
            self.drawRightString(PAGE_W - MARGIN, PAGE_H - 34, "SANJAY SHHARMA • THE CARE COLLECTION")
            
        self.setStrokeColor(colors.HexColor("#D8D2C4"))
        self.setLineWidth(0.5)
        self.line(MARGIN, PAGE_H - 38, PAGE_W - MARGIN, PAGE_H - 38)
        
        # Running Footer (Bottom Centered Page Number)
        self.drawCentredString(PAGE_W / 2.0, 30, f"- {self._pageNumber} -")
        self.restoreState()

def get_book_styles():
    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_primary = colors.HexColor("#1A202C")
    c_accent = colors.HexColor("#8C2D19")
    c_sub = colors.HexColor("#4A5568")
    
    styles.add(ParagraphStyle(
        'BookTitle',
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=c_accent,
        alignment=1, # Center
        spaceAfter=8
    ))
    styles.add(ParagraphStyle(
        'BookSubtitle',
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=c_sub,
        alignment=1,
        spaceAfter=15
    ))
    styles.add(ParagraphStyle(
        'BookAuthor',
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_primary,
        alignment=1,
        spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        'BookCredentials',
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=c_sub,
        alignment=1,
        spaceAfter=25
    ))
    styles.add(ParagraphStyle(
        'PartHeader',
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#2D3748"),
        alignment=1,
        spaceBefore=15,
        spaceAfter=15
    ))
    styles.add(ParagraphStyle(
        'ChapterHeader',
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=c_accent,
        spaceBefore=18,
        spaceAfter=6,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        'ChapterSubtitle',
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=14,
        textColor=c_sub,
        spaceAfter=12,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        'SectionHeader',
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor("#2C3E50"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        'BookBody',
        fontName='Helvetica',
        fontSize=9.5,
        leading=14.0,
        textColor=c_primary,
        spaceAfter=8
    ))
    styles.add(ParagraphStyle(
        'BookBodyBold',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=14.0,
        textColor=c_primary,
        spaceAfter=8
    ))
    styles.add(ParagraphStyle(
        'BookBullet',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=c_primary,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        'CalloutText',
        fontName='Helvetica-Oblique',
        fontSize=9.0,
        leading=13.5,
        textColor=colors.HexColor("#2D3748"),
        spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        'CalloutBold',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=14.0,
        textColor=c_accent,
        spaceAfter=4
    ))
    styles.add(ParagraphStyle(
        'TableHead',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.white,
        alignment=0
    ))
    styles.add(ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=8.0,
        leading=11.0,
        textColor=c_primary,
        alignment=0
    ))
    styles.add(ParagraphStyle(
        'TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=8.0,
        leading=11.0,
        textColor=c_primary,
        alignment=0
    ))
    styles.add(ParagraphStyle(
        'Epigraph',
        fontName='Helvetica-Oblique',
        fontSize=10.5,
        leading=15.0,
        textColor=colors.HexColor("#333333"),
        alignment=1,
        spaceBefore=20,
        spaceAfter=15
    ))
    styles.add(ParagraphStyle(
        'SmallLegal',
        fontName='Helvetica',
        fontSize=7.5,
        leading=10.5,
        textColor=colors.HexColor("#555555"),
        spaceAfter=6
    ))
    return styles

def parse_markdown_to_story(md_text, styles, is_preview=False):
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
                # Bold formatting
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
            # Format table
            num_cols = len(table_data[0])
            total_w = PAGE_W - 2 * MARGIN
            if num_cols == 2:
                col_w = [total_w * 0.35, total_w * 0.65]
            elif num_cols == 3:
                col_w = [total_w * 0.25, total_w * 0.35, total_w * 0.40]
            elif num_cols == 4:
                col_w = [total_w * 0.18, total_w * 0.22, total_w * 0.48, total_w * 0.12]
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
                    elif c_idx == 0 or cell_text.startswith("<b>"):
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
        
        # Mermaid code block ignore or handle
        if raw_s.startswith("```mermaid"):
            in_mermaid = True
            i += 1
            continue
        if in_mermaid:
            if raw_s.startswith("```"):
                in_mermaid = False
            i += 1
            continue

        # Check callouts
        if raw_s.startswith(">"):
            if not in_callout:
                if in_table:
                    flush_table()
                in_callout = True
            callout_lines.append(raw_s)
            i += 1
            continue
        elif in_callout and raw_s:
            # continuation of callout
            callout_lines.append(raw_s)
            i += 1
            continue
        elif in_callout and not raw_s:
            flush_callout()
            i += 1
            continue

        # Check tables
        if raw_s.startswith("|") and raw_s.endswith("|"):
            if not in_table:
                in_table = True
            # Check if divider line
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

        # Horizontal rule / Page break
        if raw_s == "---":
            story.append(Spacer(1, 10))
            story.append(HRFlowable(width="80%", thickness=0.5, color=colors.HexColor("#D8D2C4"), spaceAfter=15, spaceBefore=10))
            i += 1
            continue

        # Part Header
        if raw_s.startswith("# PART") or raw_s.startswith("# BONUS") or raw_s.startswith("# ABOUT"):
            story.append(PageBreak())
            story.append(Spacer(1, 40))
            part_title = raw_s.lstrip("#").strip()
            story.append(Paragraph(part_title, styles['PartHeader']))
            story.append(HRFlowable(width="50%", thickness=1.5, color=colors.HexColor("#8C2D19"), spaceAfter=20, spaceBefore=10))
            i += 1
            continue

        # Chapter Header (H2)
        if raw_s.startswith("## Chapter") or raw_s.startswith("## Toolkit"):
            story.append(PageBreak())
            ch_title = raw_s.lstrip("#").strip()
            # If next line is subtitle *(...)*
            sub_text = ""
            if i + 1 < len(lines) and lines[i+1].strip().startswith("*(") and lines[i+1].strip().endswith(")*"):
                sub_text = lines[i+1].strip().strip("*()").strip()
                i += 1
            story.append(Spacer(1, 15))
            story.append(Paragraph(ch_title, styles['ChapterHeader']))
            if sub_text:
                story.append(Paragraph(f"<i>({sub_text})</i>", styles['ChapterSubtitle']))
            i += 1
            continue

        # Other H2
        if raw_s.startswith("## "):
            h2_text = raw_s.lstrip("#").strip()
            if "Copyright" in h2_text or "Dedication" in h2_text or "Author's Note" in h2_text:
                story.append(PageBreak())
            story.append(Spacer(1, 10))
            story.append(Paragraph(h2_text, styles['SectionHeader']))
            i += 1
            continue

        # Section H3
        if raw_s.startswith("### "):
            h3_text = raw_s.lstrip("#").strip()
            story.append(Spacer(1, 8))
            story.append(Paragraph(h3_text, styles['SectionHeader']))
            i += 1
            continue

        # Book Title front matter
        if raw_s.startswith("# Hum Ladte Nahi"):
            story.append(Spacer(1, 50))
            story.append(Paragraph("Hum Ladte Nahi, Par Baat Nahi Karte", styles['BookTitle']))
            i += 1
            continue
        if raw_s.startswith("### A 4-Phase Framework"):
            story.append(Paragraph("A 4-Phase Framework for the Silent Indian Marriage", styles['BookSubtitle']))
            story.append(Spacer(1, 40))
            i += 1
            continue
        if raw_s.startswith("**Authored by Sanjay Shharma**"):
            story.append(Paragraph("Sanjay Shharma", styles['BookAuthor']))
            i += 1
            continue
        if raw_s.startswith("*M.Sc., MBA, APSCM"):
            story.append(Paragraph("M.Sc., MBA, APSCM (IIM Calcutta Alumni)<br/>Author of <i>The Care Collection</i>", styles['BookCredentials']))
            story.append(Spacer(1, 50))
            story.append(Paragraph("Published by Adorise Digital<br/>Trendy DigiStore LLC, Wyoming, USA", styles['BookCredentials']))
            story.append(PageBreak())
            i += 1
            continue

        # Bullet points or numbered items
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

        # Standard Paragraph
        p_text = raw_s
        p_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', p_text)
        p_text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', p_text)
        # Markdown links: [text](url) -> <font color="#8C2D19"><u>text</u></font>
        p_text = re.sub(r'\[(.*?)\]\(.*?\)', r'<font color="#8C2D19"><u>\1</u></font>', p_text)

        # Check if legal / copyright page
        if "Copyright ©" in p_text or "All rights reserved" in p_text or "Disclaimer:" in p_text or "Confidential Helplines" in p_text:
            story.append(Paragraph(p_text, styles['SmallLegal']))
        elif p_text.startswith("<b>") and len(p_text) < 80:
            story.append(Paragraph(p_text, styles['BookBodyBold']))
        else:
            story.append(Paragraph(p_text, styles['BookBody']))

        i += 1

    if in_callout:
        flush_callout()
    if in_table:
        flush_table()

    return story

def create_front_cover_pdf(temp_cover_path):
    doc = fitz.open()
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page.insert_image(fitz.Rect(0, 0, PAGE_W, PAGE_H), filename=str(COVER_IMG))
    doc.save(str(temp_cover_path))
    doc.close()
    print("Temporary cover PDF created.")

def build_complete_pdf():
    md_text = COMPLETE_MD.read_text(encoding="utf-8")
    styles = get_book_styles()
    story = parse_markdown_to_story(md_text, styles, is_preview=False)
    
    temp_body_pdf = BASE_DIR / "temp_body.pdf"
    doc = SimpleDocTemplate(
        str(temp_body_pdf),
        pagesize=(PAGE_W, PAGE_H),
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN
    )
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Body PDF compiled: {temp_body_pdf}")
    
    # Prepend cover
    temp_cover_pdf = BASE_DIR / "temp_cover.pdf"
    create_front_cover_pdf(temp_cover_pdf)
    
    # Merge cover + body using PyMuPDF
    final_doc = fitz.open(str(temp_cover_pdf))
    body_doc = fitz.open(str(temp_body_pdf))
    final_doc.insert_pdf(body_doc)
    final_doc.save(str(PDF_OUT_FULL))
    final_page_count = len(final_doc)
    final_doc.close()
    body_doc.close()
    
    # Cleanup temp files
    if temp_body_pdf.exists():
        temp_body_pdf.unlink()
    if temp_cover_pdf.exists():
        temp_cover_pdf.unlink()
        
    print(f"Master Full PDF successfully built: {PDF_OUT_FULL} ({final_page_count} pages).")
    return final_page_count

def build_preview_pdf():
    # Extracts Front Matter + Part 1 (Chapters 1 to 3) + CTA Page
    p1_text = (BASE_DIR / "book_manuscript_part1.md").read_text(encoding="utf-8")
    # Stop before Chapter 4
    idx_ch4 = p1_text.find("## Chapter 4:")
    if idx_ch4 != -1:
        p1_preview = p1_text[:idx_ch4].strip()
    else:
        p1_preview = p1_text
        
    cta_text = """
---

# GET THE COMPLETE 14-CHAPTER EDITION

## Unlock the Full 4-Phase System & Reconnection Toolkits

Aapne abhi *Hum Ladte Nahi, Par Baat Nahi Karte* ke pehle 3 chapters padhe hain. Yeh sirf shuruat hai. 

Rishte ko sach mein theek karne ke liye, aage ki kitaab aapko step-by-step un muddo par le jaati hai jinse har Indian parivar guzar raha hai:

### What's Inside the Complete Edition:
- **Part 2: DECODE**
  - **Chapter 5:** In-laws, Joint Family Dynamics & The WhatsApp Group Politics.
  - **Chapter 6:** The 4 Horsemen of Indian Marriages (Taane, Criticism, Defensiveness, Stonewalling).
- **Part 3: REPAIR — The 30-Day Protocol**
  - **Chapter 7:** The 4 Engines of Marriage (Physical, Emotional, Intellectual, Spiritual).
  - **Chapter 8:** The 5 Micro-Conversations (10-minute daily rituals).
  - **Chapter 9:** The Weekly Ritual (Chai, walks, date nights without guilt).
  - **Chapter 10:** The 5-Rung Touch Ladder (Safe affection to intimacy).
  - **Chapter 11:** The 4-Part Clean Apology Formula.
  - **Chapter 12:** How to Fight Cleanly (Rules of engaged disagreement).
- **Part 4: FUTURE-PROOF**
  - **Chapter 13:** The Sandwich Generation (Balancing aging parents, kids, and marriage).
  - **Chapter 14:** The 10-Year Joint Life Vision.
- **4 Actionable Bonus Toolkits:**
  - **Toolkit 1:** The 30-Day Daily Reconnection Checklist.
  - **Toolkit 2:** 50 Hinglish Conversation Starters.
  - **Toolkit 3:** 10 Word-for-Word Desi Living Room Scripts.
  - **Toolkit 4:** The Emergency 5-Minute De-escalation Protocol.

---

### Instant Download & Access:
- **Official Bookstore:** [books.adorisedigital.com](https://books.adorisedigital.com)
- **Direct Gumroad Link:** [adorisedigital.gumroad.com/l/hum-ladte-nahi](https://adorisedigital.gumroad.com/l/hum-ladte-nahi)
- **Includes:** Full Publication 6x9 PDF + EPUB for Kindle/Apple Books + High-Res Covers & Printable Trackers.
"""
    full_preview_md = f"{p1_preview}\n\n{cta_text}"
    styles = get_book_styles()
    story = parse_markdown_to_story(full_preview_md, styles, is_preview=True)
    
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
    
    temp_cover_pdf = BASE_DIR / "temp_cover.pdf"
    create_front_cover_pdf(temp_cover_pdf)
    
    final_doc = fitz.open(str(temp_cover_pdf))
    body_doc = fitz.open(str(temp_body_pdf))
    final_doc.insert_pdf(body_doc)
    final_doc.save(str(PDF_OUT_PREVIEW))
    preview_page_count = len(final_doc)
    final_doc.close()
    body_doc.close()
    
    if temp_body_pdf.exists():
        temp_body_pdf.unlink()
    if temp_cover_pdf.exists():
        temp_cover_pdf.unlink()
        
    print(f"Lead Magnet 3-Chapter Preview PDF successfully built: {PDF_OUT_PREVIEW} ({preview_page_count} pages).")
    return preview_page_count

def build_epub():
    book = epub.EpubBook()
    book.set_identifier("urn:isbn:adorise-hum-ladte-nahi-2026")
    book.set_title("Hum Ladte Nahi, Par Baat Nahi Karte")
    book.set_language("hi-Latn")
    book.add_author("Sanjay Shharma")
    
    # Metadata
    book.add_metadata('DC', 'description', 'A 4-Phase Framework for the Silent Indian Marriage by Sanjay Shharma (IIM Calcutta Alumni). Published by Adorise Digital.')
    book.add_metadata('DC', 'publisher', 'Adorise Digital')
    
    # Cover Image
    with open(COVER_IMG, 'rb') as f:
        book.set_cover("cover.jpg", f.read())
        
    # Read markdown and convert to HTML chapters
    md_text = COMPLETE_MD.read_text(encoding="utf-8")
    
    # Split by major chapters (## Chapter or ## Toolkit or # PART)
    raw_sections = re.split(r'\n(?=## Chapter|## Toolkit|# PART|# Dedication|# Copyright|# Author|# ABOUT)', md_text)
    
    spine = ['nav']
    toc = []
    
    for idx, sec in enumerate(raw_sections):
        sec = sec.strip()
        if not sec:
            continue
        first_line = sec.splitlines()[0].strip("# ").strip()
        # Clean title
        title = first_line.split("\n")[0].strip("*()")
        if not title:
            title = f"Section {idx+1}"
            
        html_content = markdown.markdown(sec, extensions=['tables', 'fenced_code'])
        # Add minimal stylish CSS
        styled_html = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
<title>{title}</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #2D3748; padding: 5%; }}
h1, h2, h3 {{ color: #8C2D19; }}
blockquote {{ border-left: 3px solid #8C2D19; padding-left: 12px; margin-left: 0; color: #4A5568; font-style: italic; background: #F7FAFC; padding: 8px 12px; }}
table {{ border-collapse: collapse; width: 100%; margin: 16px 0; }}
th, td {{ border: 1px solid #CBD5E0; padding: 8px; text-align: left; font-size: 0.9em; }}
th {{ background-color: #EDF2F7; color: #1A202C; }}
tr:nth-child(even) {{ background-color: #F7FAFC; }}
</style>
</head>
<body>
{html_content}
</body>
</html>
"""
        c_item = epub.EpubHtml(title=title, file_name=f"chap_{idx:02d}.xhtml", lang="hi-Latn")
        c_item.content = styled_html.encode('utf-8')
        book.add_item(c_item)
        spine.append(c_item)
        toc.append(c_item)

    book.toc = tuple(toc)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = spine
    
    epub.write_epub(str(EPUB_OUT), book, {})
    print(f"EPUB successfully built: {EPUB_OUT}")

if __name__ == "__main__":
    p_full = build_complete_pdf()
    p_prev = build_preview_pdf()
    build_epub()
    print("All compilation jobs finished successfully!")
