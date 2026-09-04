"""
build_book.py - Build PDF, EPUB, and JPG cover for "The Solo AI Income Engine"
Inputs:  book-project/manuscript.md
Outputs: book-project/outputs/cover.jpg
         book-project/outputs/The-Solo-AI-Income-Engine.pdf
         book-project/outputs/The-Solo-AI-Income-Engine.epub
"""
from __future__ import annotations
import os
import re
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, KeepTogether, Image as RLImage,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import ebooklib
from ebooklib import epub

ROOT = Path(__file__).resolve().parent
MANUSCRIPT = ROOT / "manuscript.md"
OUT = ROOT / "outputs"
OUT.mkdir(parents=True, exist_ok=True)

# ---------- 1. PARSE MARKDOWN ----------
def parse_markdown(md: str):
    """Lightweight parser: returns (front_matter_dict, list_of_blocks).
    block = ('h1'|'h2'|'h3'|'p'|'quote'|'hr'|'ul'|'code', text_or_items)
    """
    blocks = []
    front = {}
    in_code = False
    code_buf = []
    in_list = False
    list_buf = []

    def flush_list():
        nonlocal in_list, list_buf
        if in_list:
            blocks.append(("ul", list_buf))
            in_list = False
            list_buf = []

    lines = md.split("\n")
    i = 0
    # Front-matter
    if lines and lines[0].strip() == "---":
        i = 1
        while i < len(lines) and lines[i].strip() != "---":
            m = re.match(r'(\w+):\s*(.*)', lines[i])
            if m and m.group(1) != "keywords":
                front[m.group(1)] = m.group(2).strip().strip('"')
            elif m and m.group(1) == "keywords":
                m2 = re.search(r'\[(.*)\]', lines[i])
                if m2:
                    front["keywords"] = [k.strip().strip('"') for k in m2.group(1).split(",")]
            i += 1
        i += 1  # skip closing ---

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if in_code:
            if stripped.startswith("```"):
                blocks.append(("code", "\n".join(code_buf)))
                code_buf = []
                in_code = False
            else:
                code_buf.append(line)
            i += 1
            continue
        if stripped.startswith("```"):
            flush_list()
            in_code = True
            i += 1
            continue
        if not stripped:
            flush_list()
            i += 1
            continue
        if re.match(r"^# ", stripped):
            flush_list()
            blocks.append(("h1", stripped[2:].strip()))
            i += 1
            continue
        if re.match(r"^## ", stripped):
            flush_list()
            blocks.append(("h2", stripped[3:].strip()))
            i += 1
            continue
        if re.match(r"^### ", stripped):
            flush_list()
            blocks.append(("h3", stripped[4:].strip()))
            i += 1
            continue
        if re.match(r"^#### ", stripped):
            flush_list()
            blocks.append(("h4", stripped[5:].strip()))
            i += 1
            continue
        if stripped == "---":
            flush_list()
            blocks.append(("hr", ""))
            i += 1
            continue
        # GFM-style pipe table: header row, separator row (---|---|---), then rows
        if stripped.startswith("|") and stripped.endswith("|") and "|" in stripped[1:]:
            j = i + 1
            if j < len(lines):
                sep = lines[j].strip()
                # Separator looks like |---|---:|---|
                if re.match(r"^\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)+\|?\s*$", sep):
                    flush_list()
                    header_cells = [c.strip() for c in stripped.strip("|").split("|")]
                    j += 1
                    rows = []
                    while j < len(lines) and lines[j].strip().startswith("|") and lines[j].strip().endswith("|"):
                        rows.append([c.strip() for c in lines[j].strip().strip("|").split("|")])
                        j += 1
                    blocks.append(("table", [header_cells] + rows))
                    i = j
                    continue
        if stripped.startswith("> "):
            flush_list()
            # collect contiguous quote
            q = [stripped[2:].strip()]
            j = i + 1
            while j < len(lines) and lines[j].strip().startswith("> "):
                q.append(lines[j].strip()[2:].strip())
                j += 1
            blocks.append(("quote", "\n".join(q)))
            i = j
            continue
        if re.match(r"^[-*] ", stripped):
            if not in_list:
                in_list = True
                list_buf = []
            list_buf.append(stripped[2:].strip())
            i += 1
            continue
        if re.match(r"^\d+\. ", stripped):
            if not in_list:
                in_list = True
                list_buf = []
            list_buf.append(stripped)
            i += 1
            continue
        # paragraph (collect contiguous non-empty lines)
        flush_list()
        p = [stripped]
        j = i + 1
        while j < len(lines) and lines[j].strip() and not re.match(r"^(#|>|-|\*|```|---\s*$|\d+\. )", lines[j].strip()):
            p.append(lines[j].strip())
            j += 1
        blocks.append(("p", " ".join(p)))
        i = j
    flush_list()
    return front, blocks


