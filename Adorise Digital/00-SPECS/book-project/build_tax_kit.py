"""
build_tax_kit.py - Build the Complete ITR, GST & TDS Filing Kit.
Reads book-project/manuscript_tax_kit.md, outputs to book-project/tax_kit/.
"""
import os
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
import ebooklib
from ebooklib import epub

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "manuscript_tax_kit.md"
OUT = ROOT / "tax_kit"
OUT.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(ROOT))
from build_book import parse_markdown, inline_md  # noqa: E402


# ---------- COVER (deep green + gold = money / tax / India) ----------
def build_cover(out_path, title, subtitle, author):
    W, H = 1800, 2700
    top = (10, 40, 30)         # deep forest
    mid = (28, 90, 50)         # money green
    bot = (212, 175, 55)       # gold
    img = Image.new("RGB", (W, H), "#0a1f14")
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
    for x in range(0, W, 80):
        draw.line([(x, 0), (x, H)], fill=(255, 255, 255, 18), width=1)
    for y in range(0, H, 80):
        draw.line([(0, y), (W, y)], fill=(255, 255, 255, 18), width=1)
    # Gold halo
    cx, cy = W // 2, 1500
    for r in range(700, 600, -2):
        alpha = max(0, 50 - (700 - r) // 4)
        draw.ellipse((cx - r, cy - r // 2, cx + r, cy + r // 2), outline=(255, 215, 0, alpha), width=1)

    def load_font(size, bold=False):
        cands = [
            "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf",
        ]
        for p in cands:
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, size)
                except Exception:
                    pass
        return ImageFont.load_default()

    f_eyebrow = load_font(46, bold=True)
    f_title = load_font(140, bold=True)
    f_sub = load_font(52, bold=False)
    f_author = load_font(54, bold=True)
    f_foot = load_font(34, bold=False)

    draw.text((W // 2, 360), "2026 EDITION  /  INDIA TAX KIT", font=f_eyebrow, fill=(255, 255, 255, 230), anchor="mm")

    # Title (long — 3 lines)
    title_lines = _wrap(draw, "COMPLETE ITR, GST & TDS FILING KIT", f_title, W - 200)
    y = 640
    for ln in title_lines[:3]:
        draw.text((W // 2, y), ln, font=f_title, fill=(255, 255, 255, 255), anchor="mm")
        y += 155

    draw.line([(W // 2 - 240, y + 20), (W // 2 + 240, y + 20)], fill=(255, 215, 0, 240), width=5)
    sub_lines = _wrap(draw, subtitle, f_sub, W - 220)
    yy = y + 90
    for ln in sub_lines[:5]:
        draw.text((W // 2, yy), ln, font=f_sub, fill=(245, 245, 220, 240), anchor="mm")
        yy += 62

    draw.text((W // 2, H - 320), author.upper(), font=f_author, fill=(255, 255, 255, 250), anchor="mm")
    draw.text((W // 2, H - 240), "ADORISE DIGITAL  /  SHERIDAN, WY", font=f_foot, fill=(255, 255, 255, 220), anchor="mm")
    draw.text((W // 2, H - 160), "INDIAN TAX COMPLIANCE MASTER BUNDLE", font=load_font(28, bold=True), fill=(255, 215, 0, 230), anchor="mm")

    draw.text((100, 100), "₹", font=load_font(96, bold=True), fill=(255, 215, 0, 220), anchor="mm")
    draw.text((W - 100, 100), "v.1", font=load_font(72, bold=True), fill=(255, 255, 255, 200), anchor="mm")

    img = img.convert("RGB")
    img.save(out_path, "JPEG", quality=92, optimize=True)
    return out_path


def _wrap(draw, text, font, max_w):
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


# ---------- PDF ----------
def build_pdf(blocks, front, out_path, cover_path):
    PAGE_W, PAGE_H = (6 * 72, 9 * 72)
    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=(PAGE_W, PAGE_H),
        leftMargin=0.7 * inch, rightMargin=0.7 * inch,
        topMargin=0.8 * inch, bottomMargin=0.8 * inch,
        title=front.get("title", ""),
        author=front.get("author", "Sanjay Shharma"),
        subject="ITR, GST, TDS, Indian tax compliance, 2026",
        keywords=", ".join(front.get("keywords", []) or []),
    )
    styles = getSampleStyleSheet()
    # Register a TTF font that supports the ₹ glyph (and other Unicode) for body text.
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    body_font = "Helvetica"
    body_font_bold = "Helvetica-Bold"
    body_font_oblique = "Helvetica-Oblique"
    _registered = []
    for ttf_path, reg_name in [
        (r"C:\Windows\Fonts\segoeui.ttf", "BodySans"),
        (r"C:\Windows\Fonts\segoeuib.ttf", "BodySans-Bold"),
        (r"C:\Windows\Fonts\segoeuii.ttf", "BodySans-Italic"),
    ]:
        if os.path.exists(ttf_path):
            try:
                pdfmetrics.registerFont(TTFont(reg_name, ttf_path))
                _registered.append(reg_name)
            except Exception:
                pass
    if _registered:
        body_font = "BodySans" if "BodySans" in _registered else body_font
        body_font_bold = "BodySans-Bold" if "BodySans-Bold" in _registered else body_font_bold
        body_font_oblique = "BodySans-Italic" if "BodySans-Italic" in _registered else body_font_oblique
    h1 = ParagraphStyle("H1", parent=styles["Heading1"], fontName=body_font_bold,
                        fontSize=22, leading=28, spaceBefore=18, spaceAfter=14,
                        textColor=HexColor("#0a2e1a"), alignment=TA_LEFT, keepWithNext=True)
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName=body_font_bold,
                        fontSize=16, leading=20, spaceBefore=14, spaceAfter=8,
                        textColor=HexColor("#1c5a32"), keepWithNext=True)
    h3 = ParagraphStyle("H3", parent=styles["Heading3"], fontName=body_font_bold,
                        fontSize=12.5, leading=16, spaceBefore=10, spaceAfter=6,
                        textColor=HexColor("#2a7042"), keepWithNext=True)
    h4 = ParagraphStyle("H4", parent=styles["Heading4"], fontName=body_font_bold,
                        fontSize=11, leading=14, spaceBefore=8, spaceAfter=4,
                        textColor=HexColor("#2a7042"), keepWithNext=True)
    body = ParagraphStyle("Body", parent=styles["BodyText"], fontName=body_font,
                          fontSize=10.5, leading=15, spaceAfter=8, alignment=TA_JUSTIFY)
    quote = ParagraphStyle("Quote", parent=body, fontName=body_font_oblique,
                           leftIndent=18, rightIndent=18, textColor=HexColor("#2a7042"),
                           spaceBefore=10, spaceAfter=10)
    bullet = ParagraphStyle("Bullet", parent=body, leftIndent=18, bulletIndent=4, spaceAfter=4)
    code = ParagraphStyle("Code", parent=body, fontName=body_font, fontSize=8.5, leading=11, spaceAfter=0, leftIndent=6)
    story = [PageBreak()]

    in_code_block = False
    for kind, content in blocks:
        if kind == "h1":
            story.append(PageBreak())
            story.append(Paragraph(inline_md(content), h1))
        elif kind == "h2":
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
                story.append(Paragraph(inline_md(line) or "&nbsp;", code))
        elif kind == "table":
            header, *rows = content
            cell_style = ParagraphStyle("TblCell", parent=body, fontSize=8.5, leading=11, spaceAfter=0, alignment=TA_LEFT)
            cell_style_b = ParagraphStyle("TblCellB", parent=body, fontSize=8.5, leading=11, spaceAfter=0, alignment=TA_LEFT, fontName=body_font_bold)
            ncols = max(len(header), max((len(r) for r in rows), default=0))
            data = []
            header_row = [Paragraph(inline_md(c), cell_style_b) for c in header + [""] * (ncols - len(header))]
            data.append(header_row)
            for r in rows:
                data.append([Paragraph(inline_md(c), cell_style) for c in r + [""] * (ncols - len(r))])
            avail = PAGE_W - 1.4 * inch
            col_w = avail / ncols
            t = Table(data, colWidths=[col_w] * ncols, repeatRows=1)
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1c5a32")),
                ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
                ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#999999")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#ffffff"), HexColor("#f4f0e8")]),
            ]))
            story.append(t)
            story.append(Spacer(1, 8))

    def on_page(canvas, doc):
        canvas.saveState()
        if doc.page == 1:
            canvas.drawImage(str(cover_path), 0, 0, width=PAGE_W, height=PAGE_H,
                             preserveAspectRatio=True, anchor="c", mask="auto")
        else:
            canvas.setFont("Helvetica", 8)
            canvas.setFillColor(HexColor("#888888"))
            canvas.drawCentredString(PAGE_W / 2, 0.4 * inch, str(doc.page))
        canvas.restoreState()

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    return out_path


# ---------- EPUB ----------
def build_epub(blocks, front, out_path, cover_path):
    book = epub.EpubBook()
    book.set_identifier("urn:uuid:tax-kit-india-2026-001")
    book.set_title(front.get("title", "Complete ITR, GST & TDS Filing Kit — 2026"))
    book.set_language("en")
    book.add_author(front.get("author", "Sanjay Shharma"))
    book.add_metadata("DC", "publisher", front.get("publisher", "Adorise Digital"))
    book.add_metadata("DC", "rights", front.get("rights", ""))
    book.add_metadata("DC", "description",
        "The Complete ITR, GST & TDS Filing Kit — 2026 Edition. The Indian tax compliance master bundle: ITR, GST, TDS, invoicing, checklists, calendar, templates, and step-by-step workflows for salaried, freelance, and business use.")
    for kw in (front.get("keywords") or []):
        book.add_metadata("DC", "subject", kw)
    with open(cover_path, "rb") as f:
        book.set_cover("cover.jpg", f.read())

    css = """
    @namespace epub "http://www.idpf.org/2007/ops";
    body { font-family: Georgia, serif; line-height: 1.55; }
    h1 { font-size: 1.7em; margin: 1.2em 0 0.6em; color: #0a2e1a; page-break-before: always; }
    h2 { font-size: 1.25em; margin: 1em 0 0.4em; color: #1c5a32; }
    h3 { font-size: 1.05em; margin: 0.9em 0 0.3em; color: #2a7042; }
    p { margin: 0 0 0.6em; text-align: justify; }
    blockquote { margin: 0.6em 1.2em; font-style: italic; color: #2a7042; border-left: 3px solid #d4af37; padding-left: 0.8em; }
    ul { margin: 0 0 0.8em 1.2em; }
    hr { border: 0; border-top: 1px solid #cccccc; margin: 1.5em 0; }
    code, pre { font-family: "Courier New", monospace; font-size: 0.85em; background: #f4f0e8; padding: 0 0.2em; }
    pre { padding: 0.6em; white-space: pre-wrap; }
    table { border-collapse: collapse; width: 100%; margin: 0.5em 0 1em; }
    th, td { border: 1px solid #ccc; padding: 4px 6px; text-align: left; font-size: 0.9em; }
    th { background: #1c5a32; color: white; }
    """
    style = epub.EpubItem(uid="style", file_name="style/main.css", media_type="text/css", content=css)
    book.add_item(style)

    title_html = f"""
    <html><head><link rel="stylesheet" href="style/main.css"/></head>
    <body><div style="text-align:center; margin-top:30%;">
      <h1 style="page-break-before:avoid;">{escape(front.get('title',''))}</h1>
      <p style="font-size:1.1em; color:#2a7042;">{escape(front.get('subtitle',''))}</p>
      <p style="margin-top:3em;"><b>{escape(front.get('author',''))}</b></p>
      <p style="color:#666;">{escape(front.get('edition',''))}</p>
    </div></body></html>
    """
    title_chap = epub.EpubHtml(title="Title Page", file_name="title.xhtml", lang="en")
    title_chap.content = title_html
    title_chap.add_item(style)
    book.add_item(title_chap)

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
                li = []
                for it in content:
                    cleaned = re.sub(r"^\d+\.\s*", "", it)
                    li.append("<li>" + inline_md(cleaned) + "</li>")
                out.append("<ul>" + "".join(li) + "</ul>")
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

    chapters = []
    cur_part = None
    cur_title = None
    cur_blocks = []
    pre_blocks = []
    for kind, content in blocks:
        if kind == "h1":
            cur_part = content
            cur_blocks.append((kind, content))
            if cur_title is None:
                pre_blocks = cur_blocks
                cur_blocks = []
                cur_part = content
        elif kind == "h2":
            chap_start = re.match(r"^\d+\.\s", content)
            if chap_start:
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
        chapters = [(None, "Introduction", pre_blocks)] + chapters

    chapter_items = []
    for idx, (part, title, bs) in enumerate(chapters, 1):
        safe = re.sub(r"[^A-Za-z0-9]+", "_", title)[:40] or f"chapter_{idx}"
        fname = f"chap_{idx:02d}_{safe}.xhtml"
        chap = epub.EpubHtml(title=title, file_name=fname, lang="en")
        body = render_blocks(bs)
        heading = f"<h1>{inline_md(title)}</h1>"
        chap.content = f'<html><head><link rel="stylesheet" href="style/main.css"/></head><body>{heading}{body}</body></html>'
        chap.add_item(style)
        book.add_item(chap)
        chapter_items.append(chap)

    book.toc = tuple(chapter_items)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ["cover", "nav", title_chap] + chapter_items
    epub.write_epub(str(out_path), book)
    return out_path


def main():
    md = SRC.read_text(encoding="utf-8")
    front, blocks = parse_markdown(md)
    title = front.get("title", "Complete ITR, GST & TDS Filing Kit — 2026")
    subtitle = front.get("subtitle", "")
    author = front.get("author", "Sanjay Shharma")

    cover = OUT / "cover.jpg"
    pdf = OUT / "Complete-ITR-GST-TDS-Filing-Kit-2026.pdf"
    epub_out = OUT / "Complete-ITR-GST-TDS-Filing-Kit-2026.epub"

    print(f"Building cover -> {cover.name}")
    build_cover(cover, title, subtitle, author)
    print(f"  cover: {cover.stat().st_size:,} bytes")

    print(f"Building PDF   -> {pdf.name}")
    build_pdf(blocks, front, pdf, cover)
    print(f"  pdf:   {pdf.stat().st_size:,} bytes")

    print(f"Building EPUB  -> {epub_out.name}")
    build_epub(blocks, front, epub_out, cover)
    print(f"  epub:  {epub_out.stat().st_size:,} bytes")

    print("\nTax kit complete.")


if __name__ == "__main__":
    main()
