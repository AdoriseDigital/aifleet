"""
covers_ornate.py - Ornate 2026 bestseller cover design matching the reference style.

Visual language (from reference):
  - Deep navy blue background
  - Gold ornamental corner flourishes
  - White uppercase serif title (large, bold)
  - Gold serif subtitle
  - Centered gold line-art icon/illustration
  - White serif author name at bottom
  - Gold border frame around the cover
  - Optional red diagonal ribbon for bonus content
"""
import os
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent
REF_DIR = ROOT / "references"


def load_font(size, bold=False, italic=False, weight=None):
    if weight is None:
        weight = "bold" if bold else "regular"
    cands = []
    if weight == "black":
        cands = [r"C:\Windows\Fonts\seguibl.ttf", r"C:\Windows\Fonts\impact.ttf",
                 r"C:\Windows\Fonts\arialbd.ttf"]
    elif weight == "bold":
        cands = [r"C:\Windows\Fonts\segoeuib.ttf", r"C:\Windows\Fonts\arialbd.ttf",
                 r"C:\Windows\Fonts\calibrib.ttf", r"C:\Windows\Fonts\georgiab.ttf"]
    elif weight == "italic":
        cands = [r"C:\Windows\Fonts\segoeuii.ttf", r"C:\Windows\Fonts\calibrii.ttf",
                 r"C:\Windows\Fonts\ariali.ttf", r"C:\Windows\Fonts\georgiai.ttf"]
    elif weight == "serif_bold":
        cands = [r"C:\Windows\Fonts\georgiab.ttf", r"C:\Windows\Fonts\timesbd.ttf",
                 r"C:\Windows\Fonts\segoeuib.ttf"]
    elif weight == "serif_regular":
        cands = [r"C:\Windows\Fonts\georgia.ttf", r"C:\Windows\Fonts\times.ttf",
                 r"C:\Windows\Fonts\segoeui.ttf"]
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


def text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


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


# ---------- gold gradient background ----------
def vertical_gradient(W, H, top_rgb, bot_rgb, mid_rgb=None):
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
        my = int(H * 0.55)
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


# ---------- ornate gold corner flourishes ----------
def make_flourish_image(color, size=800, scale=1.0):
    """Build a self-contained RGBA flourish image (top-left oriented)."""
    W = int(size * scale)
    H = int(size * scale)
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    c = color + (255,) if len(color) == 3 else color
    s = W / 8.0  # base unit

    def arc(x0, y0, x1, y1, start, end, width):
        d.arc((x0, y0, x1, y1), start, end, fill=c, width=int(width))

    def filled(x, y, r):
        d.ellipse((x - r, y - r, x + r, y + r), fill=c)

    # Big quarter-circle scroll (outer)
    arc(0, 0, int(s * 4), int(s * 4), 180, 270, 10)
    # mid scroll
    arc(int(s * 0.6), int(s * 0.6), int(s * 3.4), int(s * 3.4), 180, 270, 7)
    # inner scroll
    arc(int(s * 1.2), int(s * 1.2), int(s * 2.8), int(s * 2.8), 180, 270, 4)

    # Side tails extending horizontally and vertically
    arc(0, int(s * 3.5), int(s * 2.5), int(s * 5.5), 90, 180, 6)
    arc(int(s * 3.5), 0, int(s * 5.5), int(s * 2.5), 0, 90, 6)

    # Tiny inner swirls
    arc(int(s * 1.8), int(s * 1.8), int(s * 2.4), int(s * 2.4), 0, 360, 3)

    # Leaf teardrops at scroll endpoints
    for cx, cy, r in [(int(s * 4.2), int(s * 0.4), int(s * 0.45)),
                      (int(s * 0.4), int(s * 4.2), int(s * 0.4)),
                      (int(s * 3), int(s * 2), int(s * 0.25)),
                      (int(s * 5.5), int(s * 0.6), int(s * 0.2)),
                      (int(s * 0.6), int(s * 5.5), int(s * 0.2))]:
        filled(cx, cy, r)

    # Small dots
    for cx, cy, r in [(int(s * 4.5), int(s * 0.3), int(s * 0.1)),
                      (int(s * 0.3), int(s * 4.5), int(s * 0.1)),
                      (int(s * 2), int(s * 2), int(s * 0.12)),
                      (int(s * 3.5), int(s * 1.5), int(s * 0.08)),
                      (int(s * 1.5), int(s * 3.5), int(s * 0.08)),
                      (int(s * 5.8), int(s * 0.3), int(s * 0.07)),
                      (int(s * 0.3), int(s * 5.8), int(s * 0.07))]:
        filled(cx, cy, r)

    # Outward L-line (extends toward page corner)
    d.line([(int(s * 5.8), 0), (int(s * 5.8), int(s * 5.8))], fill=c, width=4)
    d.line([(0, int(s * 5.8)), (int(s * 5.8), int(s * 5.8))], fill=c, width=4)

    return img


