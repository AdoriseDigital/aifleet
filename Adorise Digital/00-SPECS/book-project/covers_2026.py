"""
covers_2026.py - Modern 2026 Amazon-bestseller cover design.

Design principles applied:
  - Bold minimalism: title is the hero
  - 2-3 color palette, high contrast (thumbnail-readable)
  - One strong focal element per cover
  - Subtitle at ~60% of title weight
  - Author name subordinate
  - Abstract geometric accent (not stock photo)
  - Designed to work at 120px wide
"""
import os
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent

# ---------- font loader (uses Windows TTF with full Unicode coverage) ----------
def load_font(size, bold=False, italic=False, weight=None):
    if weight is None:
        weight = "bold" if bold else "regular"
    cands = []
    if weight == "black":
        cands = [r"C:\Windows\Fonts\seguibl.ttf", r"C:\Windows\Fonts\impact.ttf",
                 r"C:\Windows\Fonts\framd.ttf", r"C:\Windows\Fonts\arialbd.ttf"]
    elif weight == "bold":
        cands = [r"C:\Windows\Fonts\segoeuib.ttf", r"C:\Windows\Fonts\arialbd.ttf",
                 r"C:\Windows\Fonts\calibrib.ttf"]
    elif weight == "italic":
        cands = [r"C:\Windows\Fonts\segoeuii.ttf", r"C:\Windows\Fonts\calibrii.ttf",
                 r"C:\Windows\Fonts\ariali.ttf"]
    else:
        cands = [r"C:\Windows\Fonts\segoeui.ttf", r"C:\Windows\Fonts\arial.ttf",
                 r"C:\Windows\Fonts\calibri.ttf"]
    for p in cands:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


# ---------- text helpers ----------
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
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


# ---------- gradient ----------
def vertical_gradient(W, H, top_rgb, bot_rgb, mid_rgb=None, mid_y=0.55):
    img = Image.new("RGB", (W, H), top_rgb)
    px = img.load()
    if mid_rgb is None:
        for y in range(H):
            t = y / max(H - 1, 1)
            r = int(top_rgb[0] * (1 - t) + bot_rgb[0] * t)
            g = int(top_rgb[1] * (1 - t) + bot_rgb[1] * t)
            b = int(top_rgb[2] * (1 - t) + bot_rgb[2] * t)
            for x in range(W):
                px[x, y] = (r, g, b)
    else:
        my = int(H * mid_y)
        for y in range(H):
            if y <= my:
                t = y / max(my, 1)
                r = int(top_rgb[0] * (1 - t) + mid_rgb[0] * t)
                g = int(top_rgb[1] * (1 - t) + mid_rgb[1] * t)
                b = int(top_rgb[2] * (1 - t) + mid_rgb[2] * t)
            else:
                t = (y - my) / max(H - my, 1)
                r = int(mid_rgb[0] * (1 - t) + bot_rgb[0] * t)
                g = int(mid_rgb[1] * (1 - t) + bot_rgb[1] * t)
                b = int(mid_rgb[2] * (1 - t) + bot_rgb[2] * t)
            for x in range(W):
                px[x, y] = (r, g, b)
    return img


# ---------- abstract geometric focal element ----------
def draw_focal_arc(draw, W, H, color, alpha=80):
    """Big concentric arcs — confident, abstract, modern."""
    cx, cy = W // 2, int(H * 0.55)
    for r in range(int(W * 0.95), 100, -30):
        a = max(0, alpha - (int(W * 0.95) - r) // 8)
        draw.ellipse((cx - r, cy - int(r * 0.7), cx + r, cy + int(r * 0.7)),
                     outline=color + (a,) if len(color) == 3 else color, width=2)


def draw_focal_rings(draw, W, H, color):
    cx, cy = W // 2, int(H * 0.55)
    for r in range(0, int(W * 0.9), 80):
        draw.ellipse((cx - r, cy - int(r * 0.55), cx + r, cy + int(r * 0.55)),
                     outline=color + (40,), width=1)


def draw_focal_rays(draw, W, H, color):
    cx, cy = W // 2, int(H * 0.55)
    for ang in range(0, 360, 15):
        rad = math.radians(ang)
        x2 = cx + int(math.cos(rad) * W)
        y2 = cy + int(math.sin(rad) * H)
        draw.line([(cx, cy), (x2, y2)], fill=color + (18,), width=1)


def draw_focal_grid(draw, W, H, color):
    for x in range(0, W, 70):
        draw.line([(x, 0), (x, H)], fill=color + (22,), width=1)
    for y in range(0, H, 70):
        draw.line([(0, y), (W, y)], fill=color + (22,), width=1)


def draw_focal_wave(draw, W, H, color):
    for y_off in range(0, H, 60):
        pts = []
        for x in range(0, W + 60, 60):
            y = y_off + int(25 * math.sin(x * 0.012 + y_off * 0.018))
            pts.append((x, y))
        for i in range(len(pts) - 1):
            draw.line([pts[i], pts[i + 1]], fill=color + (28,), width=1)


def draw_focal_diamond(draw, W, H, color):
    """Big diamond with nested diamonds + filled center."""
    cx, cy = W // 2, int(H * 0.5)
    s = 700
    draw.polygon([(cx, cy - s), (cx + s, cy), (cx, cy + s), (cx - s, cy)],
                 outline=color + (180,), width=4)
    for r in range(s - 80, 80, -80):
        a = max(20, 200 - (s - r) // 6)
        draw.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)],
                     outline=color + (a,), width=2)
    cs = 100
    draw.polygon([(cx, cy - cs), (cx + cs, cy), (cx, cy + cs), (cx - cs, cy)],
                 fill=color + (255,) if len(color) == 3 else color)


