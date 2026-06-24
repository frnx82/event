#!/usr/bin/env python3
"""Composite the real QR code and partner logos onto the audition flyer."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

ASSETS = os.path.dirname(os.path.abspath(__file__))
PRABHUDEVA = os.path.join(ASSETS, 'prabhudeva')

# ── Load base flyer ──────────────────────────────────────────────
flyer = Image.open(os.path.join(ASSETS, 'audition-call-flyer.png')).convert('RGBA')
w, h = flyer.size
print(f'Flyer size: {w}x{h}')

# ── Extend canvas for logo strip ─────────────────────────────────
# Add space at the bottom for "NC Partners" + logos
logo_strip_height = int(h * 0.10)  # 10% of height for logo section
new_h = h + logo_strip_height
canvas = Image.new('RGBA', (w, new_h), (15, 15, 15, 255))  # Dark background
canvas.paste(flyer, (0, 0))

draw = ImageDraw.Draw(canvas)

# ── Load font ────────────────────────────────────────────────────
def get_font(size):
    """Get a font, with fallbacks."""
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

# ── Add "NC PARTNERS" label ──────────────────────────────────────
label_font = get_font(int(w * 0.018))
label = "── NC PARTNERS ──"
label_color = (180, 155, 90, 255)  # Muted gold

bbox = draw.textbbox((0, 0), label, font=label_font)
label_w = bbox[2] - bbox[0]
label_x = (w - label_w) // 2
label_y = h + 8

draw.text((label_x, label_y), label, fill=label_color, font=label_font)

# ── Load and composite partner logos ─────────────────────────────
logo_files = [
    'limelemon-logs.jpeg',      # Lime & Lemon
    'raleigh-talkies-logo.jpeg', # Raleigh Talkies
    'fusion-vibez-logo.jpeg',    # Fusion Vibez Studios
    '9bros-logo.jpeg',           # NineBros
    'vk-heritage-logo.jpeg',     # VK Heritage Handicrafts
]

logos = []
for lf in logo_files:
    path = os.path.join(PRABHUDEVA, lf)
    if os.path.exists(path):
        img = Image.open(path).convert('RGBA')
        logos.append((lf, img))
        print(f'  Loaded: {lf} ({img.size[0]}x{img.size[1]})')
    else:
        print(f'  ⚠️  Not found: {lf}')

if logos:
    # Target height for logos
    logo_max_h = int(logo_strip_height * 0.52)
    logo_y_start = label_y + int(w * 0.028)  # Below the label

    # Resize logos to uniform height, preserving aspect ratio
    resized = []
    for name, img in logos:
        ratio = logo_max_h / img.height
        new_w = int(img.width * ratio)
        resized_img = img.resize((new_w, logo_max_h), Image.LANCZOS)
        resized.append(resized_img)

    # Calculate total width with spacing
    spacing = int(w * 0.035)  # Space between logos
    total_logos_w = sum(r.width for r in resized) + spacing * (len(resized) - 1)

    # Center the logo row
    start_x = (w - total_logos_w) // 2
    x = start_x

    for logo_img in resized:
        # Paste logo (use alpha channel for transparency)
        canvas.paste(logo_img, (x, logo_y_start), logo_img)
        x += logo_img.width + spacing

    print(f'  Placed {len(resized)} logos, total width: {total_logos_w}px')

# ── Add QR code ──────────────────────────────────────────────────
qr_path = os.path.join(PRABHUDEVA, 'prabhu-deva-register-qr.png')
if os.path.exists(qr_path):
    qr = Image.open(qr_path).convert('RGBA')
    
    # Size and position
    qr_size = int(min(w, h) * 0.14)
    qr = qr.resize((qr_size, qr_size), Image.LANCZOS)
    
    # White box with gold border
    padding = 7
    border = 2
    total_size = qr_size + (padding + border) * 2
    qr_box = Image.new('RGBA', (total_size, total_size), (0, 0, 0, 0))
    qr_draw = ImageDraw.Draw(qr_box)
    
    gold = (212, 175, 55, 255)
    qr_draw.rounded_rectangle([0, 0, total_size - 1, total_size - 1], radius=10, fill=gold)
    qr_draw.rounded_rectangle([border, border, total_size - border - 1, total_size - border - 1], radius=8, fill=(255, 255, 255, 255))
    
    qr_offset = padding + border
    qr_box.paste(qr, (qr_offset, qr_offset))
    
    # Position: right side, between register section and footer
    margin_right = int(w * 0.03)
    margin_bottom = int(h * 0.10)
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
    draw.text((scan_x, scan_y), scan_label, fill=gold, font=scan_font)
    
    print(f'  QR code: {qr_size}x{qr_size}px at ({qr_x}, {qr_y})')

# ── Save final output ────────────────────────────────────────────
output_path = os.path.join(ASSETS, 'audition-call-flyer-qr.png')
canvas_rgb = canvas.convert('RGB')
canvas_rgb.save(output_path, quality=95)
print(f'\n✅ Saved: {output_path}')
print(f'   Final size: {w}x{new_h}')
