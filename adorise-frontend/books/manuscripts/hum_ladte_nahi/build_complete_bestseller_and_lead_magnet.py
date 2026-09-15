import os
import sys
from pathlib import Path
import fitz  # PyMuPDF
from reportlab.lib.pagesizes import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

BASE_DIR = Path(r"C:\Users\HOME_PC\Documents\antigravity\calm-carson\adorise-frontend\books\manuscripts\hum_ladte_nahi")
ATTACHED_PDF = Path(r"C:\Users\HOME_PC\multica_workspaces_desktop-api.multica.ai\adorise-dig-01cd3226b372\task-ca271b3a9420\workdir\Hum_Ladte_Nahi_Par_Baat_Hi_Nahi_Karte-2.pdf")
COVER_IMG = Path(r"C:\Users\HOME_PC\Documents\antigravity\calm-carson\adorise-frontend\books\previews\Care Collection Lead magnets\Hum_Ladte_Nahi_Real_Cover.jpg")
SHOWCASE_PDF = BASE_DIR / "temp_catalog_showcase_2pages.pdf"

MASTER_PDF_OUT = BASE_DIR / "Hum_Ladte_Nahi_Par_Baat_Hi_Nahi_Karte.pdf"
PREVIEW_PDF_OUT = BASE_DIR / "Hum_Ladte_Nahi_3_Chapter_Preview.pdf"

PAGE_W = 432.0
PAGE_H = 648.0
MARGIN = 32.0

def build_about_author_page_pdf(output_path):
    styles = getSampleStyleSheet()
    c_accent = colors.HexColor("#8C2D19")
    c_navy = colors.HexColor("#1A365D")
    
    title_style = ParagraphStyle('AuthTitle', fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=c_accent, alignment=1, spaceAfter=4)
    sub_style = ParagraphStyle('AuthSub', fontName='Helvetica-Oblique', fontSize=8.5, leading=12, textColor=colors.HexColor("#4A5568"), alignment=1, spaceAfter=10)
    h2_style = ParagraphStyle('AuthH2', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=c_navy, spaceBefore=6, spaceAfter=3)
    p_style = ParagraphStyle('AuthP', fontName='Helvetica', fontSize=8.0, leading=11.5, textColor=colors.HexColor("#1A202C"), spaceAfter=5)
    box_p = ParagraphStyle('AuthBox', fontName='Helvetica', fontSize=7.0, leading=9.5, textColor=colors.HexColor("#2D3748"))
    
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=(PAGE_W, PAGE_H),
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN
    )
    story = []
    story.append(Spacer(1, 6))
    story.append(Paragraph("ABOUT THE AUTHOR & THE CARE MISSION", title_style))
    story.append(Paragraph("Executive Leadership, Lived Caregiving Resilience & Practical Marital Healing", sub_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceAfter=8, spaceBefore=0))
    
    story.append(Paragraph(
        "<b>Sanjay Shharma</b> is an Author, Corporate Strategist, and Executive Mentor holding an M.Sc., MBA, and APSCM from the prestigious <b>Indian Institute of Management (IIM) Calcutta</b>, with over three decades of corporate and business leadership experience.",
        p_style
    ))
    story.append(Paragraph(
        "Having walked the devastating path of caring for his beloved wife through terminal illness until her passing, Sanjay experienced firsthand the profound emotional silence, invisible caregiver fatigue, and psychological strain that modern urban couples endure behind closed doors.",
        p_style
    ))
    story.append(Paragraph(
        "Refusing to accept clinical, theoretical marital advice that fails to understand Indian family structures — in-laws, societal comparisons, unspoken expectations, and WhatsApp family groups — he authored <b>The Care Collection</b>: a groundbreaking 14-volume publishing ecosystem dedicated to restoring warmth, dignity, and honest friendship to modern Indian marriages.",
        p_style
    ))
    
    story.append(Paragraph("<b>Author Credentials & Verified Channels:</b>", h2_style))
    
    table_data = [
        [Paragraph("<b>Academic Alumni</b>", p_style), Paragraph("Indian Institute of Management Calcutta (IIM Calcutta)", p_style)],
        [Paragraph("<b>Publishing Division</b>", p_style), Paragraph("Adorise Digital • Trendy DigiStore LLC (Wyoming, USA)", p_style)],
        [Paragraph("<b>Official Bookstore</b>", p_style), Paragraph("<u>https://books.adorisedigital.com</u>", p_style)],
        [Paragraph("<b>Global Storefront</b>", p_style), Paragraph("<u>https://adorisedigital.gumroad.com</u>", p_style)],
        [Paragraph("<b>Author LinkedIn</b>", p_style), Paragraph("<u>linkedin.com/in/sanjayshharma</u>", p_style)],
        [Paragraph("<b>Author Instagram</b>", p_style), Paragraph("<u>instagram.com/sanjayshharma</u>", p_style)],
        [Paragraph("<b>Official Support</b>", p_style), Paragraph("<u>support@adorisedigital.com</u>", p_style)],
    ]
    t = Table(table_data, colWidths=[110, 258])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2C3E50")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
    ]))
    story.append(t)
    story.append(Spacer(1, 8))
    
    box_content = [[
        Paragraph(
            "<b>24/7 CONFIDENTIAL CRISIS & MENTAL HEALTH HELPLINES (INDIA):</b><br/>"
            "If you or your spouse are in acute distress, reach out immediately:<br/>"
            "• <b>Tele-MANAS (Govt of India):</b> 14416 or 1800-891-4416 (24/7, Toll-Free, Multi-lingual)<br/>"
            "• <b>Vandrevala Foundation:</b> +91 9999 666 555 (24/7 Professional Counseling)<br/>"
            "• <b>iCall (TISS Mumbai):</b> +91 9152987821 (Mon–Sat, 10 AM – 8 PM)",
            box_p
        )
    ]]
    box_t = Table(box_content, colWidths=[368])
    box_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F9F7F2")),
        ('BOX', (0,0), (-1,-1), 1, c_accent),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(box_t)
    
    doc.build(story)
    print(f"About Author Page PDF created: {output_path}")