def paste_flourish_at_corner(base_img, color, corner, scale=1.0):
    """Paste an oriented flourish at one of the 4 corners of base_img.
    corner in {'tl', 'tr', 'br', 'bl'}.
    """
    W, H = base_img.size
    inner = 100
    size = 800
    f = make_flourish_image(color, size=size, scale=scale)
    fw, fh = f.size
    if corner == "tr":
        f = f.transpose(Image.FLIP_LEFT_RIGHT)
    elif corner == "br":
        f = f.transpose(Image.ROTATE_180)
    elif corner == "bl":
        f = f.transpose(Image.FLIP_TOP_BOTTOM)
    if corner == "tl":
        pos = (inner - 40, inner - 40)
    elif corner == "tr":
        pos = (W - inner - fw + 40, inner - 40)
    elif corner == "br":
        pos = (W - inner - fw + 40, H - inner - fh + 40)
    elif corner == "bl":
        pos = (inner - 40, H - inner - fh + 40)
    base_img.paste(f, pos, f)


# ---------- gold border frame ----------
def draw_gold_frame(draw, W, H, color, inset=70, width=4):
    c = color + (255,) if len(color) == 3 else color
    # outer + inner double frame
    draw.rectangle([inset, inset, W - inset, H - inset], outline=c, width=width)
    draw.rectangle([inset + 16, inset + 16, W - inset - 16, H - inset - 16], outline=c, width=2)


# ---------- gold ribbon / badge ----------
def draw_ribbon(draw, W, H, text1, text2, color, text_color=(255, 255, 255)):
    cx, cy = 280, 280
    sz = 600
    c = color + (255,) if len(color) == 3 else color
    tc = text_color + (255,) if len(text_color) == 3 else text_color
    # main banner as polygon (parallelogram-style)
    # diagonal banner from (cx-sz, cy-sz*0.4) -> (cx, cy+sz*0.4) -> (cx+sz*0.6, cy+sz*0.4) -> (cx+sz*0.6-sz, cy-sz*0.4)
    p1 = (cx - sz, cy - sz * 0.35)
    p2 = (cx - sz + 120, cy - sz * 0.55)
    p3 = (cx + 120, cy + sz * 0.05)
    p4 = (cx - 120, cy + sz * 0.25)
    draw.polygon([p1, p2, p3, p4], fill=c)
    # notches at ends
    draw.polygon([(p1[0], p1[1]), (p1[0] + 30, p1[1] - 25), (p1[0] + 30, p1[1] + 25)], fill=(0, 0, 0, 0))
    # text rotated
    f1 = load_font(80, weight="black")
    f2 = load_font(64, weight="black")
    # Centered text
    mid_x = (p1[0] + p3[0]) / 2
    mid_y = (p1[1] + p3[1]) / 2
    # rotation angle ~ 12 degrees
    ang = 12
    # We use a temporary image for rotated text
    txt_img = Image.new("RGBA", (700, 280), (0, 0, 0, 0))
    td = ImageDraw.Draw(txt_img)
    td.text((350, 60), text1, font=f1, fill=tc, anchor="mm")
    td.text((350, 180), text2, font=f2, fill=tc, anchor="mm")
    txt_img = txt_img.rotate(-ang, resample=Image.BICUBIC, center=(350, 140))
    draw._image.paste(txt_img, (int(mid_x - 350), int(mid_y - 140)), txt_img)


