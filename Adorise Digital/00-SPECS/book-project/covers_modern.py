"""
covers_modern.py - Modern 2026 book cover design for all 4 books.
Uses dark cinematic gradients, bold sans-serif typography, geometric accent shapes.
Replaces the older basic covers in each output directory.
"""
import os
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent

# ----- font loader -----
def load_font(size, bold=False, italic=False):
    cands = []
    if bold:
        cands += [
            r"C:\Windows\Fonts\segoeuib.ttf",  # Segoe UI Semibold
            r"C:\Windows\Fonts\arialbd.ttf",
            r"C:\Windows\Fonts\calibrib.ttf",
        ]
    elif italic:
        cands += [
            r"C:\Windows\Fonts\segoeuii.ttf",
            r"C:\Windows\Fonts\ariali.ttf",
        ]
    else:
        cands += [
            r"C:\Windows\Fonts\segoeui.ttf",
            r"C:\Windows\Fonts\arial.ttf",
            r"C:\Windows\Fonts\calibri.ttf",
        ]
    for p in cands:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


# ----- helpers -----
def wrap_text(draw, text, font, max_w):
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


def text_size(draw, text, font):
    """Get tight (w, h) of rendered text."""
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def vertical_gradient(W, H, top_rgb, mid_rgb, bot_rgb, mid_y_frac=0.5, sharpness=1.0):
    img = Image.new("RGB", (W, H), "#000000")
    px = img.load()
    mid_y = int(H * mid_y_frac)
    for y in range(H):
        if y <= mid_y:
            t = (y / max(mid_y, 1)) ** sharpness
            r = int(top_rgb[0] * (1 - t) + mid_rgb[0] * t)
            g = int(top_rgb[1] * (1 - t) + mid_rgb[1] * t)
            b = int(top_rgb[2] * (1 - t) + mid_rgb[2] * t)
        else:
            t = ((y - mid_y) / max(H - mid_y, 1)) ** sharpness
            r = int(mid_rgb[0] * (1 - t) + bot_rgb[0] * t)
            g = int(mid_rgb[1] * (1 - t) + bot_rgb[1] * t)
            b = int(mid_rgb[2] * (1 - t) + bot_rgb[2] * t)
        for x in range(W):
            px[x, y] = (r, g, b)
    return img


def add_grain(img, amount=8):
    """Add a subtle film-grain texture."""
    import random
    W, H = img.size
    noise = Image.new("L", (W, H))
    pixels = noise.load()
    for y in range(H):
        for x in range(W):
            v = 128 + random.randint(-amount, amount)
            pixels[x, y] = max(0, min(255, v))
    noise = noise.filter(ImageFilter.GaussianBlur(radius=0.6))
    out = Image.new("RGB", (W, H))
    px_in = img.load()
    px_noise = noise.load()
    px_out = out.load()
    for y in range(H):
        for x in range(W):
            n = px_noise[x, y]
            shift = int((n - 128) * 0.08)
            r, g, b = px_in[x, y]
            px_out[x, y] = (
                max(0, min(255, r + shift)),
                max(0, min(255, g + shift)),
                max(0, min(255, b + shift)),
            )
    return out


def draw_accent_shapes(draw, W, H, palette):
    """Geometric accent shapes for modern feel — vertical bar, circle, ring, line."""
    accent = palette["accent"]
    accent2 = palette["accent2"]
    # Vertical accent bar on the left edge
    draw.rectangle([0, 0, 24, H], fill=accent)
    # Top-right circle
    cx, cy, r = W - 220, 220, 110
    for i, w in enumerate(range(20, 0, -1)):
        a = 30 + i * 6
        draw.ellipse((cx - r - w, cy - r - w, cx + r + w, cy + r + w), outline=accent2 + (a,) if len(accent2) == 3 else None, width=1)
    # Diagonal accent line at the bottom
    draw.line([(60, H - 320), (W - 60, H - 320)], fill=accent, width=2)
    # Small dot cluster bottom-left
    for i, (x, y) in enumerate([(90, H - 200), (130, H - 200), (170, H - 200), (90, H - 160), (130, H - 160)]):
        r = 6 if i < 3 else 4
        draw.ellipse((x - r, y - r, x + r, y + r), fill=accent2)