def draw_focal_chakra(draw, W, H, color):
    """Stylized Ashoka-Chakra-inspired wheel behind the title."""
    import math
    cx, cy = W // 2, int(H * 0.5)
    R = 700
    # Outer ring (thicker)
    draw.ellipse((cx - R, cy - R, cx + R, cy + R), outline=color + (255,) if len(color) == 3 else color, width=8)
    # 24 spokes (thick wedges)
    for i in range(24):
        a1 = math.radians(i * 15 - 2.5)
        a2 = math.radians(i * 15 + 2.5)
        x1 = cx + int(math.cos(a1) * (R - 60))
        y1 = cy + int(math.sin(a1) * (R - 60))
        x2 = cx + int(math.cos(a1) * R)
        y2 = cy + int(math.sin(a1) * R)
        x3 = cx + int(math.cos(a2) * R)
        y3 = cy + int(math.sin(a2) * R)
        x4 = cx + int(math.cos(a2) * (R - 60))
        y4 = cy + int(math.sin(a2) * (R - 60))
        draw.polygon([(x1, y1), (x2, y2), (x3, y3), (x4, y4)], fill=color + (200,) if len(color) == 3 else color)
    # Inner ring
    ri = 240
    draw.ellipse((cx - ri, cy - ri, cx + ri, cy + ri), outline=color + (255,) if len(color) == 3 else color, width=6)
    # Hub
    hr = 90
    draw.ellipse((cx - hr, cy - hr, cx + hr, cy + hr), fill=color + (255,) if len(color) == 3 else color)
    # 24 small dots between spokes
    for i in range(24):
        a = math.radians(i * 15 + 7.5)
        x = cx + int(math.cos(a) * (R - 30))
        y = cy + int(math.sin(a) * (R - 30))
        draw.ellipse((x - 6, y - 6, x + 6, y + 6), fill=color + (255,) if len(color) == 3 else color)


def draw_focal_dotgrid(draw, W, H, color):
    """Halftone dot grid — modern, photographic feel."""
    cx, cy = W // 2, int(H * 0.55)
    R = 800
    spacing = 40
    for y in range(0, H, spacing):
        for x in range(0, W, spacing):
            dx, dy = x - cx, y - cy
            d = math.sqrt(dx * dx + dy * dy)
            if d < R:
                r = max(2, int(20 * (1 - d / R)))
                a = max(20, 180 - int(120 * d / R))
                draw.ellipse((x - r, y - r, x + r, y + r), fill=color + (a,))


# ---------- corner / top label ----------
def draw_eyebrow(draw, W, text, font, color):
    """Eyebrow label at the very top, in accent color, all caps, letter-spaced."""
    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad_x, pad_y = 28, 14
    box_w, box_h = w + pad_x * 2, h + pad_y * 2
    x = (W - box_w) // 2
    y = 130
    # rounded rect
    draw.rounded_rectangle([x, y, x + box_w, y + box_h], radius=box_h // 2,
                           outline=color + (255,) if len(color) == 3 else color, width=3)
    draw.text((W // 2, y + box_h // 2), text, font=font,
              fill=color + (255,) if len(color) == 3 else color, anchor="mm")


def draw_corner_mark(draw, W, H, color, text="AI"):
    """Top-left circular badge."""
    cx, cy, r = 150, 150, 90
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=color + (255,) if len(color) == 3 else color, width=4)
    f = load_font(56, weight="black")
    draw.text((cx, cy), text, font=f,
              fill=color + (255,) if len(color) == 3 else color, anchor="mm")