def paste_ribbon(img, W, H, text1, text2, color, text_color=(255, 255, 255)):
    cx, cy = 280, 280
    sz = 600
    c = color + (255,) if len(color) == 3 else color
    tc = text_color + (255,) if len(text_color) == 3 else text_color
    p1 = (cx - sz, cy - sz * 0.35)
    p2 = (cx - sz + 120, cy - sz * 0.55)
    p3 = (cx + 120, cy + sz * 0.05)
    p4 = (cx - 120, cy + sz * 0.25)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.polygon([p1, p2, p3, p4], fill=c)
    # notches (darker)
    notch = (max(0, c[0] - 60), max(0, c[1] - 60), max(0, c[2] - 60), 255) if len(c) == 4 else (max(0, c[0]-60), max(0, c[1]-60), max(0, c[2]-60), 255)
    # text rotated
    f1 = load_font(80, weight="black")
    f2 = load_font(64, weight="black")
    txt_img = Image.new("RGBA", (700, 280), (0, 0, 0, 0))
    td = ImageDraw.Draw(txt_img)
    td.text((350, 60), text1, font=f1, fill=tc, anchor="mm")
    td.text((350, 180), text2, font=f2, fill=tc, anchor="mm")
    txt_img = txt_img.rotate(-12, resample=Image.BICUBIC, center=(350, 140))
    overlay.paste(txt_img, (int(cx - 350), int(cy - 140)), txt_img)
    img.paste(overlay, (0, 0), overlay)


# ---------- central icons (gold line-art illustrations) ----------
def draw_icon_credit_report(draw, W, H, color):
    """Gold line-art credit report with checkmarks (like the reference)."""
    cx, cy = W // 2, int(H * 0.62)
    s = 280
    c = color + (255,) if len(color) == 3 else color
    # Outer page rectangle
    draw.rounded_rectangle([cx - s, cy - s, cx + s, cy + s], radius=18, outline=c, width=10)
    # Folded corner
    fold = 60
    draw.polygon([(cx + s, cy - s), (cx + s - fold, cy - s),
                  (cx + s, cy - s + fold)], fill=color + (50,) if len(color) == 3 else color, outline=c, width=4)
    # Title line at top
    draw.line([(cx - s + 40, cy - s + 70), (cx + s - 40, cy - s + 70)], fill=c, width=8)
    draw.text((cx, cy - s + 95), "CREDIT REPORT", font=load_font(38, weight="serif_bold"), fill=c, anchor="mm")
    # Checkboxes left column
    for i, chk_y in enumerate([cy - 40, cy + 50, cy + 140]):
        bx, by = cx - s + 60, chk_y
        draw.rectangle([bx - 28, by - 28, bx + 28, by + 28], outline=c, width=6)
        # Check mark
        draw.line([(bx - 14, by + 2), (bx - 4, by + 14), (bx + 16, by - 12)], fill=c, width=8)
    # Lines right column
    for i, line_y in enumerate([cy - 60, cy - 25, cy + 20, cy + 60, cy + 100, cy + 140, cy + 180]):
        draw.line([(cx - 10, line_y), (cx + s - 60, line_y)], fill=c, width=6)
    # Arrows pointing to errors
    for sx, sy, ex, ey in [(cx - s - 80, cy - 80, cx - s + 10, cy - 30),
                            (cx + s + 80, cy + 50, cx + s - 10, cy + 30),
                            (cx - s - 60, cy + 180, cx - s + 10, cy + 140),
                            (cx + s + 100, cy - 100, cx + s - 10, cy - 60)]:
        # curved arrow
        # simple straight arrow
        draw.line([(sx, sy), (ex, ey)], fill=c, width=6)
        # arrow head
        ang = math.atan2(ey - sy, ex - sx)
        ah = 22
        ax1 = ex - ah * math.cos(ang - math.radians(25))
        ay1 = ey - ah * math.sin(ang - math.radians(25))
        ax2 = ex - ah * math.cos(ang + math.radians(25))
        ay2 = ey - ah * math.sin(ang + math.radians(25))
        draw.polygon([(ex, ey), (ax1, ay1), (ax2, ay2)], fill=c)


