#!/usr/bin/env python3
"""Composite QR code and partner logos onto the neon-themed audition flyer (v2)."""
from PIL import Image, ImageDraw, ImageFont
import os

ASSETS = os.path.dirname(os.path.abspath(__file__))
PRABHUDEVA = os.path.join(ASSETS, 'prabhudeva')

# ── Load base flyer ──────────────────────────────────────────────
flyer = Image.open(os.path.join(ASSETS, 'audition-flyer-v2-base.png')).convert('RGBA')
w, h = flyer.size
print(f'Flyer size: {w}x{h}')

# ── Extend canvas for logo strip ─────────────────────────────────
logo_strip_height = int(h * 0.10)
new_h = h + logo_strip_height
# Deep navy background to match the neon theme
canvas = Image.new('RGBA', (w, new_h), (12, 10, 30, 255))
canvas.paste(flyer, (0, 0))
draw = ImageDraw.Draw(canvas)

# ── Font helper ──────────────────────────────────────────────────
def get_font(size):
    for path in [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNSDisplay.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]:
        try:
            return ImageFont.truetype(path, size)
        except:
            continue
    return ImageFont.load_default()

# ── "NC PARTNERS" label ──────────────────────────────────────────
label_font = get_font(int(w * 0.018))
label = "── NC PARTNERS ──"
# Neon magenta accent to match the theme
label_color = (220, 50, 220, 255)

bbox = draw.textbbox((0, 0), label, font=label_font)
label_w = bbox[2] - bbox[0]
label_x = (w - label_w) // 2
label_y = h + 8
draw.text((label_x, label_y), label, fill=label_color, font=label_font)

# ── Partner logos ────────────────────────────────────────────────
logo_files = [
    'limelemon-logs.jpeg',
    'raleigh-talkies-logo.jpeg',
    'fusion-vibez-logo.jpeg',
    '9bros-logo.jpeg',
    'vk-heritage-logo.jpeg',
]

logos = []
for lf in logo_files:
    path = os.path.join(PRABHUDEVA, lf)
    if os.path.exists(path):
        img = Image.open(path).convert('RGBA')
        logos.append((lf, img))
        print(f'  Loaded: {lf} ({img.size[0]}x{img.size[1]})')

if logos:
    logo_max_h = int(logo_strip_height * 0.52)
    logo_y_start = label_y + int(w * 0.028)

    resized = []
    for name, img in logos:
        ratio = logo_max_h / img.height
        new_w = int(img.width * ratio)
        resized_img = img.resize((new_w, logo_max_h), Image.LANCZOS)
        resized.append(resized_img)

    spacing = int(w * 0.035)
    total_logos_w = sum(r.width for r in resized) + spacing * (len(resized) - 1)
    start_x = (w - total_logos_w) // 2
    x = start_x

    for logo_img in resized:
        canvas.paste(logo_img, (x, logo_y_start), logo_img)
        x += logo_img.width + spacing

    print(f'  Placed {len(resized)} logos')

# ── QR code ──────────────────────────────────────────────────────
qr_path = os.path.join(PRABHUDEVA, 'prabhu-deva-register-qr.png')
if os.path.exists(qr_path):
    qr = Image.open(qr_path).convert('RGBA')
    qr_size = int(min(w, h) * 0.12)
    qr = qr.resize((qr_size, qr_size), Image.LANCZOS)

    padding = 7
    border = 2
    total_size = qr_size + (padding + border) * 2
    qr_box = Image.new('RGBA', (total_size, total_size), (0, 0, 0, 0))
    qr_draw = ImageDraw.Draw(qr_box)

    # Magenta/neon border to match the theme
    neon_border = (220, 50, 220, 255)
    qr_draw.rounded_rectangle([0, 0, total_size - 1, total_size - 1], radius=10, fill=neon_border)
    qr_draw.rounded_rectangle([border, border, total_size - border - 1, total_size - border - 1], radius=8, fill=(255, 255, 255, 255))

    qr_offset = padding + border
    qr_box.paste(qr, (qr_offset, qr_offset))

    # Position: bottom-right, just above the footer line
    margin_right = int(w * 0.03)
    margin_bottom = int(h * 0.04)
    qr_x = w - total_size - margin_right
    qr_y = h - total_size - margin_bottom

    canvas.paste(qr_box, (qr_x, qr_y), qr_box)

    # "SCAN TO REGISTER" label
    scan_font = get_font(int(qr_size * 0.11))
    scan_label = "SCAN TO REGISTER"
    bbox = draw.textbbox((0, 0), scan_label, font=scan_font)
    scan_w = bbox[2] - bbox[0]
    scan_x = qr_x + (total_size - scan_w) // 2
    scan_y = qr_y + total_size + 3

    draw.text((scan_x + 1, scan_y + 1), scan_label, fill=(0, 0, 0, 180), font=scan_font)
    draw.text((scan_x, scan_y), scan_label, fill=neon_border, font=scan_font)

    print(f'  QR code: {qr_size}x{qr_size}px at ({qr_x}, {qr_y})')

# ── Save ─────────────────────────────────────────────────────────
output_path = os.path.join(ASSETS, 'audition-flyer-v2-final.png')
canvas.convert('RGB').save(output_path, quality=95)
print(f'\n✅ Saved: {output_path}')
print(f'   Final size: {w}x{new_h}')