# ----- master cover builder -----
def build_modern_cover(
    out_path,
    title_main,
    title_sub,
    author,
    publisher,
    eyebrow,
    edition_badge,
    palette,
    motif="arc",  # "arc" | "rays" | "grid" | "wave"
    badge_glyph="AI",
):
    W, H = 1800, 2700  # 6x9 @ 300dpi

    # 1) Background gradient
    img = vertical_gradient(W, H, palette["top"], palette["mid"], palette["bot"], mid_y_frac=0.55, sharpness=1.0)

    # 2) Subtle background motif
    draw = ImageDraw.Draw(img, "RGBA")
    accent = palette["accent"]
    accent2 = palette["accent2"]
    if motif == "arc":
        cx, cy = W // 2, H * 0.62
        for r in range(1200, 200, -40):
            a = max(0, 35 - (1200 - r) // 30)
            draw.ellipse((cx - r, cy - int(r * 0.6), cx + r, cy + int(r * 0.6)), outline=(255, 255, 255, a), width=1)
    elif motif == "rays":
        cx, cy = W // 2, H * 0.5
        for ang in range(0, 360, 18):
            rad = math.radians(ang)
            x2 = cx + int(math.cos(rad) * 1600)
            y2 = cy + int(math.sin(rad) * 1600)
            draw.line([(cx, cy), (x2, y2)], fill=(255, 255, 255, 18), width=1)
    elif motif == "grid":
        for x in range(0, W, 90):
            draw.line([(x, 0), (x, H)], fill=(255, 255, 255, 18), width=1)
        for y in range(0, H, 90):
            draw.line([(0, y), (W, y)], fill=(255, 255, 255, 18), width=1)
    elif motif == "wave":
        for y_off in range(0, H, 80):
            pts = []
            for x in range(0, W + 60, 60):
                y = y_off + int(20 * math.sin(x * 0.012 + y_off * 0.02))
                pts.append((x, y))
            for i in range(len(pts) - 1):
                draw.line([pts[i], pts[i + 1]], fill=(255, 255, 255, 22), width=1)

    # 3) Accent shapes (modern editorial look)
    draw_accent_shapes(draw, W, H, palette)

    # 4) Fonts
    f_eyebrow = load_font(56, bold=True)
    f_title = load_font(190, bold=True)
    f_sub = load_font(64, bold=False)
    f_author = load_font(68, bold=True)
    f_publisher = load_font(38, bold=False)
    f_badge = load_font(56, bold=True)
    f_badge_corner = load_font(60, bold=True)
    f_divider_label = load_font(34, bold=False)

    title_color = (255, 255, 255, 255)
    sub_color = (255, 255, 255, 235)
    eyebrow_color = accent2 + (255,) if len(accent2) == 3 else accent + (255,)

    # 5) Eyebrow at top
    draw.text((W // 2, 220), eyebrow, font=f_eyebrow, fill=eyebrow_color, anchor="mm")

    # 6) Title (large, bold, multi-line if needed)
    title_lines = wrap_text(draw, title_main.upper(), f_title, W - 280)
    y = 480
    line_gap = 200
    for ln in title_lines[:3]:
        draw.text((W // 2, y), ln, font=f_title, fill=title_color, anchor="mm")
        y += line_gap

    # 7) Divider with small label
    div_y = y - 20
    draw.line([(W // 2 - 280, div_y), (W // 2 - 60, div_y)], fill=accent2 + (255,) if len(accent2) == 3 else accent + (255,), width=3)
    draw.line([(W // 2 + 60, div_y), (W // 2 + 280, div_y)], fill=accent2 + (255,) if len(accent2) == 3 else accent + (255,), width=3)
    # Small dot between
    draw.ellipse((W // 2 - 14, div_y - 14, W // 2 + 14, div_y + 14), fill=accent2 + (255,) if len(accent2) == 3 else accent + (255,))

    # 8) Subtitle
    sub_lines = wrap_text(draw, title_sub, f_sub, W - 300)
    yy = div_y + 90
    for ln in sub_lines[:4]:
        draw.text((W // 2, yy), ln, font=f_sub, fill=sub_color, anchor="mm")
        yy += 78

    # 9) Author block (bottom)
    author_y = H - 380
    # Accent line above author
    draw.line([(W // 2 - 200, author_y - 90), (W // 2 + 200, author_y - 90)], fill=accent + (255,) if len(accent) == 3 else accent + (255,), width=2)
    draw.text((W // 2, author_y), "AUTHOR", font=f_divider_label, fill=accent2 + (255,) if len(accent2) == 3 else accent + (255,), anchor="mm")
    draw.text((W // 2, author_y + 60), author.upper(), font=f_author, fill=(255, 255, 255, 255), anchor="mm")
    draw.text((W // 2, H - 180), publisher.upper(), font=f_publisher, fill=(220, 220, 220, 230), anchor="mm")
    draw.text((W // 2, H - 110), edition_badge, font=f_divider_label, fill=(200, 200, 200, 220), anchor="mm")

    # 10) Corner badges
    # Top-left: small marker
    draw.ellipse((70, 70, 200, 200), outline=accent + (255,) if len(accent) == 3 else accent + (255,), width=4)
    draw.text((135, 135), badge_glyph, font=f_badge_corner, fill=accent + (255,) if len(accent) == 3 else accent + (255,), anchor="mm")
    # Top-right: edition
    draw.text((W - 110, 130), "2026", font=f_badge_corner, fill=(255, 255, 255, 220), anchor="mm")
    draw.line([(W - 220, 180), (W - 60, 180)], fill=(255, 255, 255, 200), width=2)
    draw.text((W - 110, 220), "EDITION", font=f_divider_label, fill=(200, 200, 200, 200), anchor="mm")

    # 11) Light grain
    img = add_grain(img, amount=6)
    img = img.convert("RGB")
    img.save(out_path, "JPEG", quality=94, optimize=True)
    return out_path


# ----- 4 book configs -----
CONFIGS = {
    "global": {
        "out": ROOT / "outputs_global" / "cover.jpg",
        "title_main": "The Solo AI Income Engine",
        "title_sub": "How One Operator Can Build, Launch, and Scale Profitable AI Side Hustles Without a Team, Funding, or a Burnout Schedule",
        "author": "Sanjay Shharma",
        "publisher": "Adorise Digital  /  Sheridan, Wyoming",
        "eyebrow": "GLOBAL EDITION  /  AI SOLOPRENEUR",
        "edition_badge": "First Global Edition  /  2026",
        "badge_glyph": "AI",
        "motif": "rays",
        "palette": {
            "top": (12, 18, 38),
            "mid": (50, 26, 92),
            "bot": (178, 60, 122),
            "accent": (255, 105, 180),
            "accent2": (255, 215, 130),
        },
    },
    "indian": {
        "out": ROOT / "outputs_indian" / "cover.jpg",
        "title_main": "The Solo AI Income Engine",
        "title_sub": "How Indian Operators Can Build, Launch, and Scale Profitable AI Side Hustles Without a Team, Funding, or a Burnout Schedule",
        "author": "Sanjay Shharma",
        "publisher": "Adorise Digital  /  Sheridan, Wyoming",
        "eyebrow": "INDIAN EDITION  /  AI SOLOPRENEUR",
        "edition_badge": "First Indian Edition  /  2026",
        "badge_glyph": "IN",
        "motif": "arc",
        "palette": {
            "top": (15, 23, 42),
            "mid": (180, 70, 30),
            "bot": (245, 200, 60),
            "accent": (255, 153, 51),
            "accent2": (255, 255, 255),
        },
    },
    "original": {
        "out": ROOT / "outputs" / "cover.jpg",
        "title_main": "The Solo AI Income Engine",
        "title_sub": "How One Operator Can Build, Launch, and Scale Profitable AI Side Hustles Without a Team, Funding, or a Burnout Schedule",
        "author": "Sanjay Shharma",
        "publisher": "Adorise Digital  /  Sheridan, Wyoming",
        "eyebrow": "FIRST EDITION  /  AI SOLOPRENEUR",
        "edition_badge": "First Edition  /  2026",
        "badge_glyph": "AI",
        "motif": "grid",
        "palette": {
            "top": (15, 18, 36),
            "mid": (52, 28, 96),
            "bot": (190, 70, 130),
            "accent": (255, 110, 180),
            "accent2": (255, 215, 130),
        },
    },
    "tax_kit": {
        "out": ROOT / "tax_kit" / "cover.jpg",
        "title_main": "The Complete ITR, GST & TDS Filing Kit",
        "title_sub": "The Indian Tax Compliance Master Bundle  /  ITR, GST, TDS, Invoicing, Checklists, Calendar, and Ready-to-Use Templates",
        "author": "Sanjay Shharma",
        "publisher": "Adorise Digital  /  Sheridan, Wyoming",
        "eyebrow": "2026 EDITION  /  INDIAN TAX KIT",
        "edition_badge": "Indian Tax Compliance Master Bundle",
        "badge_glyph": "₹",
        "motif": "wave",
        "palette": {
            "top": (10, 28, 24),
            "mid": (16, 86, 56),
            "bot": (212, 175, 55),
            "accent": (212, 175, 55),
            "accent2": (240, 220, 120),
        },
    },
}


def main():
    for key, cfg in CONFIGS.items():
        out = cfg["out"]
        out.parent.mkdir(parents=True, exist_ok=True)
        print(f"Building {key} cover -> {out.name}")
        build_modern_cover(
            out,
            cfg["title_main"],
            cfg["title_sub"],
            cfg["author"],
            cfg["publisher"],
            cfg["eyebrow"],
            cfg["edition_badge"],
            cfg["palette"],
            motif=cfg["motif"],
            badge_glyph=cfg["badge_glyph"],
        )
        print(f"  size: {out.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