def draw_icon_money(draw, W, H, color):
    """Gold dollar/coin stack icon (large, centered)."""
    cx, cy = W // 2, int(H * 0.62)
    c = color + (255,) if len(color) == 3 else color
    # 4 stacked coins
    for i, dy in enumerate([140, 70, 0, -70]):
        s = 360 - i * 25
        draw.ellipse((cx - s, cy + dy - 40, cx + s, cy + dy + 40),
                     outline=c, width=10, fill=color + (30 + i*10,) if len(color)==3 else color)
        # inner ring
        draw.ellipse((cx - s + 20, cy + dy - 20, cx + s - 20, cy + dy + 20),
                     outline=c, width=3)
        # $ sign on top coin
        if i == 0:
            f = load_font(300, weight="black")
            draw.text((cx, cy + dy), "$", font=f, fill=c, anchor="mm")
    # Upward arrow on right
    f = load_font(380, weight="black")
    draw.text((cx + 540, cy - 120), "↑", font=f, fill=c, anchor="mm")
    # small star top-left
    for cx2, cy2, r in [(cx - 460, cy - 160, 20), (cx - 540, cy + 60, 14)]:
        draw.ellipse((cx2 - r, cy2 - r, cx2 + r, cy2 + r), fill=c)


def draw_icon_chakra(draw, W, H, color):
    """Gold chakra wheel icon (large, centered) - for tax kit."""
    cx, cy = W // 2, int(H * 0.62)
    R = 340
    c = color + (255,) if len(color) == 3 else color
    draw.ellipse((cx - R, cy - R, cx + R, cy + R), outline=c, width=14)
    for i in range(24):
        a1 = math.radians(i * 15 - 2.5)
        a2 = math.radians(i * 15 + 2.5)
        x1 = cx + int(math.cos(a1) * (R - 90))
        y1 = cy + int(math.sin(a1) * (R - 90))
        x2 = cx + int(math.cos(a1) * R)
        y2 = cy + int(math.sin(a1) * R)
        x3 = cx + int(math.cos(a2) * R)
        y3 = cy + int(math.sin(a2) * R)
        x4 = cx + int(math.cos(a2) * (R - 90))
        y4 = cy + int(math.sin(a2) * (R - 90))
        draw.polygon([(x1, y1), (x2, y2), (x3, y3), (x4, y4)], fill=c)
    ri = 130
    draw.ellipse((cx - ri, cy - ri, cx + ri, cy + ri), outline=c, width=10)
    hr = 50
    draw.ellipse((cx - hr, cy - hr, cx + hr, cy + hr), fill=c)
    for i in range(24):
        a = math.radians(i * 15 + 7.5)
        x = cx + int(math.cos(a) * (R - 50))
        y = cy + int(math.sin(a) * (R - 50))
        draw.ellipse((x - 8, y - 8, x + 8, y + 8), fill=c)


def draw_icon_rocket(draw, W, H, color):
    """Gold rocket / growth icon (large, centered)."""
    cx, cy = W // 2, int(H * 0.62)
    c = color + (255,) if len(color) == 3 else color
    s = 400
    # outer glow ring
    draw.ellipse((cx - s - 60, cy - s - 60, cx + s + 60, cy + s + 60),
                 outline=color + (60,) if len(color) == 3 else color, width=3)
    # rocket body (teardrop pointing up)
    draw.polygon([(cx, cy - s), (cx + 130, cy + 30), (cx, cy + s),
                  (cx - 130, cy + 30)], outline=c, width=10,
                 fill=color + (40,) if len(color) == 3 else color)
    # window
    draw.ellipse((cx - 60, cy - 50, cx + 60, cy + 50), outline=c, width=8, fill=color + (30,))
    # body details
    draw.line([(cx - 60, cy + 100), (cx + 60, cy + 100)], fill=c, width=6)
    draw.line([(cx - 50, cy + 180), (cx + 50, cy + 180)], fill=c, width=6)
    # fins
    draw.polygon([(cx - 130, cy + 100), (cx - 240, cy + s - 30), (cx - 130, cy + s - 100)],
                 outline=c, width=8, fill=color + (30,))
    draw.polygon([(cx + 130, cy + 100), (cx + 240, cy + s - 30), (cx + 130, cy + s - 100)],
                 outline=c, width=8, fill=color + (30,))
    # flame
    draw.polygon([(cx - 60, cy + s - 30), (cx, cy + s + 120), (cx + 60, cy + s - 30)],
                 outline=c, width=8, fill=color + (60,))
    draw.polygon([(cx - 30, cy + s + 20), (cx, cy + s + 90), (cx + 30, cy + s + 20)],
                 outline=color + (90,) if len(color) == 3 else color)
    # trajectory dots / stars
    for i, (dx, dy, r) in enumerate([(-360, -180, 14), (-440, -60, 10), (-480, 80, 12),
                                       (360, -180, 14), (440, -60, 10), (480, 80, 12),
                                       (-300, 280, 8), (300, 280, 8)]):
        draw.ellipse((cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r), fill=c)


