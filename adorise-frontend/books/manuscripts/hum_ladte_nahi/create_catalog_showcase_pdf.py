import os
import sys
from pathlib import Path
from reportlab.lib.pagesizes import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, HRFlowable

BASE_DIR = Path(r"C:\Users\HOME_PC\Documents\antigravity\calm-carson\adorise-frontend\books\manuscripts\hum_ladte_nahi")
OUTPUT_PDF = BASE_DIR / "temp_catalog_showcase_2pages.pdf"

PAGE_W = 432.0  # 6.0 in
PAGE_H = 648.0  # 9.0 in
MARGIN = 28.0   # 0.39 in margins for maximum readable content

def build_catalog_showcase():
    styles = getSampleStyleSheet()
    
    c_primary = colors.HexColor("#1A202C")
    c_accent = colors.HexColor("#8C2D19")
    c_navy = colors.HexColor("#1A365D")
    
    title_style = ParagraphStyle('CTitle', fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=c_accent, alignment=1, spaceAfter=2)
    sub_style = ParagraphStyle('CSub', fontName='Helvetica', fontSize=7.0, leading=9.5, textColor=colors.HexColor("#4A5568"), alignment=1, spaceAfter=4)
    sec_hdr = ParagraphStyle('CSec', fontName='Helvetica-Bold', fontSize=8.5, leading=11.5, textColor=colors.HexColor("#2C3E50"), spaceBefore=3, spaceAfter=2)
    
    p_num = ParagraphStyle('PNum', fontName='Helvetica-Bold', fontSize=6.5, leading=8.5, textColor=c_accent)
    p_name = ParagraphStyle('PName', fontName='Helvetica-Bold', fontSize=6.5, leading=8.5, textColor=c_primary)
    p_desc = ParagraphStyle('PDesc', fontName='Helvetica', fontSize=6.0, leading=8.0, textColor=colors.HexColor("#4A5568"))
    p_price = ParagraphStyle('PPrice', fontName='Helvetica-Bold', fontSize=6.0, leading=8.0, textColor=c_navy, alignment=2)
    
    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=(PAGE_W, PAGE_H),
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN
    )
    story = []
    
    # ==================== PAGE 1: CARE COLLECTION (14) + AI SUITE (10) = 24 BOOKS ====================
    story.append(Paragraph("THE 48-BOOK MASTER AUTHOR CATALOG — PART 1", title_style))
    story.append(Paragraph("All Titles Available in Master PDF + Reflowable Kindle EPUB at <u>books.adorisedigital.com</u>", sub_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceAfter=4, spaceBefore=0))
    
    # --- The Care Collection (14 Titles) ---
    story.append(Paragraph("<b>The Care Collection (14 Flagship Titles • Marriage, Family Dynamics & Resilience)</b>", sec_hdr))
    
    care_14 = [
        ("01", "Hum Ladte Nahi, Par Baat Hi Nahi Karte", "Silent Indian Marriages: 14 Chapters, 6 Toolkits, 12 Stories", "$9.99 / ₹899"),
        ("02", "The Quiet Care: When Someone You Love Is Sick", "Essential Family Caregiver Survival Guide for Chronic Illness", "$9.99 / ₹899"),
        ("03", "Still Married, Just Silent", "14 Conversations to Reopen Intimacy in Long-Term Marriages", "$9.99 / ₹899"),
        ("04", "When They Forget Your Name", "Compassionate Communication & Memory Care for Alzheimer's", "$9.99 / ₹899"),
        ("05", "The Long Goodbye", "Healing After the Loss of a Spouse: Bereavement Manual", "$9.99 / ₹899"),
        ("06", "The Long Hello", "Finding Meaning, Self & Reconnection After Deep Loss", "$9.99 / ₹899"),
        ("07", "The Second Chapter", "Life, Purpose, and Marital Reconnection After 50", "$9.99 / ₹899"),
        ("08", "The Second Honeymoon", "Midlife Romance, Sexual Intimacy, and Rediscovery", "$9.99 / ₹899"),
        ("09", "The Last Sandwich", "Caring for Aging Parents & Teens Without Marital Burnout", "$9.99 / ₹899"),
        ("10", "The Friends Who Fade", "Adult Friendship Drift & Rebuilding Community After 40", "$9.99 / ₹899"),
        ("11", "The Survivor", "Resilience, Hope & Post-Traumatic Growth After Crisis", "$9.99 / ₹899"),
        ("12", "Gray Divorce", "Dignified Separation, Asset Division & Autonomy After 50", "$9.99 / ₹899"),
        ("13", "Remarried at 60", "Late-Life Love, Blended Families & Estate Protection", "$9.99 / ₹899"),
        ("14", "After the Last Goodbye", "Sudden Loss & Emotional Recovery for Senior Executives", "$9.99 / ₹899"),
    ]
    
    t1_data = []
    for num, title, desc, pr in care_14:
        t1_data.append([
            Paragraph(f"#{num}", p_num),
            Paragraph(f"<b>{title}</b><br/>{desc}", p_name),
            Paragraph(pr, p_price)
        ])
    
    t1 = Table(t1_data, colWidths=[20, 296, 60])
    t1.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ('LINEBELOW', (0,0), (-1,-1), 0.3, colors.HexColor("#EDF2F7")),
    ]))
    story.append(t1)
    story.append(Spacer(1, 3))
    
    # --- The AI Wealth & Autonomous Agency Suite (10 Titles) ---
    story.append(Paragraph("<b>The AI Wealth & Autonomous Agency Suite (10 Production Systems)</b>", sec_hdr))
    
    ai_10 = [
        ("15", "The AI Agent Blueprint", "Autonomous Multi-Agent Architecture for Modern Businesses", "$19.99 / ₹1,899"),
        ("16", "The AI Agency Playbook", "Scaling Client Automation Retainers to $10k/mo Without Code", "$19.99 / ₹1,899"),
        ("17", "The AI Content Agent", "Autonomous 9:16 Video, Social Scheduling & pSEO Engines", "$19.99 / ₹1,899"),
        ("18", "The AI Agent Action Workbook", "Step-by-Step Implementation Protocols & Client Blueprints", "$19.99 / ₹1,899"),
        ("19", "The AI Agent Cheat Sheets & System Prompts", "Production Prompt Engineering & LLM Routing Templates", "$19.99 / ₹1,899"),
        ("20", "Never Miss Another Call: The AI Receptionist Engine", "24/7 Autonomous Voice Agents for SMB Client Triage", "$19.99 / ₹1,899"),
        ("21", "The AI Receptionist Blueprint", "Technical Telephony, SIP Trunking & Latency Optimization", "$19.99 / ₹1,899"),
        ("22", "The AI Receptionist Buyer's Guide", "ROI Matrix, Vendor Evaluation & Implementation Roadmap", "$19.99 / ₹1,899"),
        ("23", "AI Front Desk for HVAC, Plumbing & Home Services", "Instant Emergency Dispatch & CRM Ingestion Workflows", "$19.99 / ₹1,899"),
        ("24", "AI Front Desk for Law Firms, Dentists & Real Estate", "Confidential Intake, Appointment Booking & Retainer Triage", "$19.99 / ₹1,899"),
    ]
    
    t2_data = []
    for num, title, desc, pr in ai_10:
        t2_data.append([
            Paragraph(f"#{num}", p_num),
            Paragraph(f"<b>{title}</b><br/>{desc}", p_name),
            Paragraph(pr, p_price)
        ])
    
    t2 = Table(t2_data, colWidths=[20, 296, 60])
    t2.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 1.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ('LINEBELOW', (0,0), (-1,-1), 0.3, colors.HexColor("#EDF2F7")),
    ]))
    story.append(t2)
    
    # ==================== PAGE 2: INDIAN WEALTH (24 TITLES) + STORE ACCESS ====================
    story.append(PageBreak())
    
    story.append(Paragraph("THE 48-BOOK MASTER AUTHOR CATALOG — PART 2", title_style))
    story.append(Paragraph("The Indian Wealth & Financial Freedom Series (24 Titles • 8 Tactical Modules)", sub_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_accent, spaceAfter=4, spaceBefore=0))
    
    wealth_24 = [
        ("25", "CIBIL Repair • Book 1", "7-Step Credit Score Audit & Discrepancy Checklist", "$9.99 / ₹899"),
        ("26", "CIBIL Repair • Book 2", "Tactical Score Rebuilding Manual (DPD & Settlement Removal)", "$9.99 / ₹899"),
        ("27", "CIBIL Repair • Book 3", "Legal Dispute Templates, Ombudsman Complaints & Bank Drafts", "$9.99 / ₹899"),
        ("28", "Home Loan Approval • Book 1", "7-Step Eligibility Audit & CIBIL Pre-Screening Checklist", "$9.99 / ₹899"),
        ("29", "Home Loan Approval • Book 2", "Tactical Underwriting Manual & Lowest Rate Negotiation Guide", "$9.99 / ₹899"),
        ("30", "Home Loan Approval • Book 3", "Legal Property Verification & Encumbrance Dispute Drafts", "$9.99 / ₹899"),
        ("31", "Business Loan Approval • Book 1", "MSME & Working Capital Eligibility Audit Checklist", "$9.99 / ₹899"),
        ("32", "Business Loan Approval • Book 2", "Tactical Balance Sheet Optimization & CMA Data Preparation", "$9.99 / ₹899"),
        ("33", "Business Loan Approval • Book 3", "Collateral Structuring, CGTMSE & Bank Sanction Legal Drafts", "$9.99 / ₹899"),
        ("34", "Credit Card Hacks • Book 1", "Reward Point Maximization & Annual Fee Waiver Audit", "$9.99 / ₹899"),
        ("35", "Credit Card Hacks • Book 2", "Tactical Credit Limit Escalation & Balance Transfer Manual", "$9.99 / ₹899"),
        ("36", "Credit Card Hacks • Book 3", "Chargeback Dispute Drafts & Unauthorized Transaction Notices", "$9.99 / ₹899"),
        ("37", "Debt Settlement • Book 1", "Illegal Recovery Agent Harassment Firewall & Rights Audit", "$9.99 / ₹899"),
        ("38", "Debt Settlement • Book 2", "Tactical One-Time Settlement (OTS) Negotiation Manual (40-60% Waiver)", "$9.99 / ₹899"),
        ("39", "Debt Settlement • Book 3", "Legal Notices Against Coercion, Police Complaints & RBI Escalations", "$9.99 / ₹899"),
        ("40", "Get Hired Remote • Book 1", "30-Day Global Resume, Portfolio & LinkedIn Optimization Audit", "$9.99 / ₹899"),
        ("41", "Get Hired Remote • Book 2", "Tactical US/EU Client Cold Outreach & Interview Frameworks", "$9.99 / ₹899"),
        ("42", "Get Hired Remote • Book 3", "International Invoicing, 44ADA Taxation & W-8BEN Contract Drafts", "$9.99 / ₹899"),
        ("43", "GST Filing Mastery • Book 1", "Monthly GSTR-1, 3B & Annual Return Reconciliation Audit", "$9.99 / ₹899"),
        ("44", "GST Filing Mastery • Book 2", "Tactical Input Tax Credit (ITC) Protection & Audit Preparation", "$9.99 / ₹899"),
        ("45", "GST Filing Mastery • Book 3", "Legal Show-Cause Notice Replies (ASMT-10) & DRC-01 Dispute Drafts", "$9.99 / ₹899"),
        ("46", "GST Refund Bible • Book 1", "Export (LUT) & Inverted Duty Structure Eligibility Audit", "$9.99 / ₹899"),
        ("47", "GST Refund Bible • Book 2", "Tactical Departmental Refund Processing & Escalation Manual", "$9.99 / ₹899"),
        ("48", "GST Refund Bible • Book 3", "Legal Deficiency Memo Replies (RFD-03) & Appellate Authority Appeals", "$9.99 / ₹899"),
    ]
    
    t3_data = []
    for num, title, desc, pr in wealth_24:
        t3_data.append([
            Paragraph(f"#{num}", p_num),
            Paragraph(f"<b>{title}</b>: {desc}", p_name),
            Paragraph(pr, p_price)
        ])
        
    t3 = Table(t3_data, colWidths=[20, 296, 60])
    t3.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 1.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ('LINEBELOW', (0,0), (-1,-1), 0.3, colors.HexColor("#EDF2F7")),
    ]))
    story.append(t3)
    story.append(Spacer(1, 4))
    
    # Storefront Footer Box
    box_p = ParagraphStyle('BoxP', fontName='Helvetica', fontSize=6.5, leading=8.5, textColor=colors.HexColor("#2D3748"))
    box_data = [[
        Paragraph(
            "<b>WHERE TO GET ALL 48 TITLES INSTANTLY:</b><br/>"
            "• <b>Official Digital Bookstore:</b> <u>https://books.adorisedigital.com</u> (UPI, QR Code, Netbanking & Cards)<br/>"
            "• <b>Global Storefront (Gumroad):</b> <u>https://adorisedigital.gumroad.com</u> (USD / Apple Pay / All Cards)<br/>"
            "• <b>Support & Assistance:</b> <u>support@adorisedigital.com</u> • Published by Adorise Digital (Trendy DigiStore LLC, WY, USA)",
            box_p
        )
    ]]
    box_t = Table(box_data, colWidths=[376])
    box_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F9F7F2")),
        ('BOX', (0,0), (-1,-1), 1, c_accent),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(box_t)
    
    doc.build(story)
    print(f"Complete 48-Book Master Catalog Showcase generated: {OUTPUT_PDF}")

if __name__ == "__main__":
    build_catalog_showcase()