def draw_corner_year(draw, W, color, year="2026", label="EDITION"):
    """Top-right small block."""
    f_year = load_font(50, weight="black")
    f_label = load_font(24, weight="bold")
    x, y = W - 180, 100
    draw.text((x, y), year, font=f_year, fill=(255, 255, 255), anchor="rm")
    draw.line([(x - 140, y + 30), (x, y + 30)], fill=(255, 255, 255, 220), width=2)
    draw.text((x, y + 60), label, font=f_label, fill=(255, 255, 255, 200), anchor="rm")


# ---------- core cover ----------
def build_cover(
    out_path,
    title_main,
    title_sub,
    author,
    publisher,
    eyebrow,
    edition_badge,
    bg_top,
    bg_bot,
    bg_mid,
    text_color,
    accent,
    accent_soft,
    motif,
    badge_text,
):
    W, H = 1800, 2700
    img = vertical_gradient(W, H, bg_top, bg_bot, bg_mid)
    draw = ImageDraw.Draw(img, "RGBA")

    # focal background
    if motif == "arc":
        draw_focal_arc(draw, W, H, accent, alpha=120)
    elif motif == "rings":
        draw_focal_rings(draw, W, H, accent)
    elif motif == "rays":
        draw_focal_rays(draw, W, H, accent)
    elif motif == "grid":
        draw_focal_grid(draw, W, H, accent)
    elif motif == "wave":
        draw_focal_wave(draw, W, H, accent)
    elif motif == "diamond":
        draw_focal_diamond(draw, W, H, accent)
    elif motif == "chakra":
        draw_focal_chakra(draw, W, H, accent)
    elif motif == "dotgrid":
        draw_focal_dotgrid(draw, W, H, accent)

    # corner accents
    draw_corner_mark(draw, W, H, accent, text=badge_text)
    draw_corner_year(draw, W, accent, year="2026", label="EDITION")

    # eyebrow
    f_eyebrow = load_font(46, weight="bold")
    draw_eyebrow(draw, W, eyebrow, f_eyebrow, accent)

    # TITLE — the hero. Big, bold, all caps, with 1-2 line wraps.
    f_title = load_font(180, weight="black")
    title_lines = wrap_text(draw, title_main.upper(), f_title, W - 280)
    # shrink if too many lines
    title_size = 180
    while len(title_lines) > 3 and title_size > 110:
        title_size -= 10
        f_title = load_font(title_size, weight="black")
        title_lines = wrap_text(draw, title_main.upper(), f_title, W - 280)
    y_title = 580
    for ln in title_lines[:3]:
        draw.text((W // 2, y_title), ln, font=f_title, fill=text_color + (255,) if len(text_color) == 3 else text_color, anchor="mm")
        y_title += int(title_size * 1.05)

    # accent line + small dot — replaces generic divider
    line_y = y_title + 20
    draw.line([(W // 2 - 260, line_y), (W // 2 - 30, line_y)], fill=accent + (255,) if len(accent) == 3 else accent, width=4)
    draw.line([(W // 2 + 30, line_y), (W // 2 + 260, line_y)], fill=accent + (255,) if len(accent) == 3 else accent, width=4)
    draw.ellipse((W // 2 - 14, line_y - 14, W // 2 + 14, line_y + 14),
                 fill=accent + (255,) if len(accent) == 3 else accent)

    # SUBTITLE — 60% weight of title, clean, 2-3 lines max
    f_sub = load_font(56)
    sub_lines = wrap_text(draw, title_sub, f_sub, W - 320)
    yy = line_y + 80
    for ln in sub_lines[:3]:
        draw.text((W // 2, yy), ln, font=f_sub, fill=(255, 255, 255, 235), anchor="mm")
        yy += 70

    # AUTHOR block (bottom) — small, clean
    author_y = H - 360
    f_aud = load_font(28, weight="bold")
    draw.text((W // 2, author_y), "AUTHOR", font=f_aud, fill=accent + (220,) if len(accent) == 3 else accent, anchor="mm")
    f_author = load_font(72, weight="bold")
    draw.text((W // 2, author_y + 60), author.upper(),
              font=f_author, fill=(255, 255, 255, 255), anchor="mm")
    # accent thin line
    draw.line([(W // 2 - 140, author_y + 120), (W // 2 + 140, author_y + 120)],
              fill=accent + (255,) if len(accent) == 3 else accent, width=2)
    f_pub = load_font(34)
    draw.text((W // 2, H - 200), publisher.upper(), font=f_pub,
              fill=(220, 220, 220, 220), anchor="mm")
    f_badge = load_font(28, weight="bold")
    draw.text((W // 2, H - 140), edition_badge.upper(), font=f_badge,
              fill=(180, 180, 180, 200), anchor="mm")

    img = img.convert("RGB")
    img.save(out_path, "JPEG", quality=94, optimize=True)
    return out_path


# ---------- 4 book configs (2-3 color palettes, high contrast) ----------
CONFIGS = {
    "global": {
        "out": ROOT / "outputs_global" / "cover.jpg",
        "title_main": "The Solo AI Income Engine",
        "title_sub": "How One Operator Can Build, Launch, and Scale Profitable AI Side Hustles Without a Team or Funding",
        "author": "Sanjay Shharma",
        "publisher": "Adorise Digital",
        "eyebrow": "AI SOLOPRENEUR  /  GLOBAL EDITION",
        "edition_badge": "First Global Edition  /  2026",
        "badge_text": "AI",
        "motif": "arc",
        # Deep navy + electric gold (professional bestseller look)
        "bg_top": (8, 12, 28),
        "bg_mid": (15, 22, 50),
        "bg_bot": (28, 38, 78),
        "text_color": (255, 255, 255),
        "accent": (255, 200, 90),     # gold
        "accent_soft": (255, 230, 180),
    },
    "indian": {
        "out": ROOT / "outputs_indian" / "cover.jpg",
        "title_main": "The Solo AI Income Engine",
        "title_sub": "How Indian Operators Can Build, Launch, and Scale Profitable AI Side Hustles Without a Team or Funding",
        "author": "Sanjay Shharma",
        "publisher": "Adorise Digital",
        "eyebrow": "AI SOLOPRENEUR  /  INDIAN EDITION",
        "edition_badge": "First Indian Edition  /  2026",
        "badge_text": "IN",
        "motif": "chakra",
        # Saffron + deep navy (Indian bestseller)
        "bg_top": (10, 14, 38),
        "bg_mid": (15, 22, 60),
        "bg_bot": (24, 32, 78),
        "text_color": (255, 255, 255),
        "accent": (255, 153, 51),     # saffron
        "accent_soft": (255, 200, 120),
    },
    "original": {
        "out": ROOT / "outputs" / "cover.jpg",
        "title_main": "The Solo AI Income Engine",
        "title_sub": "How One Operator Can Build, Launch, and Scale Profitable AI Side Hustles Without a Team or Funding",
        "author": "Sanjay Shharma",
        "publisher": "Adorise Digital",
        "eyebrow": "AI SOLOPRENEUR  /  FIRST EDITION",
        "edition_badge": "First Edition  /  2026",
        "badge_text": "AI",
        "motif": "rings",
        # Charcoal + electric blue
        "bg_top": (10, 12, 24),
        "bg_mid": (18, 26, 50),
        "bg_bot": (28, 40, 80),
        "text_color": (255, 255, 255),
        "accent": (100, 180, 255),    # electric blue
        "accent_soft": (180, 220, 255),
    },
    "tax_kit": {
        "out": ROOT / "tax_kit" / "cover.jpg",
        "title_main": "The Complete ITR, GST & TDS Filing Kit",
        "title_sub": "Indian Tax Compliance Master Bundle  /  Filing Guides, Checklists, Calendar, and Ready-to-Use Templates",
        "author": "Sanjay Shharma",
        "publisher": "Adorise Digital",
        "eyebrow": "2026 EDITION  /  INDIAN TAX KIT",
        "edition_badge": "First Edition  /  2026",
        "badge_text": "₹",
        "motif": "wave",
        # Forest green + gold (finance/wealth)
        "bg_top": (8, 28, 20),
        "bg_mid": (14, 56, 36),
        "bg_bot": (22, 80, 52),
        "text_color": (255, 255, 255),
        "accent": (212, 175, 55),     # gold
        "accent_soft": (240, 220, 130),
    },
}


def main():
    for key, cfg in CONFIGS.items():
        out = cfg["out"]
        out.parent.mkdir(parents=True, exist_ok=True)
        print(f"Building {key} cover -> {out.name}")
        build_cover(
            out,
            cfg["title_main"],
            cfg["title_sub"],
            cfg["author"],
            cfg["publisher"],
            cfg["eyebrow"],
            cfg["edition_badge"],
            cfg["bg_top"],
            cfg["bg_bot"],
            cfg["bg_mid"],
            cfg["text_color"],
            cfg["accent"],
            cfg["accent_soft"],
            cfg["motif"],
            cfg["badge_text"],
        )
        print(f"  size: {out.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