def draw_icon_shield(draw, W, H, color):
    """Gold shield (compliance/protection) icon."""
    cx, cy = W // 2, int(H * 0.62)
    c = color + (255,) if len(color) == 3 else color
    # shield
    s = 220
    draw.polygon([(cx, cy - s), (cx + s, cy - s + 30), (cx + s, cy + 60),
                  (cx, cy + s + 40), (cx - s, cy + 60), (cx - s, cy - s + 30)],
                 outline=c, width=10, fill=color + (30,) if len(color) == 3 else color)
    # checkmark
    draw.line([(cx - 80, cy + 20), (cx - 20, cy + 80), (cx + 100, cy - 60)], fill=c, width=20)


def draw_icon_chakra(draw, W, H, color):
    """Gold chakra wheel icon (for tax kit)."""
    cx, cy = W // 2, int(H * 0.62)
    R = 230
    c = color + (255,) if len(color) == 3 else color
    draw.ellipse((cx - R, cy - R, cx + R, cy + R), outline=c, width=10)
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
        draw.polygon([(x1, y1), (x2, y2), (x3, y3), (x4, y4)], fill=c)
    ri = 80
    draw.ellipse((cx - ri, cy - ri, cx + ri, cy + ri), outline=c, width=6)
    hr = 30
    draw.ellipse((cx - hr, cy - hr, cx + hr, cy + hr), fill=c)


