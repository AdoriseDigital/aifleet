import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

BASE_DIR = Path(r"C:\Users\HOME_PC\Documents\antigravity\calm-carson\adorise-frontend\books\manuscripts\hum_ladte_nahi")
TRACKER_PDF = BASE_DIR / "Hum_Ladte_Nahi_30_Day_Reconnection_Tracker.pdf"

styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'TTitle',
    fontName='Helvetica-Bold',
    fontSize=18,
    leading=22,
    textColor=colors.HexColor("#8C2D19"),
    alignment=1,
    spaceAfter=4
)
sub_style = ParagraphStyle(
    'TSub',
    fontName='Helvetica',
    fontSize=10,
    leading=14,
    textColor=colors.HexColor("#4A5568"),
    alignment=1,
    spaceAfter=12
)
th_style = ParagraphStyle(
    'THead',
    fontName='Helvetica-Bold',
    fontSize=8.5,
    leading=11,
    textColor=colors.white
)
cell_style = ParagraphStyle(
    'TCell',
    fontName='Helvetica',
    fontSize=8.0,
    leading=10.5,
    textColor=colors.HexColor("#1A202C")
)
cell_bold = ParagraphStyle(
    'TCellB',
    fontName='Helvetica-Bold',
    fontSize=8.0,
    leading=10.5,
    textColor=colors.HexColor("#8C2D19")
)

days_data = [
    ("Day 1", "Soft-Start", "Subah aankh khulte hi 60s eye contact + 'Good morning, aaj kaisa din rahega?'"),
    ("Day 2", "Curiosity", "Dopahar mein bina kisi kaam ya list ke ek gentle check-in message bhejiye."),
    ("Day 3", "Shielding", "Raat ko bed par aane se pehle phone ko 20 minute ke liye doosre kamre mein rakhiye."),
    ("Day 4", "Gratitude", "Partner ki kisi ek aisi baat ki tareef kijiye jise aap aksar notice nahi karte the."),
    ("Day 5", "Unloading", "Shaam ko ghar aane ke baad 15 minute partner ko suniye bina koi solution diye."),
    ("Day 6", "Touch", "Rung 2: Casual non-demanding touch (kandhe par haath ya baal theek karna)."),
    ("Day 7", "Chai Ritual", "Raat ko bachhon ke sone ke baad balcony par 20 minute chai peete hue purani yaadein taaza kijiye."),
    ("Day 8", "Micro-Kindness", "Partner ke liye unki pasand ka ek chhota snack ya drink bina maange laakar dijiye."),
    ("Day 9", "The 30s Hug", "Rung 3: Din mein bina kisi aage ki demand ke 30 seconds tak ek doosre ko gale lagaiye."),
    ("Day 10", "Mental Load", "Ghar ke 3 aise tasks jo partner coordinate karta tha, unka poora ownership khud lijiye."),
    ("Day 11", "Clean Apology", "Kisi purani chhoti baat par bina 'Lekin' lagaye dil se ek saaf maafi mangiye."),
    ("Day 12", "Memory Lane", "Apni shaadi ya shuruati dino ki 5 puraani photos saath baith kar dekhiye aur muskuraiye."),
    ("Day 13", "Laugh Together", "Koi purana funny show, stand-up comedy ya movie 30 minute saath baith kar dekhiye."),
    ("Day 14", "The Walk", "30 minute ki evening walk jismein koi earphones na hon aur hath pakad kar chaliye."),
    ("Day 15", "Mid-Point Check", "'Pichhle do hafte mein hamare beech kya thoda sa better laga?' par 10 minute baat kijiye."),
    ("Day 16", "Food Memory", "Woh dish order kijiye ya banaiye jo aap courtship ke dino mein khaya karte the."),
    ("Day 17", "Safe Space", "Poochhiye: 'Aisa kaun sa darr hai jo pichhle kuch dino se tumhe pareshan kar raha hai?'"),
    ("Day 18", "WhatsApp Silence", "Poore din parivar ke WhatsApp forwards ya rishtedaron ki gossip par discussion zero rakhiye."),
    ("Day 19", "Public Compliment", "Kisi family member ya bachhe ke samne partner ki sacchi tareef kijiye."),
    ("Day 20", "Quiet Presence", "Ek hi kamre mein 30 minute bina screen ke baith kar book padhiye ya shanti mehsoos kijiye."),
    ("Day 21", "Date Night", "2 ghante ke liye akele bahar coffee ya dinner par jaiye (Rule: No kid logistics talk)."),
    ("Day 22", "Surprise Morning", "Subah partner ke uthne se pehle unke liye bina maange manpasand chai/coffee banaiye."),
    ("Day 23", "Future Dreaming", "Agle saal ki kisi ek chhoti trip ke baare mein baat kijiye jo aap dono akele karna chahte hain."),
    ("Day 24", "Touch Reassurance", "Haath pakad kar TV dekhiye ya sofa par aaram kijiye bina kisi awkwardness ke."),
    ("Day 25", "Clean Reset", "Agar koi baat ho, toh 20-minute pause rule apply karke mudde par baat kijiye."),
    ("Day 26", "Letter of Honor", "Ek chhota handwritten note likhiye jismein 3 baatein hon ki aap unki respect kyun karte hain."),
    ("Day 27", "Shared Silence", "Raat ko terrace par taare dekhte hue 15 minute khamoshi mein haath thamiye."),
    ("Day 28", "Gratitude Flood", "Ek doosre ko 5 specific cheezein bataiye jinke liye aap unke aabhari hain."),
    ("Day 29", "Intimate Reconnect", "Bina kisi jaldbaazi ya pressure ke, dil se judte hue kareeb aaiye."),
    ("Day 30", "The New Covenant", "Dono notebook mein likhiye: 'Hum aage ke saal kaise bitana chahte hain?' aur hug kijiye.")
]

def build_tracker():
    doc = SimpleDocTemplate(
        str(TRACKER_PDF),
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    story = []
    story.append(Paragraph("Hum Ladte Nahi, Par Baat Nahi Karte", title_style))
    story.append(Paragraph("The 30-Day Reconnection Daily Tracker • Companion Worksheet by Sanjay Shharma", sub_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#8C2D19"), spaceAfter=10, spaceBefore=0))
    
    table_rows = [[
        Paragraph("Day", th_style),
        Paragraph("Focus Phase", th_style),
        Paragraph("Daily Micro-Exercise (Rozana Ka Ek Kadam)", th_style),
        Paragraph("Done?", th_style)
    ]]
    for day, phase, desc in days_data:
        table_rows.append([
            Paragraph(day, cell_bold),
            Paragraph(phase, cell_bold),
            Paragraph(desc, cell_style),
            Paragraph("[ &nbsp; ]", cell_bold)
        ])
        
    t = Table(table_rows, colWidths=[50, 95, 350, 45], repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2C3E50")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('ALIGN', (3,0), (3,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
    ]))
    story.append(t)
    doc.build(story)
    print(f"Printable Tracker created at: {TRACKER_PDF}")

if __name__ == "__main__":
    build_tracker()