def build_cta_page_pdf(output_path):
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CTATitle', fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=colors.HexColor("#8C2D19"), alignment=1, spaceAfter=6)
    sub_style = ParagraphStyle('CTASub', fontName='Helvetica-Oblique', fontSize=9.0, leading=12.5, textColor=colors.HexColor("#4A5568"), alignment=1, spaceAfter=10)
    h2_style = ParagraphStyle('CTAH2', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=colors.HexColor("#2C3E50"), spaceBefore=5, spaceAfter=3)
    p_style = ParagraphStyle('CTAP', fontName='Helvetica', fontSize=8.0, leading=11.5, textColor=colors.HexColor("#1A202C"), spaceAfter=4)
    bullet_style = ParagraphStyle('CTABullet', fontName='Helvetica', fontSize=7.5, leading=10.5, textColor=colors.HexColor("#1A202C"), leftIndent=10, firstLineIndent=-7, spaceAfter=2)
    box_p = ParagraphStyle('CTABox', fontName='Helvetica', fontSize=7.5, leading=10.5, textColor=colors.HexColor("#2D3748"), alignment=1)
    
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=(PAGE_W, PAGE_H),
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN
    )
    story = []
    story.append(Spacer(1, 6))
    story.append(Paragraph("UNLOCK THE COMPLETE 246-PAGE EDITION", title_style))
    story.append(Paragraph("Hum Ladte Nahi, Par Baat Hi Nahi Karte! • By Sanjay Shharma (IIM Calcutta Alumni)", sub_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#8C2D19"), spaceAfter=8, spaceBefore=0))
    
    story.append(Paragraph(
        "Aapne abhi is pustak ke pehle teen adhyay (Chapters 1–3) padhe hain. Yeh sirf us gahre safar ki shuruat hai jo aapki shaadi ko silence se dosti tak le jaata hai.",
        p_style
    ))
    
    story.append(Paragraph("<b>Complete 246-Page Edition Mein Kya Shamil Hai:</b>", h2_style))
    items = [
        "<b>Part 1: Diagnose (Chapters 1–4):</b> Roommate Marriage, 5 Stages of Drift, Invisible Mental Load, and Emotional Shutdown.",
        "<b>Part 2: Decode (Chapters 5–6):</b> Indian-Specific Traps (Saas, Mayka, Comparison, WhatsApp Groups) & Pattern Breakdown.",
        "<b>Part 3: Repair (Chapters 7–12):</b> 4 Engines of Marriage, 5 Micro-Conversations, Weekly Rituals, 7-Day Touch Ladder, Rebuilding Trust, and Clean Disagreements.",
        "<b>Part 4: Future-Proof (Chapters 13–14):</b> Sandwich Generation Survival & The 50-Year Forever Plan.",
        "<b>Part II: 6 Bonus Action Toolkits:</b> 30-Day Daily Protocol, Talking Points Repair Manual, Lie Map, Crisis Helplines, Family Conversations, and Financial Intimacy.",
        "<b>Part III & IV: Real Voices & Case Studies:</b> 12 first-person stories and 8 real Indian couple case studies with word-for-word breakthroughs.",
        "<b>Part V & VI: Appendices:</b> Academic citations, Hinglish glossary, and frequently asked relationship questions."
    ]
    for item in items:
        story.append(Paragraph(f"&bull;&nbsp; {item}", bullet_style))
        
    story.append(Spacer(1, 8))
    
    box_data = [[
        Paragraph(
            "<b>GET INSTANT LIFETIME DIGITAL ACCESS (PDF + KINDLE EPUB):</b><br/><br/>"
            "<b>Official Bookstore & Indian Domestic Payments (UPI / QR / Netbanking):</b><br/>"
            "<u>https://books.adorisedigital.com</u><br/><br/>"
            "<b>Global Checkout (Gumroad / Apple Pay / All International Cards):</b><br/>"
            "<u>https://adorisedigital.gumroad.com/l/hum-ladte-nahi</u><br/><br/>"
            "<i>Includes Master 246-Page PDF + Reflowable Kindle EPUB + Printable 30-Day Wall Tracker.</i>",
            box_p
        )
    ]]
    box_t = Table(box_data, colWidths=[PAGE_W - 2 * MARGIN])
    box_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F9F7F2")),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor("#8C2D19")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(box_t)
    
    doc.build(story)
    print(f"CTA Page PDF created: {output_path}")

def assemble_master_book():
    print("\n--- ASSEMBLING 249-PAGE FULL MASTER BOOK ---")
    
    # 1. Page 0: Full-bleed KDP Cover
    master_doc = fitz.open()
    cover_page = master_doc.new_page(width=PAGE_W, height=PAGE_H)
    cover_page.insert_image(fitz.Rect(0, 0, PAGE_W, PAGE_H), filename=str(COVER_IMG))
    
    # 2. Insert 246 pages from ATTACHED_PDF
    body_doc = fitz.open(str(ATTACHED_PDF))
    master_doc.insert_pdf(body_doc)
    body_doc.close()
    
    # 3. Insert 2-Page 48-Book Master Catalog Showcase
    showcase_doc = fitz.open(str(SHOWCASE_PDF))
    master_doc.insert_pdf(showcase_doc)
    showcase_doc.close()
    
    master_doc.save(str(MASTER_PDF_OUT))
    final_count = len(master_doc)
    master_doc.close()
    print(f"MASTER BOOK ASSEMBLED: {MASTER_PDF_OUT} ({final_count} pages).")
    return final_count

def assemble_lead_magnet():
    print("\n--- ASSEMBLING 37-PAGE LEAD MAGNET PREVIEW (WITH AUTHOR AT START) ---")
    temp_about_pdf = BASE_DIR / "temp_about_author_1page.pdf"
    build_about_author_page_pdf(temp_about_pdf)
    
    temp_cta_pdf = BASE_DIR / "temp_lead_magnet_cta.pdf"
    build_cta_page_pdf(temp_cta_pdf)
    
    prev_doc = fitz.open()
    
    # Page 0: Full-bleed KDP Cover
    cover_page = prev_doc.new_page(width=PAGE_W, height=PAGE_H)
    cover_page.insert_image(fitz.Rect(0, 0, PAGE_W, PAGE_H), filename=str(COVER_IMG))
    
    # Page 1: Title & Copyright from ATTACHED_PDF (page index 0)
    body_doc = fitz.open(str(ATTACHED_PDF))
    prev_doc.insert_pdf(body_doc, from_page=0, to_page=0)
    
    # Page 2: About the Author & Mission (AT THE START!)
    about_doc = fitz.open(str(temp_about_pdf))
    prev_doc.insert_pdf(about_doc)
    about_doc.close()
    
    # Pages 3-33: Complete Table of Contents (indices 1-3) + Dedication (4-5) + Intro (6-9) + Chapters 1-3 (10-31)
    prev_doc.insert_pdf(body_doc, from_page=1, to_page=31)
    body_doc.close()
    
    # Page 34: Unlock Complete Edition CTA Page
    cta_doc = fitz.open(str(temp_cta_pdf))
    prev_doc.insert_pdf(cta_doc)
    cta_doc.close()
    
    # Pages 35-36: The 2-Page 48-Book Master Catalog Showcase (Listing all 48 books by name!)
    showcase_doc = fitz.open(str(SHOWCASE_PDF))
    prev_doc.insert_pdf(showcase_doc)
    showcase_doc.close()
    
    prev_doc.save(str(PREVIEW_PDF_OUT))
    final_prev_count = len(prev_doc)
    prev_doc.close()
    
    if temp_about_pdf.exists():
        temp_about_pdf.unlink()
    if temp_cta_pdf.exists():
        temp_cta_pdf.unlink()
        
    print(f"LEAD MAGNET PREVIEW ASSEMBLED: {PREVIEW_PDF_OUT} ({final_prev_count} pages).")
    return final_prev_count

if __name__ == "__main__":
    assemble_master_book()
    assemble_lead_magnet()