# ---------- core builder ----------
def build_ornate_cover(
    out_path,
    title_main,
    title_sub,
    author,
    bg_top,
    bg_bot,
    bg_mid,
    icon_func,
    ribbon_text=None,
):
    W, H = 1800, 2700
    img = vertical_gradient(W, H, bg_top, bg_bot, bg_mid)
    draw = ImageDraw.Draw(img, "RGBA")
    gold = (212, 175, 55)
    white = (255, 255, 255)

    # Gold border frame
    draw_gold_frame(draw, W, H, gold, inset=80, width=4)
    draw_gold_frame(draw, W, H, gold, inset=98, width=2)

    # Corner flourishes (paste pre-rendered images at each corner)
    paste_flourish_at_corner(img, gold, "tl", scale=1.0)
    paste_flourish_at_corner(img, gold, "tr", scale=1.0)
    paste_flourish_at_corner(img, gold, "br", scale=1.0)
    paste_flourish_at_corner(img, gold, "bl", scale=1.0)

    # Title (white serif, uppercase)
    f_title = load_font(170, weight="serif_bold")
    title_lines = wrap_text(draw, title_main.upper(), f_title, W - 360)
    title_size = 170
    while len(title_lines) > 3 and title_size > 120:
        title_size -= 10
        f_title = load_font(title_size, weight="serif_bold")
        title_lines = wrap_text(draw, title_main.upper(), f_title, W - 360)
    y = 600
    for ln in title_lines[:3]:
        draw.text((W // 2, y), ln, font=f_title, fill=white, anchor="mm")
        y += int(title_size * 1.05)

    # Small gold divider with dots (decorative)
    line_y = y + 30
    draw.line([(W // 2 - 200, line_y), (W // 2 - 30, line_y)], fill=gold, width=3)
    draw.line([(W // 2 + 30, line_y), (W // 2 + 200, line_y)], fill=gold, width=3)
    draw.ellipse((W // 2 - 12, line_y - 12, W // 2 + 12, line_y + 12), fill=gold)

    # Subtitle (gold serif)
    f_sub = load_font(58, weight="serif_regular")
    sub_lines = wrap_text(draw, title_sub, f_sub, W - 400)
    yy = line_y + 80
    for ln in sub_lines[:3]:
        draw.text((W // 2, yy), ln, font=f_sub, fill=gold, anchor="mm")
        yy += 70

    # Central icon
    icon_func(draw, W, H, gold)

    # Author at bottom (white serif)
    f_author = load_font(80, weight="serif_bold")
    f_publisher = load_font(36, weight="serif_regular")
    f_year = load_font(32, weight="bold")
    author_y = H - 380
    # gold accent line above author
    draw.line([(W // 2 - 250, author_y - 80), (W // 2 + 250, author_y - 80)], fill=gold, width=2)
    draw.text((W // 2, author_y), author.upper(), font=f_author, fill=white, anchor="mm")
    draw.line([(W // 2 - 200, author_y + 70), (W // 2 + 200, author_y + 70)], fill=gold, width=1)
    draw.text((W // 2, H - 200), "ADORISE DIGITAL PUBLISHING", font=f_publisher, fill=gold, anchor="mm")
    draw.text((W // 2, H - 150), "FIRST EDITION  /  2026", font=f_year, fill=(220, 200, 140), anchor="mm")

    # Optional ribbon
    if ribbon_text:
        paste_ribbon(img, W, H, ribbon_text[0], ribbon_text[1], (200, 35, 50), (255, 255, 255))

    img = img.convert("RGB")
    img.save(out_path, "JPEG", quality=95, optimize=True)
    return out_path


# ---------- configs ----------
CONFIGS = {
    "global": {
        "out": ROOT / "outputs_global" / "cover.jpg",
        "title_main": "The Solo AI Income Engine",
        "title_sub": "How One Operator Can Build, Launch, and Scale Profitable AI Side Hustles",
        "author": "Sanjay Shharma",
        "bg_top": (10, 18, 50),
        "bg_mid": (12, 22, 62),
        "bg_bot": (15, 28, 80),
        "icon": "rocket",
        "ribbon": ("PLUS", "GLOBAL EDITION"),
    },
    "indian": {
        "out": ROOT / "outputs_indian" / "cover.jpg",
        "title_main": "The Solo AI Income Engine",
        "title_sub": "How Indian Operators Can Build, Launch, and Scale Profitable AI Side Hustles",
        "author": "Sanjay Shharma",
        "bg_top": (10, 18, 50),
        "bg_mid": (12, 22, 62),
        "bg_bot": (15, 28, 80),
        "icon": "money",
        "ribbon": ("INDIAN", "EDITION"),
    },
    "original": {
        "out": ROOT / "outputs" / "cover.jpg",
        "title_main": "The Solo AI Income Engine",
        "title_sub": "How One Operator Can Build, Launch, and Scale Profitable AI Side Hustles",
        "author": "Sanjay Shharma",
        "bg_top": (10, 18, 50),
        "bg_mid": (12, 22, 62),
        "bg_bot": (15, 28, 80),
        "icon": "rocket",
        "ribbon": None,
    },
    "tax_kit": {
        "out": ROOT / "tax_kit" / "cover.jpg",
        "title_main": "The Complete ITR, GST & TDS Filing Kit",
        "title_sub": "Indian Tax Compliance Master Bundle with Filing Guides, Checklists, and Ready-to-Use Templates",
        "author": "Sanjay Shharma",
        "bg_top": (10, 32, 22),
        "bg_mid": (14, 50, 34),
        "bg_bot": (18, 72, 48),
        "icon": "chakra",
        "ribbon": ("PLUS 40+", "TEMPLATES"),
    },
}

ICONS = {
    "rocket": draw_icon_rocket,
    "money": draw_icon_money,
    "shield": draw_icon_shield,
    "credit": draw_icon_credit_report,
    "chakra": draw_icon_chakra,
}


def main():
    for key, cfg in CONFIGS.items():
        out = cfg["out"]
        out.parent.mkdir(parents=True, exist_ok=True)
        print(f"Building {key} cover -> {out.name}")
        build_ornate_cover(
            out,
            cfg["title_main"],
            cfg["title_sub"],
            cfg["author"],
            cfg["bg_top"],
            cfg["bg_bot"],
            cfg["bg_mid"],
            ICONS[cfg["icon"]],
            ribbon_text=cfg["ribbon"],
        )
        print(f"  size: {out.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
