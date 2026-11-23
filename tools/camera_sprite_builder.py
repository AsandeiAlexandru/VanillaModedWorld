"""
High-Fidelity Camera Joker Sprite Builder
Generates pixel-perfect Polaroid Now+ camera for Balatro.
Dimensions: 71x95 (1x) and 142x190 (2x).
Branded with 'joker' on the camera chin.
"""
import os
import math
from PIL import Image, ImageDraw

def create_camera_1x():
    W, H = 71, 95
    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Palette
    C_OUTLINE = (18, 18, 22, 255)
    
    # 1. Cast shadow on ground (soft Balatro style)
    for dy in range(6):
        alpha = int(100 - dy * 16)
        x_in = 8 + dy * 2
        draw.ellipse([x_in, 80 + dy, W - x_in, 84 + dy * 2], fill=(8, 8, 12, alpha))

    # 2. Camera Silhouette Map
    body = set()
    for y in range(12, 83):
        for x in range(7, 64):
            # Viewfinder hump:
            if y < 22:
                # Slope:
                if 33 <= x <= 44:
                    slope_y = 22 - (x - 33) * (9.0 / 11.0)
                    if y >= slope_y:
                        body.add((x, y))
                elif 44 < x <= 58:
                    if y >= 13:
                        # Round top corners of hump:
                        if y == 13 and (x <= 45 or x >= 57):
                            continue
                        body.add((x, y))
                elif 58 < x <= 61:
                    # Right slope of hump down to shoulder:
                    slope_right = 13 + (x - 58) * 4.0
                    if y >= slope_right:
                        body.add((x, y))
            elif y <= 81:
                # Main body
                # Top left corner rounding:
                if y <= 25 and x <= 12:
                    if (12 - x)**2 + (25 - y)**2 > 14:
                        continue
                # Bottom left corner rounding:
                if y >= 78 and x <= 12:
                    if (12 - x)**2 + (y - 78)**2 > 14:
                        continue
                # Bottom right corner rounding:
                if y >= 78 and x >= 58:
                    if (x - 58)**2 + (y - 78)**2 > 14:
                        continue
                # Top right corner rounding (below hump):
                if y <= 26 and x >= 60:
                    if (x - 60)**2 + (26 - y)**2 > 6:
                        continue
                
                # Side edges:
                if 8 <= x <= 62:
                    body.add((x, y))

    # Outlines
    outline = set()
    for (x, y) in body:
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if (nx, ny) not in body:
                outline.add((nx, ny))

    for (ox, oy) in outline:
        if 0 <= ox < W and 0 <= oy < H:
            img.putpixel((ox, oy), C_OUTLINE)

    # Fill body with rich matte shading
    for (x, y) in body:
        v_factor = (y - 13) / 70.0
        h_factor = (x - 8) / 54.0

        base_tone = 40 - v_factor * 16 - h_factor * 6
        
        # Upper face vs Lower shelf division at y = 52
        if y <= 52:
            curve_hl = max(0, 1.0 - abs(x - 22) / 16.0) * 8
            tone = base_tone + curve_hl + 4
        else:
            # Lower chin shelf
            if y == 53:
                tone = base_tone + 26
            elif y == 54:
                tone = base_tone + 12
            else:
                curve_hl = max(0, 1.0 - abs(x - 35) / 20.0) * 6
                tone = base_tone + curve_hl - 2

        # Highlights on top & left perimeter:
        if (x, y - 1) in outline:
            tone += 28
        elif (x, y - 2) in outline:
            tone += 12
        if (x - 1, y) in outline:
            tone += 16

        # Shadows on right & bottom perimeter:
        if (x + 1, y) in outline or (x, y + 1) in outline:
            tone -= 14

        r = max(18, min(95, int(tone)))
        g = max(18, min(95, int(tone * 1.01)))
        b = max(22, min(108, int(tone * 1.08)))
        img.putpixel((x, y), (r, g, b, 255))

    # 3. Viewfinder Housing Details (Top Hump)
    draw.rounded_rectangle([48, 24, 56, 32], radius=2, outline=(18, 18, 22, 255), fill=(14, 18, 26, 255))
    draw.rectangle([50, 26, 54, 30], fill=(22, 30, 42, 255))
    draw.line([50, 30, 54, 26], fill=(55, 95, 140, 255))
    draw.point([53, 26], fill=(130, 185, 235, 255))
    draw.point([54, 25], fill=(210, 240, 255, 255))

    # 4. Flash Unit (Top Left: x=12..22, y=24..33)
    draw.rounded_rectangle([12, 23, 23, 33], radius=2, outline=(18, 18, 22, 255), fill=(26, 26, 30, 255))
    draw.rounded_rectangle([13, 24, 22, 32], radius=1, fill=(180, 190, 200, 255))
    for fy in range(25, 32, 2):
        draw.line([14, fy, 21, fy], fill=(135, 145, 155, 255))
    draw.line([14, 27, 21, 27], fill=(245, 250, 255, 255))
    draw.line([14, 28, 21, 28], fill=(230, 240, 250, 255))
    draw.point([14, 27], fill=(255, 255, 255, 255))
    draw.point([15, 27], fill=(255, 255, 255, 255))

    # 5. Red Shutter Button (Middle Left: x=14..22, y=38..46)
    bx, by, br = 18, 42, 4
    draw.ellipse([bx - br - 1, by - br - 1, bx + br + 1, by + br + 1], fill=(14, 14, 18, 255))
    draw.ellipse([bx - br, by - br, bx + br, by + br], fill=(225, 40, 40, 255))
    draw.arc([bx - br, by - br, bx + br, by + br], start=180, end=330, fill=(255, 110, 110, 255), width=1)
    draw.point([bx - 1, by - 1], fill=(255, 175, 175, 255))
    draw.point([bx - 2, by - 1], fill=(255, 130, 130, 255))
    draw.arc([bx - br, by - br, bx + br, by + br], start=10, end=140, fill=(145, 20, 20, 255), width=1)

    # 6. Feature "+" Button (Middle Right: x=50..55, y=41..46)
    draw.rounded_rectangle([50, 41, 55, 46], radius=1, fill=(22, 22, 26, 255), outline=(14, 14, 18, 255))
    c_plus = (0, 210, 255, 255)
    draw.point([52, 42], fill=c_plus)
    draw.point([53, 42], fill=c_plus)
    draw.point([51, 43], fill=c_plus)
    draw.point([52, 43], fill=(200, 255, 255, 255))
    draw.point([53, 43], fill=(200, 255, 255, 255))
    draw.point([54, 43], fill=c_plus)
    draw.point([52, 44], fill=c_plus)
    draw.point([53, 44], fill=c_plus)

    # 7. Big Center Lens Assembly
    lx, ly = 35, 39
    draw.ellipse([lx - 14, ly - 14, lx + 14, ly + 14], fill=(16, 16, 20, 255), outline=C_OUTLINE)
    draw.arc([lx - 14, ly - 14, lx + 14, ly + 14], start=190, end=350, fill=(80, 80, 92, 255), width=1)
    
    draw.ellipse([lx - 12, ly - 12, lx + 12, ly + 12], fill=(28, 28, 32, 255))
    for deg in range(0, 360, 20):
        rad = math.radians(deg)
        kx = int(lx + 11.5 * math.cos(rad) + 0.5)
        ky = int(ly + 11.5 * math.sin(rad) + 0.5)
        draw.point([kx, ky], fill=(46, 46, 54, 255))

    draw.ellipse([lx - 10, ly - 10, lx + 10, ly + 10], fill=(18, 18, 22, 255), outline=(12, 12, 14, 255))
    for deg in [210, 230, 250, 270, 290, 310, 330]:
        rad = math.radians(deg)
        tx = int(lx + 9.2 * math.cos(rad) + 0.5)
        ty = int(ly + 9.2 * math.sin(rad) + 0.5)
        draw.point([tx, ty], fill=(140, 145, 155, 255))

    draw.ellipse([lx - 8, ly - 8, lx + 8, ly + 8], fill=(24, 26, 30, 255), outline=(14, 14, 16, 255))
    draw.ellipse([lx - 7, ly - 7, lx + 7, ly + 7], fill=(8, 12, 20, 255))
    draw.ellipse([lx - 5, ly - 5, lx + 5, ly + 5], fill=(4, 6, 12, 255))

    draw.arc([lx - 6, ly - 6, lx + 6, ly + 6], start=280, end=90, fill=(35, 145, 225, 255), width=2)
    draw.arc([lx - 5, ly - 5, lx + 5, ly + 5], start=300, end=70, fill=(75, 195, 255, 255), width=1)
    draw.point([lx + 4, ly - 2], fill=(160, 235, 255, 255))
    draw.point([lx + 4, ly - 1], fill=(220, 250, 255, 255))

    draw.point([lx - 3, ly - 3], fill=(255, 255, 255, 255))
    draw.point([lx - 4, ly - 3], fill=(200, 225, 255, 240))
    draw.point([lx - 3, ly - 4], fill=(200, 225, 255, 240))
    draw.point([lx - 2, ly - 2], fill=(120, 160, 210, 180))

    draw.arc([lx - 6, ly - 6, lx + 6, ly + 6], start=110, end=170, fill=(110, 45, 140, 200), width=1)

    draw.ellipse([lx - 1, ly + 11, lx + 1, ly + 13], fill=(10, 10, 12, 255))
    draw.point([lx, ly + 12], fill=(28, 38, 52, 255))

    # 8. Iconic Polaroid Rainbow Stripe
    stripes = [
        (33, (238, 49, 36, 255)),   # Red
        (34, (247, 148, 29, 255)),  # Orange
        (35, (255, 221, 0, 255)),   # Yellow
        (36, (0, 166, 81, 255)),    # Green
        (37, (0, 114, 188, 255)),   # Blue
    ]
    for (sx, color) in stripes:
        draw.line([sx, 53, sx, 75], fill=color)
        r, g, b, a = color
        draw.point([sx, 53], fill=(min(255, r + 50), min(255, g + 50), min(255, b + 50), 255))
        draw.point([sx, 75], fill=(int(r * 0.75), int(g * 0.75), int(b * 0.75), 255))

    # 9. Custom 'joker' Branding Typography
    # Lower left: 'joker' in sleek avant-garde lowercase pixel font
    c_brand = (175, 180, 192, 255) # bright silver
    joker_dots = [
        # j (x=14..15, y=64..68)
        (15, 64), # dot of j
        (15, 66), (15, 67), (15, 68), (14, 68),
        # o (x=17..19, y=66..68)
        (17, 66), (17, 67), (18, 66), (18, 68), (19, 66), (19, 67),
        # k (x=21..23, y=64..68)
        (21, 64), (21, 65), (21, 66), (21, 67), (21, 68), (23, 66), (22, 67), (23, 68),
        # e (x=25..27, y=66..68)
        (25, 66), (25, 67), (25, 68), (26, 66), (26, 67), (26, 68), (27, 66), (27, 68),
        # r (x=29..31, y=66..68)
        (29, 66), (29, 67), (29, 68), (30, 66), (31, 66)
    ]
    for (px, py) in joker_dots:
        draw.point([px, py], fill=c_brand)

    # 10. Film Ejection Slot & Lip (Bottom Chin: x=14..57, y=76..78)
    draw.line([14, 76, 57, 76], fill=(12, 12, 14, 255))
    draw.line([14, 77, 57, 77], fill=(6, 6, 8, 255))
    draw.line([15, 78, 56, 78], fill=(60, 60, 68, 255))

    return img

def create_camera_2x(img_1x):
    return img_1x.resize((142, 190), Image.NEAREST)

if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets_1x = os.path.join(BASE_DIR, 'assets', '1x')
    assets_2x = os.path.join(BASE_DIR, 'assets', '2x')
    os.makedirs(assets_1x, exist_ok=True)
    os.makedirs(assets_2x, exist_ok=True)
    
    img_1x = create_camera_1x()
    img_2x = create_camera_2x(img_1x)
    
    img_1x.save(os.path.join(assets_1x, 'j_camera.png'))
    img_2x.save(os.path.join(assets_2x, 'j_camera.png'))
    print('Updated camera assets with joker branding written to assets/1x and assets/2x!')