# ---------- 2. INLINE MD -> HTML ----------
def inline_md(text: str) -> str:
    text = escape(text, {"\"": "&quot;", "'": "&apos;"})
    # bold
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    # italic
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)\*(?!\*)", r"<i>\1</i>", text)
    # code
    text = re.sub(r"`([^`]+)`", r"<font face='Courier'>\1</font>", text)
    return text


# ---------- 3. COVER (JPG) ----------
def build_cover(out_path: Path, title: str, subtitle: str, author: str):
    W, H = 1800, 2700  # 6x9 at 300dpi
    img = Image.new("RGB", (W, H), "#0b1020")
    # diagonal gradient (deep navy -> electric violet)
    top = (11, 16, 32)
    mid = (40, 22, 78)
    bot = (180, 60, 120)
    px = img.load()
    for y in range(H):
        if y < H // 2:
            t = y / (H / 2)
            r = int(top[0] * (1 - t) + mid[0] * t)
            g = int(top[1] * (1 - t) + mid[1] * t)
            b = int(top[2] * (1 - t) + mid[2] * t)
        else:
            t = (y - H / 2) / (H / 2)
            r = int(mid[0] * (1 - t) + bot[0] * t)
            g = int(mid[1] * (1 - t) + bot[1] * t)
            b = int(mid[2] * (1 - t) + bot[2] * t)
        for x in range(W):
            px[x, y] = (r, g, b)
    draw = ImageDraw.Draw(img, "RGBA")
    # subtle grid
    for x in range(0, W, 80):
        draw.line([(x, 0), (x, H)], fill=(255, 255, 255, 14), width=1)
    for y in range(0, H, 80):
        draw.line([(0, y), (W, y)], fill=(255, 255, 255, 14), width=1)
    # glow ring
    cx, cy = W // 2, 1450
    for r in range(700, 600, -2):
        alpha = max(0, 40 - (700 - r) // 4)
        draw.ellipse((cx - r, cy - r // 2, cx + r, cy + r // 2), outline=(255, 255, 255, alpha), width=1)
    # fonts
    def load_font(size, bold=False):
        candidates = [
            "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf",
        ]
        for p in candidates:
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, size)
                except Exception:
                    pass
        return ImageFont.load_default()

    f_eyebrow = load_font(48, bold=True)
    f_title = load_font(190, bold=True)
    f_sub = load_font(64, bold=False)
    f_author = load_font(58, bold=True)
    f_foot = load_font(36, bold=False)

    eyebrow = "OPERATOR ECONOMY  /  2026 EDITION"
    draw.text((W // 2, 360), eyebrow, font=f_eyebrow, fill=(255, 255, 255, 220), anchor="mm")
    # title (wrap)
    def wrap(text, font, max_w):
        words = text.split()
        lines, cur = [], ""
        for w in words:
            test = (cur + " " + w).strip()
            if draw.textlength(test, font=font) <= max_w:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    title_lines = wrap(title.upper(), f_title, W - 240)
    y = 720
    for ln in title_lines:
        draw.text((W // 2, y), ln, font=f_title, fill=(255, 255, 255, 255), anchor="mm")
        y += 200
    # divider
    draw.line([(W // 2 - 220, y + 30), (W // 2 + 220, y + 30)], fill=(255, 255, 255, 230), width=4)
    # subtitle
    sub_lines = wrap(subtitle, f_sub, W - 280)
    yy = y + 100
    for ln in sub_lines[:4]:
        draw.text((W // 2, yy), ln, font=f_sub, fill=(245, 240, 255, 235), anchor="mm")
        yy += 80
    # author at bottom
    draw.text((W // 2, H - 280), author.upper(), font=f_author, fill=(255, 255, 255, 245), anchor="mm")
    draw.text((W // 2, H - 200), "SOLO OPERATOR PRESS", font=f_foot, fill=(255, 255, 255, 200), anchor="mm")
    # corner marks
    draw.text((100, 100), "A.I.", font=load_font(72, bold=True), fill=(255, 255, 255, 180), anchor="mm")
    draw.text((W - 100, 100), "v.1", font=load_font(72, bold=True), fill=(255, 255, 255, 180), anchor="mm")

    img = img.convert("RGB")
    img.save(out_path, "JPEG", quality=92, optimize=True)
    return out_path


# ---------- 4. PDF ----------
def build_pdf(blocks, front, out_path: Path, cover_path: Path):
    # 6 x 9 inches in points (1 inch = 72 pt)
    PAGE_W, PAGE_H = (6 * 72, 9 * 72)
    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=(PAGE_W, PAGE_H),
        leftMargin=0.7 * inch, rightMargin=0.7 * inch,
        topMargin=0.8 * inch, bottomMargin=0.8 * inch,
        title=front.get("title", ""),
        author=front.get("author", "Sanjay Shharma"),
        subject="AI, solopreneur, side hustle, micro SaaS",
        keywords=", ".join(front.get("keywords", []) or []),
    )
    styles = getSampleStyleSheet()
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    body_font = "Helvetica"
    body_font_bold = "Helvetica-Bold"
    body_font_oblique = "Helvetica-Oblique"
    for ttf_path, reg_name in [
        (r"C:\Windows\Fonts\segoeui.ttf", "BodySans"),
        (r"C:\Windows\Fonts\segoeuib.ttf", "BodySans-Bold"),
        (r"C:\Windows\Fonts\segoeuii.ttf", "BodySans-Italic"),
    ]:
        if os.path.exists(ttf_path):
            try:
                pdfmetrics.registerFont(TTFont(reg_name, ttf_path))
            except Exception:
                pass
    if pdfmetrics.getFont("BodySans"):
        body_font = "BodySans"
    if pdfmetrics.getFont("BodySans-Bold"):
        body_font_bold = "BodySans-Bold"
    if pdfmetrics.getFont("BodySans-Italic"):
        body_font_oblique = "BodySans-Italic"
    h1 = ParagraphStyle("H1", parent=styles["Heading1"], fontName=body_font_bold,
                        fontSize=22, leading=28, spaceBefore=18, spaceAfter=14,
                        textColor=HexColor("#0b1020"), alignment=TA_LEFT,
                        keepWithNext=True)
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName=body_font_bold,
                        fontSize=16, leading=20, spaceBefore=14, spaceAfter=8,
                        textColor=HexColor("#2a1748"), keepWithNext=True)
    h3 = ParagraphStyle("H3", parent=styles["Heading3"], fontName=body_font_bold,
                        fontSize=12.5, leading=16, spaceBefore=10, spaceAfter=6,
                        textColor=HexColor("#3a2058"), keepWithNext=True)
    h4 = ParagraphStyle("H4", parent=styles["Heading4"], fontName=body_font_bold,
                        fontSize=11, leading=14, spaceBefore=8, spaceAfter=4,
                        textColor=HexColor("#3a2058"), keepWithNext=True)
    body = ParagraphStyle("Body", parent=styles["BodyText"], fontName=body_font,
                          fontSize=10.5, leading=15, spaceAfter=8, alignment=TA_JUSTIFY)
    quote = ParagraphStyle("Quote", parent=body, fontName=body_font_oblique,
                          leftIndent=18, rightIndent=18, textColor=HexColor("#3a2058"),
                          borderColor=HexColor("#b46c8a"), borderWidth=0,
                          spaceBefore=10, spaceAfter=10)
    bullet = ParagraphStyle("Bullet", parent=body, leftIndent=18, bulletIndent=4, spaceAfter=4)
    cover_story = [PageBreak()]
    story = cover_story

    for kind, content in blocks:
        if kind == "h1":
            story.append(PageBreak())
            story.append(Paragraph(inline_md(content), h1))
        elif kind == "h2":
            # Only the main chapter h2 (## N. ...) gets a page break.
            # Sub-section h2s (Real Story / Workbook / Key Takeaway) flow inline.
            if re.match(r"^\d+\.\s", content):
                story.append(PageBreak())
            story.append(Paragraph(inline_md(content), h2))
        elif kind == "h3":
            story.append(Paragraph(inline_md(content), h3))
        elif kind == "h4":
            story.append(Paragraph(inline_md(content), h4))
        elif kind == "p":
            story.append(Paragraph(inline_md(content), body))
        elif kind == "quote":
            for line in content.split("\n"):
                story.append(Paragraph(inline_md(line), quote))
        elif kind == "ul":
            for item in content:
                story.append(Paragraph("• " + inline_md(re.sub(r"^\d+\.\s*", "", item)), bullet))
        elif kind == "hr":
            story.append(Spacer(1, 8))
            story.append(Paragraph("<hr/>", body))
            story.append(Spacer(1, 8))
        elif kind == "code":
            for line in content.split("\n"):
                story.append(Paragraph(inline_md(line) or "&nbsp;", ParagraphStyle("Code", parent=body, fontName=body_font, fontSize=8.5, leading=11)))
        elif kind == "table":
            header, *rows = content
            # Wrap cell text in Paragraphs so long content wraps inside the cell
            cell_style = ParagraphStyle("TblCell", parent=body, fontSize=8.5, leading=11, spaceAfter=0, alignment=TA_LEFT)
            cell_style_b = ParagraphStyle("TblCellB", parent=body, fontSize=8.5, leading=11, spaceAfter=0, alignment=TA_LEFT, fontName=body_font_bold)
            ncols = max(len(header), max((len(r) for r in rows), default=0))
            data = []
            header_row = []
            for c in header + [""] * (ncols - len(header)):
                header_row.append(Paragraph(inline_md(c), cell_style_b))
            data.append(header_row)
            for r in rows:
                row = []
                for c in r + [""] * (ncols - len(r)):
                    row.append(Paragraph(inline_md(c), cell_style))
                data.append(row)
            # Compute column widths to fit page
            avail = PAGE_W - 1.4 * inch
            col_w = avail / ncols
            t = Table(data, colWidths=[col_w] * ncols, repeatRows=1)
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), HexColor("#2a1748")),
                ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
                ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#999999")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#ffffff"), HexColor("#f4f0f8")]),
            ]))
            story.append(t)
            story.append(Spacer(1, 8))

    # Page numbers + cover on first page
    def on_page(canvas, doc):
        canvas.saveState()
        if doc.page == 1:
            # Draw cover image as full-bleed background
            canvas.drawImage(str(cover_path), 0, 0, width=PAGE_W, height=PAGE_H,
                             preserveAspectRatio=True, anchor="c", mask="auto")
        else:
            canvas.setFont("Helvetica", 8)
            canvas.setFillColor(HexColor("#888888"))
            canvas.drawCentredString(PAGE_W / 2, 0.4 * inch, str(doc.page))
        canvas.restoreState()

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    return out_path


# ---------- 5. EPUB ----------
def build_epub(blocks, front, out_path: Path, cover_path: Path):
    book = epub.EpubBook()
    book.set_identifier("urn:uuid:solo-ai-income-engine-2026-001")
    book.set_title(front.get("title", "The Solo AI Income Engine"))
    book.set_language("en")
    book.add_author(front.get("author", "Sanjay Shharma"))
    book.add_metadata("DC", "publisher", front.get("publisher", "Solo Operator Press"))
    book.add_metadata("DC", "rights", front.get("rights", ""))
    book.add_metadata("DC", "description",
        "A working manual for building, launching, and scaling profitable AI side hustles as a one-person business in 2026.")
    for kw in (front.get("keywords") or []):
        book.add_metadata("DC", "subject", kw)

    # Cover
    with open(cover_path, "rb") as f:
        book.set_cover("cover.jpg", f.read())

    # CSS
    css = """
    @namespace epub "http://www.idpf.org/2007/ops";
    body { font-family: Georgia, serif; line-height: 1.55; }
    h1 { font-size: 1.7em; margin: 1.2em 0 0.6em; color: #0b1020; page-break-before: always; }
    h2 { font-size: 1.25em; margin: 1em 0 0.4em; color: #2a1748; }
    h3 { font-size: 1.05em; margin: 0.9em 0 0.3em; color: #3a2058; }
    p { margin: 0 0 0.6em; text-align: justify; }
    blockquote { margin: 0.6em 1.2em; font-style: italic; color: #3a2058; border-left: 3px solid #b46c8a; padding-left: 0.8em; }
    ul { margin: 0 0 0.8em 1.2em; }
    hr { border: 0; border-top: 1px solid #cccccc; margin: 1.5em 0; }
    code, pre { font-family: "Courier New", monospace; font-size: 0.9em; background: #f4f0f8; padding: 0 0.2em; }
    pre { padding: 0.6em; white-space: pre-wrap; }
    .toc-title { font-size: 1.6em; font-weight: bold; margin-bottom: 1em; }
    """
    style = epub.EpubItem(uid="style", file_name="style/main.css", media_type="text/css", content=css)
    book.add_item(style)

    # Title page
    title_html = f"""
    <html><head><link rel="stylesheet" href="style/main.css"/></head>
    <body>
    <div style="text-align:center; margin-top:30%;">
      <h1 style="page-break-before:avoid;">{escape(front.get('title',''))}</h1>
      <p style="font-size:1.1em; color:#3a2058;">{escape(front.get('subtitle',''))}</p>
      <p style="margin-top:3em;"><b>{escape(front.get('author',''))}</b></p>
      <p style="color:#666;">{escape(front.get('edition',''))}</p>
    </div>
    </body></html>
    """
    title_chap = epub.EpubHtml(title="Title Page", file_name="title.xhtml", lang="en")
    title_chap.content = title_html
    title_chap.add_item(style)
    book.add_item(title_chap)

    # Group blocks into chapters (split on h1, except first "Table of Contents" / front matter)
    # Build list of structural h1/h2 titles (Part + Chapter) for the TOC
    headings = [(k, c) for (k, c) in blocks if k in ("h1", "h2")]
    print(f"  TOC headings: {len(headings)} (h1={sum(1 for k,_ in headings if k=='h1')}, h2={sum(1 for k,_ in headings if k=='h2')})")

    def render_blocks(bs):
        out = []
        for kind, content in bs:
            if kind == "h1":
                out.append(f"<h1>{inline_md(content)}</h1>")
            elif kind == "h2":
                out.append(f"<h2>{inline_md(content)}</h2>")
            elif kind == "h3":
                out.append(f"<h3>{inline_md(content)}</h3>")
            elif kind == "h4":
                out.append(f"<h4>{inline_md(content)}</h4>")
            elif kind == "p":
                out.append(f"<p>{inline_md(content)}</p>")
            elif kind == "quote":
                out.append(f"<blockquote>{inline_md(content)}</blockquote>")
            elif kind == "ul":
                num_strip = re.compile(r"^\d+\.\s*")
                li_parts = []
                for it in content:
                    cleaned = num_strip.sub("", it)
                    li_parts.append("<li>" + inline_md(cleaned) + "</li>")
                out.append("<ul>" + "".join(li_parts) + "</ul>")
            elif kind == "hr":
                out.append("<hr/>")
            elif kind == "code":
                out.append(f"<pre><code>{escape(content)}</code></pre>")
            elif kind == "table":
                header, *rows = content
                th = "".join(f"<th>{inline_md(c)}</th>" for c in header)
                trs = []
                for r in rows:
                    tds = "".join(f"<td>{inline_md(c)}</td>" for c in r)
                    trs.append(f"<tr>{tds}</tr>")
                out.append(f"<table><thead><tr>{th}</tr></thead><tbody>{''.join(trs)}</tbody></table>")
        return "\n".join(out)

    # Split blocks at each h2 (chapter). Carry forward the most recent h1 (part title)
    # as a section header. Pre-h1 blocks (TOC etc.) become an "Introduction" chapter.
    chapters = []
    cur_part = None
    cur_title = None
    cur_blocks = []
    pre_blocks = []

    for kind, content in blocks:
        if kind == "h1":
            cur_part = content
            # Do not start a new chapter on h1; keep as a heading inside current chapter
            cur_blocks.append((kind, content))
            if cur_title is None:
                # first h1 - everything before becomes intro
                pre_blocks = cur_blocks
                cur_blocks = []
                cur_part = content
        elif kind == "h2":
            # Only the main chapter h2 (## N. ...) gets a page break in EPUB.
            chap_start = re.match(r"^\d+\.\s", content)
            if chap_start:
                # h1 inside blocks carries the part heading
                if cur_title is not None:
                    chapters.append((cur_part, cur_title, cur_blocks))
                cur_title = content
                cur_blocks = []
            else:
                cur_blocks.append((kind, content))
        else:
            cur_blocks.append((kind, content))
    if cur_title is not None:
        chapters.append((cur_part, cur_title, cur_blocks))
    elif cur_blocks:
        pre_blocks.extend(cur_blocks)
    if not chapters and pre_blocks:
        chapters = [(None, "Introduction", pre_blocks)]
    else:
        # prepend intro chapter
        chapters = [(None, "Introduction", pre_blocks)] + chapters

    chapter_items = []
    for idx, (part, title, bs) in enumerate(chapters, 1):
        safe_title = re.sub(r"[^A-Za-z0-9]+", "_", title)[:40] or f"chapter_{idx}"
        fname = f"chap_{idx:02d}_{safe_title}.xhtml"
        chap = epub.EpubHtml(title=title, file_name=fname, lang="en")
        body = render_blocks(bs)
        heading = f"<h1>{inline_md(title)}</h1>"
        chap.content = f'<html><head><link rel="stylesheet" href="style/main.css"/></head><body>{heading}{body}</body></html>'
        chap.add_item(style)
        book.add_item(chap)
        chapter_items.append(chap)

    # Nav / TOC
    book.toc = tuple(chapter_items)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ["cover", "nav", title_chap] + chapter_items

    epub.write_epub(str(out_path), book)
    return out_path


# ---------- MAIN ----------
def main():
    md = MANUSCRIPT.read_text(encoding="utf-8")
    front, blocks = parse_markdown(md)
    title = front.get("title", "The Solo AI Income Engine")
    subtitle = front.get("subtitle", "")
    author = front.get("author", "Sanjay Shharma")
    publisher = front.get("publisher", "Adorise Digital, 30N Gould St, Sheridan, Wyoming, USA")

    cover = OUT / "cover.jpg"
    pdf = OUT / "The-Solo-AI-Income-Engine.pdf"
    epub_out = OUT / "The-Solo-AI-Income-Engine.epub"

    print(f"Building PDF   -> {pdf.name}")
    build_pdf(blocks, front, pdf, cover)
    print(f"  pdf size: {pdf.stat().st_size:,} bytes")

    print(f"Building EPUB  -> {epub_out}")
    build_epub(blocks, front, epub_out, cover)
    print(f"  epub size: {epub_out.stat().st_size:,} bytes")

    print("\nDone.")
    for p in (cover, pdf, epub_out):
        print(f"  {p}  ({p.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
