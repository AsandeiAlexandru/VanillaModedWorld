"""
Sprite builder for VanillaModedWorld (Balatro Mod)
Adheres strictly to balatro_mod_art_direction_prompt_system.md and vanilla Balatro assets.
"""

import os
import math
import time
import numpy as np
from PIL import Image, ImageDraw

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_1X = os.path.join(BASE_DIR, "assets", "1x")
ASSETS_2X = os.path.join(BASE_DIR, "assets", "2x")

os.makedirs(ASSETS_1X, exist_ok=True)
os.makedirs(ASSETS_2X, exist_ok=True)

# Official Balatro Palette
PALETTE = {
    # Core
    "MULT_RED": (254, 95, 85, 255),       # #FE5F55
    "MULT_SHADOW": (193, 56, 48, 255),    # #C13830
    "CHIPS_BLUE": (0, 156, 253, 255),     # #009CFD
    "CHIPS_SHADOW": (0, 107, 179, 255),   # #006BB3
    "GOLD_YELLOW": (243, 185, 88, 255),   # #F3B958
    "GOLD_HL": (255, 224, 130, 255),      # #FFE082
    "GOLD_SHADOW": (197, 139, 43, 255),   # #C58B2B
    "DARK_SLATE": (55, 66, 68, 255),      # #374244
    "DEEP_OUTLINE": (30, 37, 40, 255),    # #1E2528
    "MID_SLATE": (79, 99, 103, 255),      # #4F6367
    "CARD_WHITE": (255, 255, 255, 255),   # #FFFFFF
    "CARD_CREAM": (242, 244, 243, 255),   # #F2F4F3
    "PAPER_SHADOW": (216, 226, 220, 255), # #D8E2DC
    
    # Vanilla Blueprint Palette
    "BP_BLUE": (75, 105, 207, 255),       # #4B69CF
    "BP_GRID": (125, 147, 226, 255),      # #7D93E2
    "BP_DARK": (62, 96, 212, 255),        # #3E60D4
    "BP_WHITE": (255, 255, 255, 255),
    
    # Vanilla Tarot Parchment Palette
    "TAROT_CREAM": (255, 229, 180, 255),  # #FFE5B4
    "TAROT_TAN": (218, 183, 114, 255),    # #DAB772
    "TAROT_BROWN": (165, 133, 71, 255),   # #A58547
    "TAROT_SLATE": (79, 99, 103, 255),    # #4F6367
    
    # Categories & Accents
    "TAROT_PURPLE": (158, 123, 181, 255), # #9E7BB5
    "PLANET_CYAN": (19, 175, 206, 255),   # #13AFCE
    "GREEN": (75, 194, 146, 255),         # #4BC292
    "HOLO_MAGENTA": (219, 90, 180, 255),
    "FOIL_CYAN": (80, 215, 255, 255),
    
    # Legendary / Dark Palette
    "VOID_BLACK": (18, 18, 22, 255),
    "VOID_PURPLE": (40, 28, 54, 255),
    "STANCZYK_RED": (205, 42, 42, 255),
    "STANCZYK_DARK": (130, 24, 28, 255),
}

def export_sprite(img: Image.Image, filename: str):
    """Exports sprite to 1x and nearest-neighbor upscaled 2x."""
    path_1x = os.path.join(ASSETS_1X, filename)
    path_2x = os.path.join(ASSETS_2X, filename)
    
    for attempt in range(5):
        try:
            img.save(path_1x, format="PNG")
            break
        except OSError:
            time.sleep(0.1)

    img_2x = img.resize((img.width * 2, img.height * 2), Image.Resampling.NEAREST)
    for attempt in range(5):
        try:
            img_2x.save(path_2x, format="PNG")
            break
        except OSError:
            time.sleep(0.1)

    print(f"[OK] Exported {filename} -> 1x ({img.width}x{img.height}) and 2x ({img_2x.width}x{img_2x.height})")

def create_card_base(bg_color=PALETTE["CARD_CREAM"], border_color=PALETTE["DEEP_OUTLINE"]):
    """Creates a standard 71x95 Balatro card blank with rounded transparent corners."""
    img = Image.new("RGBA", (71, 95), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([1, 1, 69, 93], fill=bg_color)
    draw.line([(3, 0), (67, 0)], fill=border_color)
    draw.line([(3, 94), (67, 94)], fill=border_color)
    draw.line([(0, 3), (0, 91)], fill=border_color)
    draw.line([(70, 3), (70, 91)], fill=border_color)
    
    corner_pixels = [
        ((1, 2), border_color), ((2, 1), border_color),
        ((69, 2), border_color), ((68, 1), border_color),
        ((1, 92), border_color), ((2, 93), border_color),
        ((69, 92), border_color), ((68, 93), border_color),
    ]
    for pt, col in corner_pixels:
        draw.point(pt, fill=col)
        
    return img

def bezier_points(p0, p1, p2, p3, steps=15):
    """Generates smooth sampled points along a cubic Bezier curve."""
    pts = []
    for i in range(steps + 1):
        t = i / float(steps)
        u = 1 - t
        x = u**3 * p0[0] + 3 * u**2 * t * p1[0] + 3 * u * t**2 * p2[0] + t**3 * p3[0]
        y = u**3 * p0[1] + 3 * u**2 * t * p1[1] + 3 * u * t**2 * p2[1] + t**3 * p3[1]
        pts.append((int(round(x)), int(round(y))))
    return pts

TAROT_FONT = {
    'W': [
        '##.##.#',
        '##.##.#',
        '##.##.#',
        '#######',
        '###.##.',
        '##..##.'
    ],
    'E': [
        '####',
        '##..',
        '##..',
        '###.',
        '##..',
        '####'
    ],
    'A': [
        '.##.',
        '###.',
        '##.#',
        '####',
        '##.#',
        '##.#'
    ],
    'K': [
        '##.#',
        '##.#',
        '###.',
        '##.#',
        '##.#',
        '##.#'
    ],
    'N': [
        '##..##',
        '###.##',
        '#.####',
        '#..###',
        '#...##',
        '#...##'
    ],
    'S': [
        '.###',
        '##..',
        '.##.',
        '..##',
        '.###',
        '###.'
    ],
    'M': [
        '##..##.',
        '###.##.',
        '#######',
        '##.##.#',
        '##.##.#',
        '##.##.#'
    ],
    'I': [
        '####',
        '.##.',
        '.##.',
        '.##.',
        '.##.',
        '####'
    ],
    'R': [
        '###.',
        '##.#',
        '##.#',
        '###.',
        '##.#',
        '##.#'
    ],
    'O': [
        '.###.',
        '##.##',
        '##.##',
        '##.##',
        '##.##',
        '.###.'
    ],
    'P': [
        '###.',
        '##.#',
        '##.#',
        '###.',
        '##..',
        '##..'
    ]
}

def is_interior_canvas(x, y):
    """Returns True if (x, y) is inside the authentic Balatro Tarot interior illustration canvas.
    Stops strictly inside the inner woodcut frame borders (x=9..61, y=6..88),
    and strictly excludes the top Roman numeral plaque and bottom title banner.
    """
    if not (9 <= x <= 61):
        return False
    if y < 6 or y > 88:
        return False

    # Top Roman numeral plaque exclusion:
    # Plaque borders: y=6,7 -> x in [23, 48]; y=8 -> x in [24, 47]; y=9 -> x in [25, 46]
    if y in (6, 7) and 23 <= x <= 48:
        return False
    if y == 8 and 24 <= x <= 47:
        return False
    if y == 9 and 25 <= x <= 46:
        return False

    # Bottom title banner exclusion:
    # Banner borders: y=82 -> x in [14, 56]; y=83 -> x in [13, 57]; y=84..88 -> x in [12, 58]
    if y == 82 and 14 <= x <= 56:
        return False
    if y == 83 and 13 <= x <= 57:
        return False
    if 84 <= y <= 88 and 12 <= x <= 58:
        return False

    return True

def trace_tarot_ray(cx, cy, angle_rad, r_start, r_max):
    """Traces a ray strictly within the tarot interior illustration canvas.
    Stops immediately upon reaching the inner frame, top Roman numeral plaque, or bottom title banner.
    """
    points = []
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    for r in range(r_start, r_max + 1):
        x = int(round(cx + cos_a * r))
        y = int(round(cy + sin_a * r))
        if not is_interior_canvas(x, y):
            break
        points.append((x, y))
    return points

def create_tarot_base(numeral_str="XVI", title_str="MIRROR"):
    """
    Creates an authentic vanilla Balatro Tarot card base directly from the official card frame.
    Features:
    - 100% authentic woodcut borders, corner brackets, and notched parchment contours
    - Official Roman numeral plaque (XI from Strength for Weakness, XVI from Tower for Mirror)
    - Pristine Balatro bottom title banner with exact row 82 border and centered woodcut typography
    - Strictly compliant with the official 5-color Balatro Tarot palette:
      #4F6367 (Slate), #A58547 (Amber), #DAB772 (Gold), #FFE5B4 (Cream), #FFFFFF (White)
    """
    C_SLATE = (79, 99, 103, 255)
    C_CREAM = (255, 229, 180, 255)

    # Determine template
    if numeral_str == "XI":
        template_path = os.path.join(BASE_DIR, "tools", "vanilla", "tarot_strength.png")
    else:
        template_path = os.path.join(BASE_DIR, "tools", "vanilla", "tarot_tower.png")

    if os.path.exists(template_path):
        base = Image.open(template_path).convert("RGBA")
    else:
        sheet_path = os.path.join(BASE_DIR, "PC _ Computer - Balatro - Jokers and Consumables - Tarot, Planet and Spectral Cards.png")
        sheet = Image.open(sheet_path).convert("RGBA")
        col = 1 if numeral_str == "XI" else 6
        base = sheet.crop((col * 71, 95, (col + 1) * 71, 190))

    # 1. Clear ALL interior canvas pixels (including upper and lower flanks) to C_CREAM
    # so no leftover vanilla template art or dark patches remain
    for y in range(95):
        for x in range(71):
            if is_interior_canvas(x, y):
                base.putpixel((x, y), C_CREAM)

    # Restore inner frame line at (8, 27) (Tower template had a lightning strike break at this pixel)
    base.putpixel((8, 27), C_SLATE)

    # 2. Clear banner interior strictly within inner banner body (x=14..56 y=83, x=13..57 y=84..88, x=15..55 y=89)
    for x in range(14, 57):
        base.putpixel((x, 83), C_CREAM)
    for y in range(84, 89):
        for x in range(13, 58):
            base.putpixel((x, y), C_CREAM)
    for x in range(15, 56):
        base.putpixel((x, 89), C_CREAM)

    # 3. Draw Title Text
    display_title = "MIRROR" if title_str in ("MIRROR", "THE MIRROR") else title_str
    widths = [len(TAROT_FONT[ch][0]) for ch in display_title]
    total_w = sum(widths) + (len(display_title) - 1)
    cur_x = int(round(35.0 - total_w / 2.0))
    for i, ch in enumerate(display_title):
        if ch in TAROT_FONT:
            grid = TAROT_FONT[ch]
            for row_idx, row in enumerate(grid):
                for col_idx, char in enumerate(row):
                    if char == '#':
                        base.putpixel((cur_x + col_idx, 84 + row_idx), C_SLATE)
            cur_x += widths[i] + 1

    return base

def build_mod_icon():
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([2, 2, 29, 29], fill=PALETTE["GREEN"])
    draw.line([(3, 1), (28, 1)], fill=PALETTE["DEEP_OUTLINE"])
    draw.line([(3, 30), (28, 30)], fill=PALETTE["DEEP_OUTLINE"])
    draw.line([(1, 3), (1, 28)], fill=PALETTE["DEEP_OUTLINE"])
    draw.line([(30, 3), (30, 28)], fill=PALETTE["DEEP_OUTLINE"])
    
    v_pixels = [
        (8, 9), (9, 9), (22, 9), (23, 9),
        (9, 10), (10, 10), (21, 10), (22, 10),
        (10, 11), (11, 11), (20, 11), (21, 11),
        (11, 12), (12, 12), (19, 12), (20, 12),
        (12, 13), (13, 13), (18, 13), (19, 13),
        (13, 14), (14, 14), (17, 14), (18, 14),
        (14, 15), (15, 15), (16, 15), (17, 15),
        (15, 16), (16, 16),
        (15, 17), (16, 17),
    ]
    for x, y in v_pixels:
        draw.point((x+1, y+1), fill=PALETTE["DEEP_OUTLINE"])
    for x, y in v_pixels:
        draw.point((x, y), fill=PALETTE["CARD_WHITE"])
    export_sprite(img, "icon.png")

def draw_vertical_joker_text(img: Image.Image, color, top_left=True, bottom_right=True):
    """
    Draws authentic vanilla vertical 'J-O-K-E-R' text (from j_joker):
    - Top-left (y=7..50, x=3..12): reading top-to-bottom
    - Bottom-right (y=44..87, x=58..67): 180-degree inverted index reading down-to-up
    """
    mask_path = os.path.join(BASE_DIR, "tools", "vertical_joker_mask.png")
    if not os.path.exists(mask_path):
        return
    mask = Image.open(mask_path)
    
    if top_left:
        color_layer = Image.new("RGBA", mask.size, color)
        img.paste(color_layer, (3, 7), mask)
        
    if bottom_right:
        mask_rot = mask.rotate(180)
        color_layer = Image.new("RGBA", mask.size, color)
        img.paste(color_layer, (58, 44), mask_rot)

def build_j_espresso():
    """Builds improved Espresso Joker (71x95 px, 142x190 2x) - Italian demitasse with rich crema & rising steam."""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    C_OUTLINE = PALETTE["DEEP_OUTLINE"]
    C_CREAM = PALETTE["CARD_CREAM"]
    C_WHITE = PALETTE["CARD_WHITE"]
    C_SHADOW = PALETTE["PAPER_SHADOW"]
    C_BROWN_DARK = (45, 26, 14, 255)
    C_BROWN = (82, 48, 26, 255)
    C_BROWN_LIGHT = (135, 82, 46, 255)
    C_CREMA = (205, 145, 85, 255)
    C_CREMA_HL = (235, 185, 120, 255)
    C_GOLD = PALETTE["GOLD_YELLOW"]
    C_GOLD_HL = PALETTE["GOLD_HL"]
    C_RED = PALETTE["MULT_RED"]

    # 1. Soft shadow on the card table
    draw.ellipse([14, 69, 56, 79], fill=(215, 222, 220, 255))

    # 2. Porcelain Saucer
    draw.ellipse([15, 63, 55, 75], fill=C_WHITE, outline=C_OUTLINE)
    draw.ellipse([17, 65, 53, 73], fill=C_CREAM)
    draw.ellipse([21, 67, 49, 72], fill=C_SHADOW)
    draw.arc([16, 64, 54, 74], start=0, end=180, fill=C_GOLD)

    # 3. Demitasse Cup Body
    # Handle
    draw.arc([43, 47, 54, 62], start=270, end=90, fill=C_OUTLINE, width=3)
    draw.arc([44, 48, 53, 61], start=270, end=90, fill=C_WHITE, width=2)
    draw.point((51, 54), fill=C_SHADOW)

    # Cup ceramic body (Warm Terracotta-Ruby Red)
    draw.polygon([(22, 44), (20, 52), (23, 66), (47, 66), (50, 52), (48, 44)], fill=C_RED, outline=C_OUTLINE)
    draw.line([(22, 46), (23, 64)], fill=(255, 160, 150, 255))
    draw.line([(47, 46), (46, 64)], fill=PALETTE["MULT_SHADOW"])

    # Coffee bean emblem on cup front
    draw.ellipse([32, 53, 38, 60], fill=C_BROWN_DARK)
    draw.line([(34, 54), (36, 59)], fill=C_CREMA_HL)

    # 4. Cup Rim & Steaming Espresso Surface
    draw.ellipse([21, 40, 49, 48], fill=C_WHITE, outline=C_OUTLINE)
    draw.ellipse([23, 42, 47, 46], fill=C_BROWN_DARK)
    draw.ellipse([25, 43, 45, 45], fill=C_CREMA)
    draw.point((30, 44), fill=C_CREMA_HL)
    draw.point((38, 44), fill=C_CREMA_HL)
    draw.point((34, 43), fill=C_GOLD_HL)

    # 5. Rising Elegant Steam Wisps
    steam_pixels = [
        (28, 37), (27, 34), (28, 31), (29, 28), (28, 25), (26, 22), (27, 19),
        (35, 36), (36, 33), (35, 30), (34, 26), (35, 23), (36, 19), (35, 16),
        (42, 38), (43, 35), (42, 32), (41, 29), (42, 26), (43, 23), (42, 20)
    ]
    for sx, sy in steam_pixels:
        draw.point((sx, sy), fill=(225, 235, 230, 220))
        draw.point((sx + 1, sy), fill=C_WHITE)

    # 6. Roasted Coffee Beans on Saucer
    draw.ellipse([12, 73, 17, 78], fill=C_BROWN, outline=C_OUTLINE)
    draw.line([(14, 74), (15, 77)], fill=C_BROWN_DARK)
    draw.point((13, 75), fill=C_BROWN_LIGHT)
    draw.ellipse([53, 72, 58, 77], fill=C_BROWN, outline=C_OUTLINE)
    draw.line([(55, 73), (56, 76)], fill=C_BROWN_DARK)
    draw.point((54, 74), fill=C_BROWN_LIGHT)

    # 7. Authentic vertical JOKER text in top-left and bottom-right
    draw_vertical_joker_text(img, PALETTE["DARK_SLATE"], top_left=True, bottom_right=True)

    export_sprite(img, "j_espresso.png")

def build_j_double_espresso():
    """Builds Double Espresso Joker (71x95 px, 142x190 2x) - Twin demitasse espresso cups with double steam & beans."""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    C_OUTLINE = PALETTE["DEEP_OUTLINE"]
    C_CREAM = PALETTE["CARD_CREAM"]
    C_WHITE = PALETTE["CARD_WHITE"]
    C_SHADOW = PALETTE["PAPER_SHADOW"]
    C_BROWN_DARK = (45, 26, 14, 255)
    C_BROWN = (82, 48, 26, 255)
    C_BROWN_LIGHT = (135, 82, 46, 255)
    C_CREMA = (205, 145, 85, 255)
    C_CREMA_HL = (235, 185, 120, 255)
    C_GOLD = PALETTE["GOLD_YELLOW"]
    C_GOLD_HL = PALETTE["GOLD_HL"]
    C_RED = PALETTE["MULT_RED"]
    C_RED_DARK = PALETTE["MULT_SHADOW"]

    # Table shadow under the double tray
    draw.ellipse([11, 70, 59, 81], fill=(215, 222, 220, 255))

    # Elongated double porcelain saucer
    draw.ellipse([12, 64, 58, 76], fill=C_WHITE, outline=C_OUTLINE)
    draw.ellipse([14, 66, 56, 74], fill=C_CREAM)
    draw.arc([13, 65, 57, 75], start=0, end=180, fill=C_GOLD)

    def draw_cup(cx, cy, body_col, shadow_col, handle_left=False):
        hx = cx - 14 if handle_left else cx + 9
        draw.arc([hx, cy + 5, hx + 10, cy + 18], start=90 if handle_left else 270, end=270 if handle_left else 90, fill=C_OUTLINE, width=3)
        draw.arc([hx, cy + 6, hx + 9, cy + 17], start=90 if handle_left else 270, end=270 if handle_left else 90, fill=C_WHITE, width=2)
        
        draw.polygon([(cx - 11, cy + 2), (cx - 13, cy + 9), (cx - 10, cy + 22), (cx + 10, cy + 22), (cx + 13, cy + 9), (cx + 11, cy + 2)], fill=body_col, outline=C_OUTLINE)
        draw.line([(cx - 11, cy + 4), (cx - 10, cy + 20)], fill=(255, 160, 150, 255) if body_col == C_RED else C_GOLD_HL)
        draw.line([(cx + 10, cy + 4), (cx + 9, cy + 20)], fill=shadow_col)
        
        draw.ellipse([cx - 12, cy - 2, cx + 12, cy + 6], fill=C_WHITE, outline=C_OUTLINE)
        draw.ellipse([cx - 10, cy, cx + 10, cy + 4], fill=C_BROWN_DARK)
        draw.ellipse([cx - 8, cy + 1, cx + 8, cy + 3], fill=C_CREMA)
        draw.point((cx - 3, cy + 2), fill=C_CREMA_HL)
        draw.point((cx + 3, cy + 2), fill=C_CREMA_HL)

    # Back/Right cup (Deep Roasted Mahogany with Gold Trim)
    draw_cup(43, 46, (60, 36, 20, 255), C_BROWN_DARK, handle_left=False)
    # Front/Left cup (Terracotta Red)
    draw_cup(27, 49, C_RED, C_RED_DARK, handle_left=True)

    # Double Bean Emblem on Front Cup
    draw.ellipse([24, 58, 27, 63], fill=C_BROWN_DARK)
    draw.ellipse([27, 58, 30, 63], fill=C_BROWN_DARK)
    draw.point((25, 60), fill=C_CREMA_HL)
    draw.point((28, 60), fill=C_CREMA_HL)

    # Rising Double Steam plumes intertwining
    steam_pixels = [
        (25, 43), (24, 40), (25, 36), (27, 32), (28, 28), (27, 24), (25, 20), (26, 16),
        (43, 40), (44, 37), (43, 33), (41, 29), (40, 25), (41, 21), (43, 17), (42, 13),
        (33, 35), (35, 31), (34, 27), (36, 23), (35, 19), (34, 15)
    ]
    for sx, sy in steam_pixels:
        draw.point((sx, sy), fill=(225, 235, 230, 220))
        draw.point((sx + 1, sy), fill=C_WHITE)

    # Energetic golden espresso sparkles
    sparkles = [(16, 36), (53, 34), (35, 10), (49, 18), (21, 24)]
    for sx, sy in sparkles:
        draw.line([(sx - 1, sy), (sx + 1, sy)], fill=C_GOLD_HL)
        draw.line([(sx, sy - 1), (sx, sy + 1)], fill=C_GOLD_HL)
        draw.point((sx, sy), fill=C_WHITE)

    # Beans on the saucer
    draw.ellipse([11, 74, 16, 79], fill=C_BROWN, outline=C_OUTLINE)
    draw.ellipse([54, 73, 59, 78], fill=C_BROWN, outline=C_OUTLINE)

    # Vertical JOKER Lettering
    draw_vertical_joker_text(img, PALETTE["DARK_SLATE"], top_left=True, bottom_right=True)

    export_sprite(img, "j_double_espresso.png")

def build_c_the_mirror():
    """Builds The Mirror Tarot Card (71x95, 2x 142x190)
    Effect: Select 2 cards, copy enhancement from left card to right card.
    100% authentic Balatro Tarot woodcut style adhering strictly to the official 5-color palette.
    Features:
    - Authentic vanilla Tarot frame and Roman numeral plaque (XVI)
    - Detailed celestial radiating woodcut sunburst and fine diagonal hatching across the sky
    - Celestial 4-point diamond stars and stippled parchment texture
    - Baroque oval mirror frame with top acanthus crest and side curls
    - Reflective beveled glass with twin playing card silhouettes and glowing diamond seal matrix
    - Fluted baroque column handle with carved pommel and finial
    - Pristine bottom banner with centered woodcut title lettering MIRROR
    """
    img = create_tarot_base("XVI", "MIRROR")
    draw = ImageDraw.Draw(img)

    C_SLATE = (79, 99, 103, 255)
    C_AMBER = (165, 133, 71, 255)
    C_GOLD = (218, 183, 114, 255)
    C_CREAM = (255, 229, 180, 255)
    C_WHITE = (255, 255, 255, 255)

    cx, cy = 35, 38

    # 1. Background: Intricate Celestial Sunburst Radiance & Woodcut Cross-Hatching
    # Seamlessly covers the entire interior illustration canvas including upper flanks (around plaque)
    # and lower flanks (around banner), strictly bounded by frame borders
    for y in range(95):
        for x in range(71):
            if not is_interior_canvas(x, y):
                continue
            dist = math.hypot(x - cx, y - cy)
            angle = math.atan2(y - cy, x - cx)
            ray_idx = int((angle + math.pi) / (math.pi / 8.0)) % 16

            if ray_idx % 2 == 1:
                # Shaded ray: fine diagonal woodcut hatching
                if (x + y) % 3 == 0:
                    img.putpixel((x, y), C_AMBER)
                elif (x + y) % 3 == 1:
                    img.putpixel((x, y), C_GOLD)
                else:
                    img.putpixel((x, y), C_CREAM)
            else:
                # Light ray: cream with fine golden stippling towards outer edges
                if dist > 26 and (x ^ y) % 7 == 0:
                    img.putpixel((x, y), C_GOLD)
                elif dist > 34 and (x + y) % 5 == 0:
                    img.putpixel((x, y), C_WHITE)
                else:
                    img.putpixel((x, y), C_CREAM)

    # Radiating fine engraved boundary lines for beams (stops strictly at frame / plaque / banner)
    for angle_deg in range(0, 360, 22):
        rad = math.radians(angle_deg)
        for px, py in trace_tarot_ray(cx, cy, rad, 18, 55):
            img.putpixel((px, py), C_GOLD)

    # Celestial 4-point diamond stars in the sky and flanks (strictly within interior canvas)
    stars = [
        (16, 8), (54, 8),   # Upper flanks left & right of plaque
        (15, 16), (55, 16),
        (14, 32), (56, 32),
        (14, 62), (56, 62),
        (20, 72), (50, 72),
        (10, 85), (60, 85)  # Lower flanks left & right of banner
    ]
    for sx, sy in stars:
        if is_interior_canvas(sx, sy):
            img.putpixel((sx, sy), C_WHITE)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if is_interior_canvas(sx + dx, sy + dy):
                    img.putpixel((sx + dx, sy + dy), C_WHITE)
            for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                if is_interior_canvas(sx + dx, sy + dy):
                    img.putpixel((sx + dx, sy + dy), C_GOLD)

    # 2. Baroque Ornate Frame Outer Silhouette (Oval: x in [17, 53], y in [18, 58])
    draw.ellipse([17, 18, 53, 58], fill=C_GOLD, outline=C_SLATE)
    draw.ellipse([18, 19, 52, 57], outline=C_CREAM)
    draw.ellipse([19, 20, 51, 56], fill=C_AMBER)

    # Acanthus leaf crown crest at top (x in [29, 41], y in [12, 20])
    draw.polygon([(35, 12), (32, 16), (29, 14), (31, 20), (39, 20), (41, 14), (38, 16)], fill=C_GOLD, outline=C_SLATE)
    draw.line([(35, 13), (35, 19)], fill=C_SLATE)
    draw.point((35, 15), fill=C_WHITE)

    # Side decorative flourishes on frame (acanthus curls at 9 o'clock and 3 o'clock)
    draw.arc([13, 34, 19, 42], start=90, end=270, fill=C_SLATE, width=2)
    draw.arc([14, 35, 18, 41], start=90, end=270, fill=C_GOLD, width=1)
    draw.arc([51, 34, 57, 42], start=270, end=90, fill=C_SLATE, width=2)
    draw.arc([52, 35, 56, 41], start=270, end=90, fill=C_GOLD, width=1)

    # 3. Inner Beveled Glass Rim & Reflective Mirror Surface
    draw.ellipse([21, 22, 49, 54], fill=C_SLATE)
    draw.ellipse([22, 23, 48, 53], fill=C_CREAM)

    # Glass surface woodcut gradient & reflection
    for gy in range(24, 53):
        for gx in range(23, 48):
            nx = (gx - 35) / 12.0
            ny = (gy - 38) / 14.0
            if nx * nx + ny * ny <= 1.0:
                diag = (gx + gy) / 75.0
                if diag < 0.70:
                    col = C_WHITE if (gx + gy) % 2 == 0 else C_CREAM
                elif diag < 0.84:
                    col = C_CREAM if (gx + gy) % 2 == 0 else C_GOLD
                else:
                    col = C_GOLD if (gx + gy) % 2 == 0 else C_AMBER
                img.putpixel((gx, gy), col)

    # Dynamic specular white reflection streaks slicing diagonally across the mirror
    draw.line([(26, 26), (32, 32)], fill=C_WHITE, width=2)
    draw.line([(34, 34), (38, 38)], fill=C_WHITE, width=1)

    # 4. Magical Reflection Inside the Glass: Twin Playing Cards & Mystic Diamond Matrix
    # Left Card (Source): x=27..34, y=36..47
    draw.rectangle([27, 36, 34, 47], fill=C_CREAM, outline=C_SLATE)
    draw.line([(28, 37), (33, 37)], fill=C_WHITE)
    draw.point((30, 41), fill=C_AMBER); draw.point((31, 41), fill=C_AMBER)
    draw.point((30, 42), fill=C_AMBER); draw.point((31, 42), fill=C_AMBER)

    # Right Card (Target being enhanced): x=36..43, y=35..46
    draw.rectangle([36, 35, 43, 46], fill=C_WHITE, outline=C_SLATE)
    draw.line([(37, 36), (42, 36)], fill=C_CREAM)
    # Golden seal diamond matrix glowing on the enhanced card
    draw.polygon([(39, 39), (41, 41), (39, 43), (37, 41)], fill=C_GOLD, outline=C_SLATE)
    draw.point((39, 41), fill=C_WHITE)

    # Connecting mystical radiance sparks between cards
    draw.point((35, 38), fill=C_GOLD)
    draw.point((35, 43), fill=C_GOLD)
    draw.point((35, 40), fill=C_WHITE)

    # 5. Baroque Carved Handle: x in [32, 38], y in [58, 77]
    draw.polygon([(32, 58), (38, 58), (36, 62), (34, 62)], fill=C_GOLD, outline=C_SLATE)
    draw.rectangle([33, 62, 37, 72], fill=C_GOLD, outline=C_SLATE)
    draw.line([(34, 63), (34, 71)], fill=C_WHITE)
    draw.line([(35, 63), (35, 71)], fill=C_CREAM)
    draw.line([(36, 63), (36, 71)], fill=C_AMBER)
    draw.line([(33, 65), (37, 65)], fill=C_SLATE)
    draw.line([(33, 69), (37, 69)], fill=C_SLATE)
    draw.polygon([(35, 76), (32, 73), (38, 73)], fill=C_GOLD, outline=C_SLATE)
    draw.point((35, 74), fill=C_WHITE)

    export_sprite(img, "c_the_mirror.png")

def build_c_the_weakness():
    """Builds The Weakness Tarot Card (71x95, 2x 142x190)
    Effect: Decreases rank of up to 2 selected cards by 1.
    100% authentic Balatro Tarot woodcut style adhering strictly to the official 5-color palette.
    Features:
    - Authentic vanilla Tarot frame and Roman numeral plaque (XI counterpart to Strength)
    - Detailed celestial shockwave rays and woodcut diagonal cross-hatching across the sky
    - Knight's heraldic heater shield with weathered steel face and beveled gold rim
    - Ceremonial sword driven vertically through center with a violent dramatic jagged fracture
    - Snapped lower blade section deflected and angled with flying sharp steel shards
    - Withered thorny briar vines and drooping wild rosebuds in woodcut cross-hatching
    - Weeping sorrow power droplets draining downwards
    - Pristine bottom banner with centered woodcut title lettering WEAKNESS
    """
    img = create_tarot_base("XI", "WEAKNESS")
    draw = ImageDraw.Draw(img)

    C_SLATE = (79, 99, 103, 255)
    C_AMBER = (165, 133, 71, 255)
    C_GOLD = (218, 183, 114, 255)
    C_CREAM = (255, 229, 180, 255)
    C_WHITE = (255, 255, 255, 255)

    cx, cy = 35, 44

    # 1. Background: Engraved Woodcut Cross-Hatching & Shockwave Fracture Rays
    # Seamlessly covers the entire interior illustration canvas including upper flanks (around plaque)
    # and lower flanks (around banner), strictly bounded by frame borders
    for y in range(95):
        for x in range(71):
            if not is_interior_canvas(x, y):
                continue
            dist = math.hypot(x - cx, y - cy)
            angle = math.atan2(y - cy, x - cx)
            ray_idx = int((angle + math.pi) / (math.pi / 6.0)) % 12

            # Background diagonal woodcut hatching outside the shield
            if (x < 18 or x > 52 or y < 22 or y > 66):
                if ray_idx % 2 == 1:
                    if (x - y) % 3 == 0:
                        img.putpixel((x, y), C_AMBER)
                    elif (x - y) % 3 == 1:
                        img.putpixel((x, y), C_GOLD)
                    else:
                        img.putpixel((x, y), C_CREAM)
                else:
                    if dist > 25 and (x + y) % 4 == 0:
                        img.putpixel((x, y), C_GOLD)
                    else:
                        img.putpixel((x, y), C_CREAM)

    # Radiating shockwave burst lines (stops strictly at frame / plaque / banner)
    for angle_deg in range(15, 360, 30):
        rad = math.radians(angle_deg)
        for px, py in trace_tarot_ray(cx, cy, rad, 16, 55):
            if not (18 <= px <= 52 and 22 <= py <= 65):
                img.putpixel((px, py), C_GOLD)

    # Diamond stars & glints in corners and flanks (strictly within interior canvas)
    stars = [
        (16, 8), (54, 8),   # Upper flanks left & right of plaque
        (15, 16), (55, 16),
        (14, 28), (56, 28),
        (14, 70), (56, 70),
        (10, 85), (60, 85)  # Lower flanks left & right of banner
    ]
    for sx, sy in stars:
        if is_interior_canvas(sx, sy):
            img.putpixel((sx, sy), C_WHITE)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if is_interior_canvas(sx + dx, sy + dy):
                    img.putpixel((sx + dx, sy + dy), C_WHITE)
            for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                if is_interior_canvas(sx + dx, sy + dy):
                    img.putpixel((sx + dx, sy + dy), C_GOLD)

    # 2. Heraldic Heater Shield (x in [18, 52], y in [22, 65])
    shield_pts = [(19, 23), (51, 23), (52, 44), (35, 66), (18, 44)]
    draw.polygon(shield_pts, fill=C_AMBER, outline=C_SLATE)

    # Inner gold border
    inner_pts = [(21, 25), (49, 25), (50, 43), (35, 63), (20, 43)]
    draw.polygon(inner_pts, fill=C_CREAM, outline=C_GOLD)
    draw.line([(22, 26), (48, 26)], fill=C_WHITE)

    # Shield interior woodcut cross-hatching
    for sy in range(27, 63):
        for sx in range(22, 49):
            if (sx + sy) % 3 == 0:
                img.putpixel((sx, sy), C_GOLD)
            elif (sx - sy) % 4 == 0:
                img.putpixel((sx, sy), C_AMBER)

    # 3. Knight's Ceremonial Sword Driven Vertically Through Center (x=35)
    # Pommel
    draw.ellipse([33, 14, 37, 18], fill=C_GOLD, outline=C_SLATE)
    draw.point((35, 15), fill=C_WHITE)
    # Grip
    draw.rectangle([34, 18, 36, 22], fill=C_AMBER, outline=C_SLATE)
    draw.line([(34, 19), (36, 19)], fill=C_GOLD)
    draw.line([(34, 21), (36, 21)], fill=C_GOLD)
    # Crossguard
    draw.rectangle([27, 22, 43, 25], fill=C_GOLD, outline=C_SLATE)
    draw.line([(28, 23), (42, 23)], fill=C_WHITE)
    draw.point((27, 24), fill=C_SLATE); draw.point((43, 24), fill=C_SLATE)

    # Upper Blade Section (y=25..40, centered at x=35)
    draw.rectangle([33, 26, 37, 40], fill=C_CREAM, outline=C_SLATE)
    draw.line([(35, 26), (35, 40)], fill=C_SLATE)
    draw.line([(34, 26), (34, 40)], fill=C_WHITE)
    draw.line([(36, 26), (36, 40)], fill=C_GOLD)

    # 4. The Dramatic Violent Fracture / Crack (y=40..46)
    crack_pts = [(33, 40), (37, 42), (32, 44), (38, 46), (34, 48)]
    for i in range(len(crack_pts) - 1):
        draw.line([crack_pts[i], crack_pts[i + 1]], fill=C_SLATE, width=2)

    # Spidering fractures across shield
    draw.line([(33, 41), (22, 38)], fill=C_SLATE, width=2)
    draw.line([(22, 38), (18, 42)], fill=C_SLATE, width=1)
    draw.line([(37, 43), (48, 46)], fill=C_SLATE, width=2)
    draw.line([(48, 46), (52, 50)], fill=C_SLATE, width=1)

    # Lower Broken Blade Section (Snapped & Shifted slightly right to x=36..39, y=47..66)
    draw.polygon([(36, 47), (39, 47), (38, 64), (35, 67), (34, 63)], fill=C_CREAM, outline=C_SLATE)
    draw.line([(36, 48), (36, 63)], fill=C_WHITE)
    draw.line([(37, 48), (37, 63)], fill=C_SLATE)

    # Flying sharp steel shards
    draw.polygon([(26, 43), (29, 41), (28, 45)], fill=C_WHITE, outline=C_SLATE)
    draw.polygon([(42, 47), (45, 45), (43, 49)], fill=C_WHITE, outline=C_SLATE)
    draw.point((30, 48), fill=C_WHITE)
    draw.point((41, 42), fill=C_WHITE)

    # 5. Withered Dark Thorns & Briar Vines wrapping around the broken weapon
    vine_pts1 = [(17, 32), (24, 34), (32, 31), (39, 36), (46, 33), (53, 36)]
    for i in range(len(vine_pts1) - 1):
        draw.line([vine_pts1[i], vine_pts1[i + 1]], fill=C_SLATE, width=2)
    draw.line([(25, 34), (27, 37)], fill=C_AMBER)
    draw.line([(42, 35), (44, 38)], fill=C_AMBER)

    vine_pts2 = [(16, 48), (24, 45), (34, 49), (42, 47), (49, 54), (35, 62)]
    for i in range(len(vine_pts2) - 1):
        draw.line([vine_pts2[i], vine_pts2[i + 1]], fill=C_SLATE, width=2)
    draw.line([(22, 46), (20, 44)], fill=C_AMBER)
    draw.line([(44, 48), (46, 46)], fill=C_AMBER)

    # Two Wilted, Drooping Rosebuds in Woodcut Engraving
    draw.ellipse([18, 35, 23, 40], fill=C_AMBER, outline=C_SLATE)
    draw.point((20, 37), fill=C_GOLD)
    draw.ellipse([16, 43, 18, 47], fill=C_AMBER, outline=C_SLATE)
    draw.ellipse([47, 38, 52, 43], fill=C_AMBER, outline=C_SLATE)
    draw.point((49, 40), fill=C_GOLD)
    draw.ellipse([53, 46, 55, 50], fill=C_AMBER, outline=C_SLATE)

    # 6. Weeping Sorrow Power Droplets (draining downwards)
    draw.polygon([(35, 50), (33, 54), (37, 54)], fill=C_GOLD, outline=C_SLATE)
    draw.ellipse([33, 52, 37, 56], fill=C_GOLD, outline=C_SLATE)
    draw.point((34, 53), fill=C_WHITE)
    draw.ellipse([35, 60, 38, 64], fill=C_GOLD, outline=C_SLATE)
    draw.point((36, 61), fill=C_WHITE)
    draw.ellipse([33, 71, 37, 75], fill=C_GOLD, outline=C_SLATE)
    draw.point((34, 72), fill=C_WHITE)
    draw.ellipse([27, 55, 29, 58], fill=C_GOLD, outline=C_SLATE)
    draw.ellipse([43, 57, 45, 60], fill=C_GOLD, outline=C_SLATE)

    export_sprite(img, "c_weakness.png")

def build_c_swaper():
    """Builds The Swapper Tarot Card (71x95, 2x 142x190)
    Effect: Select 2 cards, swap all Enhancements, Editions, and Seals between them.
    100% authentic Balatro Tarot woodcut style adhering strictly to official 5-color palette.
    Features:
    - Authentic vanilla Tarot frame and Roman numeral plaque (XVI)
    - Fully detailed celestial radiating woodcut sunburst and fine diagonal hatching across the entire canvas
    - Celestial 4-point diamond stars and stippled parchment texture across flanks and corners
    - Two miniature playing cards in the background being swapped in pure Tarot woodcut style
    - Prominent circular golden swap arrows with sharp arrowheads in dynamic clockwise rotation
    - Flying essence sparkles along the swap arcs
    - Central mystical exchange star glint
    - Pristine bottom banner with centered woodcut title lettering SWAPPER
    Strictly limited to the 5 official Balatro Tarot colors: Slate, Amber, Gold, Cream, White.
    """
    img = create_tarot_base("XVI", "SWAPPER")
    draw = ImageDraw.Draw(img)

    C_SLATE = (79, 99, 103, 255)
    C_AMBER = (165, 133, 71, 255)
    C_GOLD  = (218, 183, 114, 255)
    C_CREAM = (255, 229, 180, 255)
    C_WHITE = (255, 255, 255, 255)

    cx, cy = 35, 46

    # 1. Background: Intricate Celestial Sunburst Radiance & Woodcut Cross-Hatching
    # Seamlessly covers the entire interior illustration canvas including upper flanks (around plaque)
    # and lower flanks (around banner), strictly bounded by frame borders
    for y in range(95):
        for x in range(71):
            if not is_interior_canvas(x, y):
                continue
            dist = math.hypot(x - cx, y - cy)
            angle = math.atan2(y - cy, x - cx)
            ray_idx = int((angle + math.pi) / (math.pi / 8.0)) % 16

            if ray_idx % 2 == 1:
                # Shaded ray: fine diagonal woodcut hatching
                if (x + y) % 3 == 0:
                    img.putpixel((x, y), C_AMBER)
                elif (x + y) % 3 == 1:
                    img.putpixel((x, y), C_GOLD)
                else:
                    img.putpixel((x, y), C_CREAM)
            else:
                # Light ray: cream with fine golden stippling towards outer edges
                if dist > 22 and (x ^ y) % 6 == 0:
                    img.putpixel((x, y), C_GOLD)
                elif dist > 32 and (x + y) % 4 == 0:
                    img.putpixel((x, y), C_WHITE)
                else:
                    img.putpixel((x, y), C_CREAM)

    # Radiating fine engraved boundary lines for beams
    for angle_deg in range(0, 360, 20):
        rad = math.radians(angle_deg)
        for px, py in trace_tarot_ray(cx, cy, rad, 16, 55):
            img.putpixel((px, py), C_AMBER)

    # Celestial 4-point diamond stars in the sky, flanks, and around banners
    stars = [
        (16, 8), (54, 8),   # Upper flanks left & right of plaque
        (14, 18), (56, 18),
        (13, 30), (57, 30),
        (13, 62), (57, 62),
        (18, 74), (52, 74),
        (10, 85), (60, 85)  # Lower flanks left & right of banner
    ]
    for sx, sy in stars:
        if is_interior_canvas(sx, sy):
            draw.line([(sx - 2, sy), (sx + 2, sy)], fill=C_SLATE)
            draw.line([(sx, sy - 2), (sx, sy + 2)], fill=C_SLATE)
            img.putpixel((sx, sy), C_WHITE)

    # 2. Glowing Halo Ring behind the cards
    for deg in range(360):
        rad = math.radians(deg)
        for r in (22, 23):
            hx = int(cx + r * math.cos(rad))
            hy = int(cy + r * math.sin(rad))
            if is_interior_canvas(hx, hy):
                img.putpixel((hx, hy), C_GOLD if (hx + hy) % 2 == 0 else C_AMBER)

    # 3. Two miniature playing cards being swapped (Pure Tarot woodcut palette)
    # Left card: x=20..31, y=37..54
    draw.rectangle([20, 37, 31, 54], fill=C_WHITE, outline=C_SLATE)
    draw.rectangle([22, 39, 29, 52], outline=C_GOLD)
    # Left card interior: ornate woodcut diamond pip & corner accents
    draw.polygon([(25, 42), (28, 45), (25, 48), (22, 45)], fill=C_AMBER)
    draw.polygon([(25, 43), (27, 45), (25, 47), (23, 45)], fill=C_GOLD)
    draw.point((25, 45), fill=C_WHITE)
    draw.point((23, 40), fill=C_SLATE)
    draw.point((28, 51), fill=C_SLATE)

    # Right card: x=39..50, y=37..54
    draw.rectangle([39, 37, 50, 54], fill=C_WHITE, outline=C_SLATE)
    draw.rectangle([41, 39, 48, 52], outline=C_GOLD)
    # Right card interior: ornate woodcut celestial cross & corner accents
    draw.polygon([(44, 42), (47, 45), (44, 48), (41, 45)], fill=C_AMBER)
    draw.polygon([(44, 43), (46, 45), (44, 47), (42, 45)], fill=C_GOLD)
    draw.point((44, 45), fill=C_WHITE)
    draw.point((42, 40), fill=C_SLATE)
    draw.point((47, 51), fill=C_SLATE)

    # 4. Circular Swap Arrows (Outer dynamic arcs representing clockwise exchange)
    arrow_r = 18

    # Top curved arrow (arcs from 195 deg to 345 deg)
    for deg in range(195, 345, 2):
        rad = math.radians(deg)
        for t in (-1, 0, 1):
            ax = int(cx + (arrow_r + t) * math.cos(rad))
            ay = int(cy + (arrow_r + t) * math.sin(rad))
            if is_interior_canvas(ax, ay):
                img.putpixel((ax, ay), C_GOLD)
        ax_in = int(cx + (arrow_r - 2) * math.cos(rad))
        ay_in = int(cy + (arrow_r - 2) * math.sin(rad))
        ax_out = int(cx + (arrow_r + 2) * math.cos(rad))
        ay_out = int(cy + (arrow_r + 2) * math.sin(rad))
        if is_interior_canvas(ax_in, ay_in): img.putpixel((ax_in, ay_in), C_SLATE)
        if is_interior_canvas(ax_out, ay_out): img.putpixel((ax_out, ay_out), C_SLATE)

    # Top Arrowhead pointing downward to the right (towards Right Card)
    draw.polygon([(53, 46), (47, 39), (55, 38)], fill=C_GOLD, outline=C_SLATE)
    draw.line([(48, 40), (52, 45)], fill=C_WHITE)

    # Bottom curved arrow (arcs from 15 deg to 165 deg)
    for deg in range(15, 165, 2):
        rad = math.radians(deg)
        for t in (-1, 0, 1):
            ax = int(cx + (arrow_r + t) * math.cos(rad))
            ay = int(cy + (arrow_r + t) * math.sin(rad))
            if is_interior_canvas(ax, ay):
                img.putpixel((ax, ay), C_GOLD)
        ax_in = int(cx + (arrow_r - 2) * math.cos(rad))
        ay_in = int(cy + (arrow_r - 2) * math.sin(rad))
        ax_out = int(cx + (arrow_r + 2) * math.cos(rad))
        ay_out = int(cy + (arrow_r + 2) * math.sin(rad))
        if is_interior_canvas(ax_in, ay_in): img.putpixel((ax_in, ay_in), C_SLATE)
        if is_interior_canvas(ax_out, ay_out): img.putpixel((ax_out, ay_out), C_SLATE)

    # Bottom Arrowhead pointing upward to the left (towards Left Card)
    draw.polygon([(17, 46), (23, 53), (15, 54)], fill=C_GOLD, outline=C_SLATE)
    draw.line([(22, 52), (18, 47)], fill=C_WHITE)

    # 5. Particle exchange trails (Pure Tarot gold/white):
    draw.point((30, 27), fill=C_GOLD)
    draw.point((38, 27), fill=C_WHITE)
    draw.point((40, 65), fill=C_GOLD)
    draw.point((32, 65), fill=C_WHITE)

    # 6. Central Mystical Exchange Glyphs (between the two cards)
    draw.line([(cx - 2, cy), (cx + 2, cy)], fill=C_SLATE)
    draw.line([(cx, cy - 2), (cx, cy + 2)], fill=C_SLATE)
    draw.point((cx, cy), fill=C_WHITE)

    export_sprite(img, "c_swaper.png")

SPECTRAL_FONT = {
    'P': [
        '### ',
        '## #',
        '## #',
        '### ',
        '##  ',
        '##  '
    ],
    'H': [
        '## #',
        '## #',
        '## #',
        '####',
        '## #',
        '## #'
    ],
    'A': [
        ' ## ',
        '### ',
        '## #',
        '####',
        '## #',
        '## #'
    ],
    'N': [
        '##  ##',
        '### ##',
        '# ####',
        '#  ###',
        '#   ##',
        '#   ##'
    ],
    'T': [
        '####',
        ' ## ',
        ' ## ',
        ' ## ',
        ' ## ',
        ' ## '
    ],
    'S': [
        ' ###',
        '##  ',
        ' ## ',
        '  ##',
        ' ###',
        '### '
    ],
    'M': [
        '##  #  ',
        '#### # ',
        '#######',
        '## # ##',
        '## # ##',
        '## # ##'
    ],
    'E': [
        '####',
        '##  ',
        '### ',
        '##  ',
        '##  ',
        '####'
    ],
    'C': [
        ' ###',
        '##  ',
        '##  ',
        '##  ',
        '##  ',
        ' ###'
    ]
}

def create_clean_spectral_base(banner_text):
    """Creates a 100% authentic Balatro Spectral Card base with the signature frame intact.
    Features:
    - Pristine outer card border and transparent rounded corners
    - Full authentic Balatro inner ornate frame: outer shadow, frame line, dark slate bevel,
      and inset ecto-white pinstripe border (x=9..61, y=6..75)
    - Clean deep navy void (78, 87, 121) inside the frame picture window (x=10..60, y=7..74)
    - Seamless authentic Balatro scroll ribbon banner (y=80..91) with intact ornate folds
      at left (x=8..11) and right (x=59..62) and authentic pixel-art title typography
    """
    template_path = os.path.join(BASE_DIR, "tools", "vanilla", "spectral_frame.png")
    if not os.path.exists(template_path):
        template_path = os.path.join(BASE_DIR, "tools", "scratch", "spectral_perfect_frame.png")
    base = Image.open(template_path).copy()

    C_OUTLINE = (79, 99, 103, 255)
    C_DARK_BG = (78, 87, 121, 255)
    C_ECTO = (226, 235, 249, 255)

    # 1. Clean the interior picture window (x=10..60, y=7..74) inside the frame
    for y in range(7, 75):
        for x in range(10, 61):
            if (x, y) in [(10, 7), (60, 7), (10, 74), (60, 74)]:
                base.putpixel((x, y), C_ECTO)
            else:
                base.putpixel((x, y), C_DARK_BG)

    # 2. Clear banner text area strictly within inner banner body (x=12..58, y=83..88)
    # Never touches the ornate ribbon fold borders at x=8..11 and x=59..62
    for y in range(83, 89):
        for x in range(12, 59):
            base.putpixel((x, y), C_ECTO)

    # 3. Draw Title Text
    widths = [len(SPECTRAL_FONT[ch][0]) for ch in banner_text]
    total_w = sum(widths) + (len(banner_text) - 1)
    cur_x = int(round(35.0 - total_w / 2.0))
    for i, ch in enumerate(banner_text):
        grid = SPECTRAL_FONT[ch]
        for row_idx, row in enumerate(grid):
            for col_idx, char in enumerate(row):
                if char == '#':
                    base.putpixel((cur_x + col_idx, 83 + row_idx), C_OUTLINE)
        cur_x += widths[i] + 1

    return base

def build_c_phantasm():
    """Builds Phantasm Spectral Card (71x95, 2x 142x190)
    Effect: Add a random Seal to 2 selected cards in your hand.
    Authentic Balatro spectral card featuring a floating hooded ethereal spectre conjuring glowing
    mystical seals onto two hovering playing cards inside the signature vanilla Spectral card frame.
    Strictly complies with the authentic Spectral card color palette.
    """
    base = create_clean_spectral_base("PHANTASM")
    draw = ImageDraw.Draw(base)

    C_OUTLINE = (79, 99, 103, 255)       # Dark Slate #4F6367
    C_DARK_BG = (78, 87, 121, 255)       # Dark Navy #4E5779
    C_MID_NAVY = (94, 114, 151, 255)     # Mid Navy #5E7297
    C_BLUE = (99, 143, 225, 255)         # Spectral Blue #638FE1
    C_LIGHT_BLUE = (122, 164, 242, 255)  # Light Blue #7AA4F2
    C_ECTO = (226, 235, 249, 255)        # Ecto #E2EBF9
    C_WHITE = (255, 255, 255, 255)       # White #FFFFFF
    C_GOLD = (199, 178, 74, 255)         # Spectral Gold #C7B24A
    C_BRASS = (167, 156, 103, 255)       # Brass #A79C67

    # Subtle celestial dither inside picture window
    for y in range(7, 75):
        for x in range(10, 61):
            if (x, y) not in [(10, 7), (60, 7), (10, 74), (60, 74)]:
                dist = math.hypot(x - 35, y - 36)
                if dist < 24 and (x + y) % 2 == 0:
                    base.putpixel((x, y), C_MID_NAVY)
                else:
                    base.putpixel((x, y), C_DARK_BG)

    # 1. Celestial Energy tendrils rising in background
    tendrils = [
        [(17, 50), (14, 38), (17, 26), (22, 16), (27, 12)],
        [(53, 50), (56, 38), (53, 26), (48, 16), (43, 12)],
        [(23, 44), (21, 34), (24, 24), (29, 15)],
        [(47, 44), (49, 34), (46, 24), (41, 15)],
    ]
    for tendril in tendrils:
        for i in range(len(tendril) - 1):
            draw.line([tendril[i], tendril[i+1]], fill=C_BLUE, width=1)

    # 2. Floating Phantom Spirit (Hooded Ethereal Spectre)
    phantom_body = [
        (35, 12), (39, 13), (43, 16), (46, 21), (46, 27),
        (43, 32), (45, 38), (43, 42), (39, 39), (35, 44),
        (31, 39), (27, 42), (25, 38), (27, 32), (24, 27),
        (24, 21), (27, 16), (31, 13)
    ]
    draw.polygon(phantom_body, fill=C_ECTO, outline=C_OUTLINE)

    # Shaded folds in robes
    draw.line([(31, 20), (29, 34)], fill=C_MID_NAVY)
    draw.line([(39, 20), (41, 34)], fill=C_MID_NAVY)
    draw.line([(35, 24), (35, 41)], fill=C_WHITE)

    # Deep shadowy hood interior
    hood = [
        (32, 17), (38, 17), (41, 21), (40, 25),
        (35, 28), (30, 25), (29, 21)
    ]
    draw.polygon(hood, fill=C_DARK_BG, outline=C_OUTLINE)

    # Piercing glowing eyes
    draw.point((32, 21), fill=C_WHITE)
    draw.point((33, 21), fill=C_LIGHT_BLUE)
    draw.point((37, 21), fill=C_LIGHT_BLUE)
    draw.point((38, 21), fill=C_WHITE)

    # Outstretched glowing spirit hands channeling magic
    draw.ellipse([19, 29, 23, 33], fill=C_WHITE, outline=C_OUTLINE)
    draw.line([(21, 33), (21, 40)], fill=C_LIGHT_BLUE)
    draw.line([(22, 33), (24, 42)], fill=C_BLUE)

    draw.ellipse([47, 29, 51, 33], fill=C_WHITE, outline=C_OUTLINE)
    draw.line([(49, 33), (49, 40)], fill=C_LIGHT_BLUE)
    draw.line([(48, 33), (46, 42)], fill=C_BLUE)

    # 3. Two Floating Playing Cards (Target of the Seal Conjuration)
    # Left Card
    card_l = [(13, 44), (26, 41), (28, 64), (15, 67)]
    draw.polygon(card_l, fill=C_ECTO, outline=C_OUTLINE)
    card_l_face = [(15, 46), (24, 43), (26, 62), (17, 65)]
    draw.polygon(card_l_face, fill=C_DARK_BG)

    # Right Card
    card_r = [(44, 41), (57, 44), (55, 67), (42, 64)]
    draw.polygon(card_r, fill=C_ECTO, outline=C_OUTLINE)
    card_r_face = [(46, 43), (55, 46), (53, 65), (44, 62)]
    draw.polygon(card_r_face, fill=C_DARK_BG)

    # 4. Glowing Seal Matrices Branded on Cards!
    # Left Seal (center at 20, 54)
    draw.ellipse([17, 51, 24, 58], fill=C_GOLD, outline=C_OUTLINE)
    draw.ellipse([18, 52, 23, 57], fill=C_BRASS)
    draw.point((20, 54), fill=C_WHITE)
    draw.point((21, 54), fill=C_WHITE)
    draw.point((20, 53), fill=C_LIGHT_BLUE)
    draw.point((20, 55), fill=C_LIGHT_BLUE)
    draw.point((19, 54), fill=C_LIGHT_BLUE)
    draw.point((22, 54), fill=C_LIGHT_BLUE)
    draw.line([(21, 33), (20, 50)], fill=C_LIGHT_BLUE)
    draw.point((20, 48), fill=C_WHITE)

    # Right Seal (center at 49, 54)
    draw.ellipse([46, 51, 53, 58], fill=C_GOLD, outline=C_OUTLINE)
    draw.ellipse([47, 52, 52, 57], fill=C_BRASS)
    draw.point((49, 54), fill=C_WHITE)
    draw.point((50, 54), fill=C_WHITE)
    draw.point((49, 53), fill=C_LIGHT_BLUE)
    draw.point((49, 55), fill=C_LIGHT_BLUE)
    draw.point((48, 54), fill=C_LIGHT_BLUE)
    draw.point((51, 54), fill=C_LIGHT_BLUE)
    draw.line([(49, 33), (49, 50)], fill=C_LIGHT_BLUE)
    draw.point((49, 48), fill=C_WHITE)

    # 5. Floating Seal Embers & Brand Runes
    embers = [(11, 54), (32, 48), (38, 48), (59, 54), (35, 61), (24, 69), (46, 69)]
    for ex, ey in embers:
        draw.point((ex, ey), fill=C_GOLD)
        draw.point((ex + 1, ey), fill=C_LIGHT_BLUE)

    export_sprite(base, "c_phantasm.png")
    return base

def build_c_pact():
    """Builds Pact Spectral Card (71x95, 2x 142x190)
    Authentic Balatro spectral card featuring the Golden Ouroboros Infinity Snake and payout wealth
    inside the signature vanilla Spectral card frame.
    Strictly complies with the authentic Spectral card color palette.
    """
    base = create_clean_spectral_base("PACT")
    draw = ImageDraw.Draw(base)

    C_OUTLINE = (79, 99, 103, 255)
    C_DARK_BG = (78, 87, 121, 255)
    C_MID_NAVY = (94, 114, 151, 255)
    C_BLUE = (99, 143, 225, 255)
    C_LIGHT_BLUE = (122, 164, 242, 255)
    C_ECTO = (226, 235, 249, 255)
    C_WHITE = (255, 255, 255, 255)
    C_GOLD = (199, 178, 74, 255)
    C_BRASS = (167, 156, 103, 255)

    # Subtle celestial dither inside picture window
    for y in range(7, 75):
        for x in range(10, 61):
            if (x, y) not in [(10, 7), (60, 7), (10, 74), (60, 74)]:
                dist = math.hypot(x - 35, y - 37)
                if dist < 23 and (x + y) % 2 == 0:
                    base.putpixel((x, y), C_MID_NAVY)
                else:
                    base.putpixel((x, y), C_DARK_BG)

    # 1. Celestial Radiant Burst behind the snake
    burst_rays = [
        (0, 23), (20, 19), (40, 24), (60, 20), (80, 25), (100, 21), (120, 24), (140, 19),
        (160, 23), (180, 20), (200, 24), (220, 19), (240, 25), (260, 20), (280, 24), (300, 19), (320, 23), (340, 20)
    ]
    for deg, r in burst_rays:
        rad = math.radians(deg)
        x2 = int(round(35 + r * math.cos(rad)))
        y2 = int(round(37 + (r * 0.75) * math.sin(rad)))
        draw.line([(35, 37), (x2, y2)], fill=C_BLUE, width=1)
        x_in = int(round(35 + (r - 4) * math.cos(rad)))
        y_in = int(round(37 + ((r - 4) * 0.75) * math.sin(rad)))
        draw.line([(35, 37), (x_in, y_in)], fill=C_ECTO, width=1)

    # 2. Golden Ouroboros Infinity Snake
    cx, cy = 35.5, 37.0
    a, b = 15.0, 12.0

    curve = []
    num_steps = 360
    for i in range(num_steps):
        t = (2 * math.pi * i) / num_steps
        denom = 1 + (math.sin(t) ** 2)
        px = cx + (a * math.cos(t)) / denom
        py = cy + (b * math.sin(t) * math.cos(t)) / denom
        curve.append((px, py))

    # Snake body outline
    for px, py in curve:
        ix, iy = int(round(px)), int(round(py))
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                if dx*dx + dy*dy <= 9:
                    base.putpixel((ix + dx, iy + dy), C_OUTLINE)

    # Snake body core with segmented scales
    for i, (px, py) in enumerate(curve):
        ix, iy = int(round(px)), int(round(py))
        seg = (i // 12) % 2
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                dist2 = dx*dx + dy*dy
                if dist2 <= 4:
                    col = C_ECTO if dy > 0 else (C_GOLD if seg == 0 else C_BRASS)
                    base.putpixel((ix + dx, iy + dy), col)

    # Crossover: right-to-left strand passes over left-to-right strand
    for px, py in curve[70:110]:
        ix, iy = int(round(px)), int(round(py))
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                if dx*dx + dy*dy <= 8:
                    base.putpixel((ix + dx, iy + dy), C_OUTLINE)
    for i, (px, py) in enumerate(curve[70:110]):
        ix, iy = int(round(px)), int(round(py))
        seg = ((i + 70) // 12) % 2
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx*dx + dy*dy <= 4:
                    col = C_ECTO if dy > 0 else (C_GOLD if seg == 0 else C_BRASS)
                    base.putpixel((ix + dx, iy + dy), col)

    # 3. Detailed Snake Head & Jaws eating tail
    head_poly = [
        (20, 35), (22, 31), (25, 29), (29, 29), (32, 31),
        (33, 33), (29, 35), (25, 35), (22, 37)
    ]
    draw.polygon(head_poly, fill=C_GOLD, outline=C_OUTLINE)
    draw.line([(24, 30), (28, 30)], fill=C_ECTO)
    draw.point((26, 31), fill=C_LIGHT_BLUE)
    draw.point((27, 31), fill=C_WHITE)

    # Upper jaw & fangs
    draw.polygon([(29, 31), (34, 32), (32, 34), (29, 33)], fill=C_GOLD, outline=C_OUTLINE)
    draw.point((32, 34), fill=C_WHITE)
    draw.point((33, 34), fill=C_WHITE)

    # Lower jaw & fangs
    draw.polygon([(26, 36), (32, 37), (30, 39), (25, 38)], fill=C_BRASS, outline=C_OUTLINE)
    draw.point((31, 36), fill=C_WHITE)
    draw.rectangle([29, 34, 31, 35], fill=C_DARK_BG)

    # Tail tip entering jaws
    tail_pts = [(33, 35), (36, 35), (35, 36), (32, 36)]
    draw.polygon(tail_pts, fill=C_ECTO, outline=C_OUTLINE)
    draw.point((31, 35), fill=C_ECTO)

    # 4. Pile of Golden Coins at bottom (y=57..69) representing $25 payout
    coins = [
        (24, 69), (28, 69), (32, 69), (36, 69), (40, 69), (44, 69),
        (26, 66), (30, 66), (34, 66), (38, 66), (42, 66),
        (28, 63), (32, 63), (36, 63), (40, 63),
        (30, 60), (34, 60), (38, 60),
        (34, 57)
    ]
    for cx, cy in coins:
        draw.ellipse([cx - 2, cy - 1, cx + 2, cy + 1], fill=C_GOLD, outline=C_OUTLINE)
        draw.point((cx - 1, cy - 1), fill=C_WHITE)
        draw.point((cx, cy), fill=C_BRASS)

    export_sprite(base, "c_pact.png")
    return base

def build_j_wrong_schematics():
    bp_blue = PALETTE["BP_BLUE"]
    bp_grid = PALETTE["BP_GRID"]
    bp_white = PALETTE["BP_WHITE"]
    red_mark = PALETTE["MULT_RED"]
    
    img = create_card_base(bg_color=bp_blue, border_color=(191, 199, 213, 255))
    draw = ImageDraw.Draw(img)

    for x in range(4, 68, 6):
        draw.line([(x, 3), (x, 91)], fill=bp_grid)
    for y in range(4, 92, 6):
        draw.line([(3, y), (67, y)], fill=bp_grid)

    draw.rectangle([4, 4, 66, 90], outline=bp_white)

    draw.line([(35, 34), (24, 28)], fill=bp_white, width=1)
    draw.line([(24, 28), (17, 34)], fill=bp_white, width=1)
    draw.line([(17, 34), (16, 42)], fill=bp_white, width=1)
    draw.ellipse([13, 40, 17, 44], outline=bp_white)
    
    draw.line([(35, 34), (46, 28)], fill=bp_white, width=1)
    draw.line([(46, 28), (53, 34)], fill=bp_white, width=1)
    draw.line([(53, 34), (54, 42)], fill=bp_white, width=1)
    draw.ellipse([53, 40, 57, 44], outline=bp_white)
    
    draw.line([(35, 34), (35, 24)], fill=bp_white, width=1)
    draw.ellipse([33, 22, 37, 26], outline=bp_white)

    draw.ellipse([25, 36, 45, 58], outline=bp_white)
    
    collar_pts = [(23, 58), (28, 66), (35, 58), (42, 66), (47, 58)]
    for i in range(len(collar_pts)-1):
        draw.line([collar_pts[i], collar_pts[i+1]], fill=bp_white)
    draw.ellipse([27, 65, 29, 67], outline=bp_white)
    draw.ellipse([41, 65, 43, 67], outline=bp_white)

    # Drafting Eyes
    draw.ellipse([28, 43, 34, 49], outline=bp_white)
    draw.line([(31, 41), (31, 51)], fill=bp_white)
    draw.line([(26, 46), (36, 46)], fill=bp_white)
    draw.point((31, 46), fill=bp_white)

    draw.ellipse([37, 40, 43, 46], outline=bp_white)
    draw.line([(40, 38), (40, 48)], fill=bp_white)
    draw.line([(35, 43), (45, 43)], fill=bp_white)
    draw.point((40, 43), fill=bp_white)

    draw.line([(35, 49), (36, 52)], fill=bp_white)

    # Dimension line & opposing arrows
    draw.line([(12, 73), (58, 73)], fill=bp_white, width=1)
    draw.line([(12, 73), (16, 71)], fill=bp_white, width=1)
    draw.line([(12, 73), (16, 75)], fill=bp_white, width=1)
    draw.line([(58, 73), (54, 71)], fill=bp_white, width=1)
    draw.line([(58, 73), (54, 75)], fill=bp_white, width=1)
    
    draw.arc([16, 18, 54, 56], start=190, end=260, fill=bp_white)
    draw.arc([16, 18, 54, 56], start=280, end=350, fill=bp_white)

    draw.ellipse([35, 38, 45, 48], outline=red_mark)
    draw.line([(48, 37), (50, 37)], fill=red_mark)
    draw.point((51, 38), fill=red_mark)
    draw.point((50, 39), fill=red_mark)
    draw.point((50, 41), fill=red_mark)

    # Vertical JOKER text in top-left and bottom-right (drafting white)
    draw_vertical_joker_text(img, bp_white, top_left=True, bottom_right=True)

    export_sprite(img, "j_wrong_schematics.png")

def build_j_magifect():
    img = create_card_base(bg_color=PALETTE["DARK_SLATE"], border_color=PALETTE["DEEP_OUTLINE"])
    draw = ImageDraw.Draw(img)
    draw.rectangle([3, 3, 67, 91], outline=PALETTE["MID_SLATE"])
    
    # Vertical JOKER text ONLY in top-left (top-to-bottom)
    draw_vertical_joker_text(img, PALETTE["CARD_WHITE"], top_left=True, bottom_right=False)

    draw.line([(8, 48), (28, 48)], fill=PALETTE["CARD_WHITE"], width=2)
    prism_pts = [(35, 30), (22, 60), (48, 60)]
    draw.polygon(prism_pts, fill=(79, 99, 103, 180), outline=PALETTE["CARD_WHITE"])
    draw.line([(35, 30), (35, 60)], fill=PALETTE["CARD_WHITE"])

    draw.line([(40, 44), (64, 32)], fill=PALETTE["FOIL_CYAN"], width=2)
    draw.point((65, 32), fill=PALETTE["CARD_WHITE"])
    draw.line([(42, 48), (64, 48)], fill=PALETTE["HOLO_MAGENTA"], width=2)
    draw.point((65, 48), fill=PALETTE["CARD_WHITE"])
    draw.line([(40, 52), (64, 64)], fill=PALETTE["GOLD_YELLOW"], width=2)
    draw.line([(41, 53), (64, 65)], fill=PALETTE["GREEN"], width=1)
    draw.point((65, 64), fill=PALETTE["CARD_WHITE"])

    sparkles = [(20, 34), (48, 28), (56, 74), (16, 68), (35, 72)]
    for sx, sy in sparkles:
        draw.point((sx, sy), fill=PALETTE["GOLD_HL"])
        draw.point((sx+1, sy), fill=PALETTE["CARD_WHITE"])
        draw.point((sx, sy+1), fill=PALETTE["CARD_WHITE"])
        
    export_sprite(img, "j_magifect.png")

def build_j_stanczyk():
    """
    Builds Legendary Joker 'Stańczyk' sprite sheet (71x190) following vanilla Legendary Joker anatomy:
    - Row 0 (0..94): Authentic Localthunk wavy marbled background mapped to black & grey,
      with the vanilla cream plaque at the bottom reading 'STANCZYK'.
    - Row 1 (95..189): Floating soul layer (transparent background) of Stańczyk:
      Scarlet jester cowl with horns, golden bells, pensive eyes, red jester robe with gold trim.
    """
    sheet = Image.new("RGBA", (71, 190), (0, 0, 0, 0))
    
    # --- ROW 0: CARD BASE (0, 0) ---
    base_template_path = os.path.join(BASE_DIR, "tools", "legendary_base_black_grey.png")
    if os.path.exists(base_template_path):
        base_img = Image.open(base_template_path).copy()
    else:
        # Fallback if template is not found
        base_img = create_card_base(bg_color=PALETTE["VOID_BLACK"], border_color=PALETTE["DEEP_OUTLINE"])
        
    sheet.paste(base_img, (0, 0))
    
    # --- ROW 1: FLOATING SOUL SPRITE (0, 1) ---
    soul_img = Image.new("RGBA", (71, 95), (0, 0, 0, 0))
    draw_soul = ImageDraw.Draw(soul_img)
    
    slate = PALETTE["MID_SLATE"]
    red = PALETTE["MULT_RED"]
    red_dark = PALETTE["MULT_SHADOW"]
    gold = PALETTE["GOLD_YELLOW"]
    white = PALETTE["CARD_WHITE"]
    
    # 1. Hood Horns
    # Left horn curving outward
    draw_soul.polygon([(35, 22), (24, 14), (18, 20), (22, 28), (35, 26)], fill=red, outline=slate)
    draw_soul.ellipse([14, 18, 20, 24], fill=gold, outline=slate) # Left Bell
    # Right horn curving outward
    draw_soul.polygon([(35, 22), (46, 14), (52, 20), (48, 28), (35, 26)], fill=red, outline=slate)
    draw_soul.ellipse([50, 18, 56, 24], fill=gold, outline=slate) # Right Bell

    # 2. Main Hood & Head Silhouette
    draw_soul.ellipse([23, 16, 47, 44], fill=red_dark, outline=slate)
    draw_soul.ellipse([25, 18, 45, 42], fill=red)

    # 3. White Face
    draw_soul.ellipse([28, 24, 42, 42], fill=white, outline=slate)

    # 4. Eyes & Brows (Golden brows & dark pupils)
    draw_soul.line([(30, 30), (33, 30)], fill=gold, width=1)
    draw_soul.point((32, 31), fill=slate)
    draw_soul.point((32, 32), fill=slate)

    draw_soul.line([(37, 30), (40, 30)], fill=gold, width=1)
    draw_soul.point((38, 31), fill=slate)
    draw_soul.point((38, 32), fill=slate)

    # Nose line
    draw_soul.line([(35, 33), (35, 35)], fill=slate)

    # Red Clown Lips/Smile
    draw_soul.line([(31, 38), (34, 40)], fill=red_dark, width=1)
    draw_soul.line([(34, 40), (36, 40)], fill=red_dark, width=1)
    draw_soul.line([(36, 40), (39, 38)], fill=red_dark, width=1)
    draw_soul.point((35, 39), fill=white)

    # 5. Robe & Shoulders
    draw_soul.ellipse([18, 42, 52, 70], fill=red_dark, outline=slate)
    draw_soul.ellipse([20, 44, 50, 68], fill=red)

    # Golden trim down center
    draw_soul.line([(33, 44), (33, 68)], fill=gold, width=1)
    draw_soul.line([(37, 44), (37, 68)], fill=gold, width=1)
    draw_soul.line([(34, 46), (36, 68)], fill=white, width=1)

    # Jester collar points with golden bells
    draw_soul.polygon([(26, 42), (21, 52), (28, 48)], fill=red, outline=slate)
    draw_soul.ellipse([19, 50, 23, 54], fill=gold, outline=slate)

    draw_soul.polygon([(44, 42), (49, 52), (42, 48)], fill=red, outline=slate)
    draw_soul.ellipse([47, 50, 51, 54], fill=gold, outline=slate)

    sheet.paste(soul_img, (0, 95))
    export_sprite(sheet, "j_stanczyk.png")

def build_j_doubler():
    """
    Builds Rare Joker 'Doubler' sprite (71x95).
    Features a rich velvet purple card with an ornate embossed golden medallion
    bearing a gleaming '2X' multiplier stamp with radiant light rays.
    """
    img = create_card_base(bg_color=PALETTE["DARK_SLATE"], border_color=PALETTE["DEEP_OUTLINE"])
    draw = ImageDraw.Draw(img)
    
    # Inner gold border
    draw.rectangle([3, 3, 67, 91], outline=PALETTE["GOLD_SHADOW"])
    draw.rectangle([4, 4, 66, 90], outline=PALETTE["GOLD_YELLOW"])
    
    # JOKER text at top in Gold
    gold = PALETTE["GOLD_YELLOW"]
    gold_hl = PALETTE["GOLD_HL"]
    draw.rectangle([14, 8, 18, 9], fill=gold)
    draw.rectangle([16, 9, 18, 13], fill=gold)
    draw.rectangle([14, 12, 16, 14], fill=gold)
    draw.rectangle([21, 8, 27, 14], fill=gold)
    draw.rectangle([23, 10, 25, 12], fill=PALETTE["DARK_SLATE"])
    draw.line([(30, 8), (30, 14)], fill=gold, width=2)
    draw.line([(35, 8), (32, 11)], fill=gold, width=2)
    draw.line([(32, 11), (36, 14)], fill=gold, width=2)
    draw.rectangle([39, 8, 41, 14], fill=gold)
    draw.line([(41, 8), (45, 8)], fill=gold, width=2)
    draw.line([(41, 11), (44, 11)], fill=gold, width=1)
    draw.line([(41, 14), (45, 14)], fill=gold, width=2)
    draw.rectangle([48, 8, 50, 14], fill=gold)
    draw.rectangle([50, 8, 54, 11], fill=gold)
    draw.point((52, 9), fill=PALETTE["DARK_SLATE"])
    draw.point((51, 9), fill=PALETTE["DARK_SLATE"])
    draw.line([(51, 11), (54, 14)], fill=gold, width=2)

    # Radiant golden rays in background
    rays = [
        ((35, 52), (16, 32)), ((35, 52), (54, 32)),
        ((35, 52), (16, 72)), ((35, 52), (54, 72)),
        ((35, 52), (12, 52)), ((35, 52), (58, 52)),
        ((35, 52), (35, 28)), ((35, 52), (35, 76))
    ]
    for p1, p2 in rays:
        draw.line([p1, p2], fill=PALETTE["GOLD_SHADOW"], width=1)

    # Large Golden Medallion
    draw.ellipse([17, 34, 53, 70], fill=PALETTE["DEEP_OUTLINE"])
    draw.ellipse([18, 35, 52, 69], fill=PALETTE["GOLD_SHADOW"])
    draw.ellipse([20, 37, 50, 67], fill=PALETTE["GOLD_YELLOW"])
    draw.ellipse([22, 39, 48, 65], fill=PALETTE["GOLD_HL"])
    draw.ellipse([24, 41, 46, 63], fill=PALETTE["GOLD_YELLOW"])

    # Bold Chunky "2X" Emblem in center
    # "2" (x=26..33, y=45..59)
    slate = PALETTE["DEEP_OUTLINE"]
    draw.line([(27, 46), (32, 46)], fill=slate, width=2)
    draw.line([(32, 46), (32, 50)], fill=slate, width=2)
    draw.line([(32, 50), (27, 56)], fill=slate, width=2)
    draw.line([(26, 56), (33, 56)], fill=slate, width=2)
    # White highlight on "2"
    draw.line([(28, 47), (31, 47)], fill=PALETTE["CARD_WHITE"])
    draw.line([(27, 57), (32, 57)], fill=PALETTE["CARD_WHITE"])

    # "X" (x=37..44, y=47..57)
    draw.line([(37, 48), (43, 56)], fill=slate, width=2)
    draw.line([(43, 48), (37, 56)], fill=slate, width=2)
    # White highlight on "X"
    draw.line([(38, 48), (43, 55)], fill=PALETTE["CARD_WHITE"])

    # Sparkles around medallion
    sparkles = [(14, 26), (56, 26), (14, 78), (56, 78), (35, 24), (35, 80)]
    for sx, sy in sparkles:
        draw.point((sx, sy), fill=PALETTE["CARD_WHITE"])
        draw.point((sx+1, sy), fill=gold_hl)
        draw.point((sx-1, sy), fill=gold_hl)
        draw.point((sx, sy+1), fill=gold_hl)
        draw.point((sx, sy-1), fill=gold_hl)

    export_sprite(img, "j_doubler.png")

def build_b_echo():
    """
    Builds 'Echo Deck' card back sprite (71x95).
    Theme: Double trigger / Echo / Soundwave resonance.
    Geometric deck back featuring concentric ripple rings and repeating diamond pulses.
    """
    img = create_card_base(bg_color=(24, 38, 48, 255), border_color=PALETTE["DEEP_OUTLINE"])
    draw = ImageDraw.Draw(img)
    
    cyan = PALETTE["PLANET_CYAN"]
    gold = PALETTE["GOLD_YELLOW"]
    gold_hl = PALETTE["GOLD_HL"]
    navy = (15, 25, 32, 255)
    cream = PALETTE["CARD_CREAM"]
    
    # 1. Repeating geometric diamond lattice background
    for y in range(6, 90, 8):
        for x in range(6, 66, 8):
            draw.point((x, y), fill=(40, 60, 75, 255))
            draw.point((x+4, y+4), fill=(30, 48, 60, 255))
            
    # 2. Outer and Inner frame lines
    draw.rectangle([4, 4, 66, 90], outline=(45, 75, 95, 255))
    draw.rectangle([6, 6, 64, 88], outline=cyan)
    draw.rectangle([8, 8, 62, 86], outline=gold)
    
    # 3. Corner flourish accents (small gold diamonds)
    for cx, cy in [(10, 10), (60, 10), (10, 84), (60, 84)]:
        draw.polygon([(cx, cy-2), (cx+2, cy), (cx, cy+2), (cx-2, cy)], fill=gold_hl)

    # 4. Concentric Dual Echo Wave Rings in center (radiating pulses)
    draw.ellipse([14, 26, 56, 68], outline=(45, 80, 100, 255), width=2)
    draw.ellipse([18, 30, 52, 64], outline=cyan, width=2)
    draw.ellipse([23, 35, 47, 59], outline=gold, width=2)
    
    # 5. Central Twin Pulse Symbol (Overlapping diamonds representing dual triggers)
    draw.polygon([(30, 47), (35, 41), (40, 47), (35, 53)], outline=cyan, fill=navy)
    draw.polygon([(33, 47), (38, 41), (43, 47), (38, 53)], outline=gold, fill=(35, 45, 30, 160))
    draw.point((35, 47), fill=cream)
    draw.point((36, 47), fill=gold_hl)
    draw.point((37, 47), fill=cyan)
    
    # 6. Resonance tick marks
    for ty in [16, 20, 74, 78]:
        draw.line([(33, ty), (37, ty)], fill=cyan)
    for tx in [13, 17, 53, 57]:
        draw.line([(tx, 45), (tx, 49)], fill=cyan)

    export_sprite(img, "b_echo.png")

def build_j_burnt_offering():
    """
    Builds Rare Joker 'Burnt Offering' sprite (71x95).
    Features an ornate ceremonial sacrificial brazier with mystic Tarot purple flames
    consuming a playing card, while a glowing purple/gold Tarot card rises from the ashes.
    """
    img = create_card_base(bg_color=PALETTE["CARD_CREAM"], border_color=PALETTE["DEEP_OUTLINE"])
    draw = ImageDraw.Draw(img)
    
    # Inner border line
    draw.rectangle([3, 3, 67, 91], outline=PALETTE["PAPER_SHADOW"])
    
    # Vertical JOKER text in top-left and bottom-right
    draw_vertical_joker_text(img, PALETTE["DARK_SLATE"], top_left=True, bottom_right=True)

    # 1. Antique ceremonial bronze/stone brazier bowl at bottom (y=62..78)
    bronze = (165, 133, 71, 255)
    dark_bronze = (107, 78, 40, 255)
    
    # Brazier pedestal stand
    draw.rectangle([31, 72, 39, 78], fill=dark_bronze)
    draw.line([(25, 78), (45, 78)], fill=dark_bronze, width=2)
    draw.line([(27, 77), (43, 77)], fill=bronze)
    
    # Brazier bowl
    draw.ellipse([18, 58, 52, 72], fill=dark_bronze)
    draw.ellipse([19, 59, 51, 71], fill=bronze)
    draw.ellipse([21, 60, 49, 68], fill=(55, 35, 20, 255))
    
    # Glowing embers
    for ex, ey in [(25, 64), (35, 63), (45, 64), (30, 65), (40, 65)]:
        draw.point((ex, ey), fill=PALETTE["MULT_RED"])
        draw.point((ex+1, ey), fill=PALETTE["GOLD_HL"])

    # 2. Playing card burning in the brazier
    card_pts = [(28, 42), (42, 38), (45, 62), (31, 66)]
    draw.polygon(card_pts, fill=PALETTE["CARD_WHITE"], outline=PALETTE["DEEP_OUTLINE"])
    draw.point((35, 48), fill=PALETTE["MULT_RED"])
    draw.point((36, 48), fill=PALETTE["MULT_RED"])
    draw.point((35, 49), fill=PALETTE["MULT_RED"])
    for cy in range(60, 67):
        for cx in range(30, 46):
            if (cx + cy) % 2 == 0 and cy > 61:
                draw.point((cx, cy), fill=(40, 40, 40, 255))
            elif cy > 64:
                draw.point((cx, cy), fill=PALETTE["DEEP_OUTLINE"])

    # 3. Mystical Tarot Purple flames licking up the card
    purple = PALETTE["TAROT_PURPLE"]
    flame_pts = [
        [(24, 60), (26, 48), (28, 54), (25, 62)],
        [(32, 60), (35, 34), (38, 42), (36, 62)],
        [(42, 60), (46, 46), (44, 54), (43, 62)]
    ]
    for fp in flame_pts:
        draw.polygon(fp, fill=purple)
    draw.polygon([(33, 58), (35, 44), (37, 58)], fill=PALETTE["GOLD_HL"])
    draw.polygon([(34, 56), (35, 48), (36, 56)], fill=PALETTE["CARD_WHITE"])

    # 4. Miniature glowing Tarot card hovering in rising smoke (x=27..43, y=18..33)
    tarot_purple = PALETTE["TAROT_PURPLE"]
    tarot_gold = PALETTE["GOLD_YELLOW"]
    draw.rectangle([27, 18, 43, 33], fill=tarot_purple, outline=PALETTE["DEEP_OUTLINE"])
    draw.rectangle([28, 19, 42, 32], outline=tarot_gold)
    draw.ellipse([32, 23, 38, 28], outline=PALETTE["CARD_WHITE"])
    draw.point((35, 25), fill=tarot_gold)
    draw.point((35, 26), fill=PALETTE["DEEP_OUTLINE"])
    draw.line([(34, 20), (36, 20)], fill=tarot_gold)

    # 5. Rising smoke curls & floating golden sparks
    smoke_pts = [(24, 36), (22, 28), (24, 20), (46, 38), (48, 30), (46, 22)]
    for sx, sy in smoke_pts:
        draw.point((sx, sy), fill=PALETTE["PAPER_SHADOW"])
    sparks = [(20, 48), (50, 46), (22, 32), (48, 26), (35, 14)]
    for px, py in sparks:
        draw.point((px, py), fill=PALETTE["GOLD_HL"])

    export_sprite(img, "j_burnt_offering.png")

def build_j_jackpot():
    """Builds Jackpot Joker (71x95 px, 142x190 2x) - Vintage mechanical slot machine with triple lucky 7s."""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    C_OUTLINE = PALETTE["DEEP_OUTLINE"]
    C_CAB_BODY = (42, 60, 72, 255)
    C_CAB_DARK = (28, 40, 48, 255)
    C_CAB_LIGHT = (65, 90, 108, 255)
    C_GOLD = PALETTE["GOLD_YELLOW"]
    C_GOLD_HL = PALETTE["GOLD_HL"]
    C_GOLD_SHADOW = PALETTE["GOLD_SHADOW"]
    C_RED = PALETTE["MULT_RED"]
    C_RED_DARK = PALETTE["MULT_SHADOW"]
    C_WHITE = PALETTE["CARD_WHITE"]
    C_REEL_BG = (248, 246, 240, 255)
    C_SHADOW = (210, 218, 215, 255)

    # 1. Cast shadow under the machine
    draw.ellipse([14, 75, 56, 83], fill=C_SHADOW)

    # 2. Main Cabinet Box: x in [16, 54], y in [24, 76]
    draw.rectangle([16, 24, 54, 76], fill=C_CAB_BODY, outline=C_OUTLINE)
    draw.line([(17, 25), (53, 25)], fill=C_CAB_LIGHT)
    draw.line([(17, 25), (17, 75)], fill=C_CAB_LIGHT)
    draw.line([(53, 26), (53, 75)], fill=C_CAB_DARK)
    draw.line([(17, 75), (53, 75)], fill=C_CAB_DARK)

    # 3. Top Marquee Dome: x in [18, 52], y in [13, 24]
    draw.polygon([(18, 24), (21, 16), (28, 13), (42, 13), (49, 16), (52, 24)], fill=C_GOLD, outline=C_OUTLINE)
    draw.polygon([(20, 23), (22, 17), (29, 14), (41, 14), (48, 17), (50, 23)], fill=C_GOLD_HL)
    draw.rectangle([23, 16, 47, 22], fill=C_CAB_DARK, outline=C_OUTLINE)

    # Pixel "7 7 7" marquee header
    def draw_mini_7(x, y, col):
        draw.line([(x, y), (x + 3, y)], fill=col)
        draw.point((x + 3, y + 1), fill=col)
        draw.point((x + 2, y + 2), fill=col)
        draw.point((x + 1, y + 3), fill=col)
        draw.point((x + 1, y + 4), fill=col)

    draw_mini_7(26, 17, C_RED)
    draw_mini_7(33, 17, C_RED)
    draw_mini_7(40, 17, C_RED)

    # Flashing lights around the arched marquee
    marquee_bulbs = [(20, 20), (24, 15), (30, 13), (35, 13), (40, 13), (46, 15), (50, 20)]
    for i, (bx, by) in enumerate(marquee_bulbs):
        col = C_RED if i % 2 == 0 else C_GOLD_HL
        draw.point((bx, by), fill=col)

    # 4. Reel Display Window (Recessed Frame)
    draw.rectangle([18, 27, 52, 53], fill=C_OUTLINE)
    draw.rectangle([19, 28, 51, 52], fill=C_CAB_DARK)

    # Payline side pointer arrows
    draw.polygon([(17, 41), (19, 39), (19, 43)], fill=C_RED)
    draw.polygon([(53, 41), (51, 39), (51, 43)], fill=C_RED)

    # 3 Reels
    for rx in [20, 31, 42]:
        draw.rectangle([rx, 30, rx + 8, 50], fill=C_REEL_BG)
        draw.line([(rx, 30), (rx + 8, 30)], fill=(195, 195, 195, 255))
        draw.line([(rx, 31), (rx + 8, 31)], fill=(220, 220, 220, 255))
        draw.line([(rx, 49), (rx + 8, 49)], fill=(220, 220, 220, 255))
        draw.line([(rx, 50), (rx + 8, 50)], fill=(195, 195, 195, 255))

        # Bold Red "7" on each reel
        draw.rectangle([rx + 1, 35, rx + 7, 36], fill=C_RED)
        draw.point((rx + 1, 37), fill=C_RED)
        draw.line([(rx + 6, 36), (rx + 6, 38)], fill=C_RED)
        draw.line([(rx + 5, 38), (rx + 5, 40)], fill=C_RED)
        draw.line([(rx + 4, 40), (rx + 4, 43)], fill=C_RED)
        draw.line([(rx + 3, 43), (rx + 3, 46)], fill=C_RED)
        # Drop shadow / 3D bevel on 7
        draw.line([(rx + 7, 36), (rx + 7, 37)], fill=C_RED_DARK)
        draw.point((rx + 6, 39), fill=C_RED_DARK)
        draw.point((rx + 5, 41), fill=C_RED_DARK)
        draw.point((rx + 4, 44), fill=C_RED_DARK)
        draw.point((rx + 4, 46), fill=C_RED_DARK)
        draw.point((rx + 2, 35), fill=C_WHITE)

    # Reel separator bars in gold
    draw.line([(29, 28), (29, 52)], fill=C_GOLD)
    draw.line([(30, 28), (30, 52)], fill=C_GOLD_SHADOW)
    draw.line([(40, 28), (40, 52)], fill=C_GOLD)
    draw.line([(41, 28), (41, 52)], fill=C_GOLD_SHADOW)

    # 5. Machine Front Details (Below Reels)
    draw.rectangle([18, 54, 52, 56], fill=C_GOLD, outline=C_OUTLINE)
    draw.line([(19, 55), (51, 55)], fill=C_GOLD_HL)

    # 6. Coin Hopper / Payout Tray at Bottom
    draw.rectangle([18, 58, 52, 73], fill=C_OUTLINE)
    draw.rectangle([19, 59, 51, 72], fill=C_CAB_DARK)
    draw.rectangle([21, 62, 49, 70], fill=(16, 22, 28, 255))

    # Gold Coins tumbling and overflowing
    coins = [
        (24, 65, C_GOLD), (27, 64, C_GOLD_HL), (30, 66, C_GOLD),
        (33, 63, C_GOLD_HL), (36, 65, C_GOLD), (39, 64, C_GOLD_HL),
        (42, 66, C_GOLD), (45, 64, C_GOLD_HL), (48, 66, C_GOLD),
        (26, 68, C_GOLD_HL), (29, 69, C_GOLD), (33, 67, C_GOLD_HL),
        (37, 69, C_GOLD), (41, 68, C_GOLD_HL), (44, 70, C_GOLD),
        (28, 72, C_GOLD_HL), (32, 73, C_GOLD), (35, 74, C_GOLD_HL),
        (39, 73, C_GOLD), (42, 72, C_GOLD_HL), (30, 75, C_GOLD),
        (36, 76, C_GOLD_HL), (46, 72, C_GOLD), (24, 73, C_GOLD_HL)
    ]
    for cx, cy, col in coins:
        draw.ellipse([cx - 2, cy - 1, cx + 2, cy + 1], fill=col, outline=C_OUTLINE)
        draw.point((cx, cy - 1), fill=C_WHITE if col == C_GOLD_HL else C_GOLD_HL)

    # 7. Pull Lever (One-Armed Bandit)
    draw.rectangle([54, 37, 56, 40], fill=C_OUTLINE)
    draw.rectangle([55, 38, 56, 39], fill=C_GOLD)
    draw.line([(56, 38), (60, 31)], fill=C_OUTLINE, width=2)
    draw.line([(56, 38), (60, 31)], fill=(185, 195, 200, 255), width=1)
    draw.ellipse([59, 26, 63, 30], fill=C_RED, outline=C_OUTLINE)
    draw.point((60, 27), fill=C_WHITE)
    draw.point((62, 29), fill=C_RED_DARK)

    # 8. Golden Sparkles around the machine
    sparkles = [(13, 27), (56, 17), (12, 56), (58, 52), (35, 8)]
    for sx, sy in sparkles:
        draw.line([(sx - 2, sy), (sx + 2, sy)], fill=C_GOLD_HL)
        draw.line([(sx, sy - 2), (sx, sy + 2)], fill=C_GOLD_HL)
        draw.point((sx, sy), fill=C_WHITE)

    # 9. Authentic Vertical JOKER Lettering (top-left & bottom-right)
    draw_vertical_joker_text(img, PALETTE["DARK_SLATE"], top_left=True, bottom_right=True)

    export_sprite(img, "j_jackpot.png")

def build_j_the_bell():
    """Builds The Bell Joker (71x95 px, 142x190 2x) - Golden resonant cathedral bell with Gaussian wave arcs."""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    C_OUTLINE = PALETTE["DEEP_OUTLINE"]
    C_CREAM = PALETTE["CARD_CREAM"]
    C_WHITE = PALETTE["CARD_WHITE"]
    C_GOLD = PALETTE["GOLD_YELLOW"]
    C_GOLD_HL = PALETTE["GOLD_HL"]
    C_GOLD_SHADOW = PALETTE["GOLD_SHADOW"]
    C_BRONZE = (150, 95, 35, 255)
    C_WOOD = (105, 58, 30, 255)
    C_WOOD_DARK = (65, 34, 18, 255)
    C_IRON = (60, 70, 75, 255)
    C_CYAN = PALETTE["PLANET_CYAN"]

    # 1. Wooden Crossbeam / Headstock at top: x in [22, 48], y in [17, 24]
    draw.rectangle([22, 17, 48, 23], fill=C_WOOD, outline=C_OUTLINE)
    draw.line([(23, 18), (47, 18)], fill=(145, 85, 45, 255))
    draw.line([(23, 22), (47, 22)], fill=C_WOOD_DARK)
    draw.point((25, 20), fill=C_IRON)
    draw.point((45, 20), fill=C_IRON)

    # 2. Bell Crown / Suspension Loop
    draw.rectangle([31, 23, 39, 29], fill=C_IRON, outline=C_OUTLINE)
    draw.rectangle([33, 25, 37, 27], fill=(100, 115, 120, 255))

    # 3. Bell Main Body
    bell_poly = [
        (30, 29), (40, 29),
        (43, 35), (44, 44),
        (50, 55), (52, 62),
        (18, 62), (20, 55),
        (26, 44), (27, 35)
    ]
    draw.polygon(bell_poly, fill=C_GOLD, outline=C_OUTLINE)

    # 3D Shading & Specular Highlights
    draw.line([(31, 31), (28, 44)], fill=C_GOLD_HL, width=2)
    draw.line([(28, 44), (21, 60)], fill=C_GOLD_HL, width=2)
    draw.line([(31, 33), (23, 58)], fill=C_WHITE, width=1)

    draw.line([(39, 31), (43, 44)], fill=C_GOLD_SHADOW, width=2)
    draw.line([(43, 44), (50, 60)], fill=C_GOLD_SHADOW, width=2)
    draw.line([(40, 33), (48, 58)], fill=C_BRONZE, width=1)

    # Engraved sound rings
    draw.line([(28, 41), (42, 41)], fill=C_OUTLINE)
    draw.line([(28, 42), (42, 42)], fill=C_GOLD_HL)
    draw.line([(23, 52), (47, 52)], fill=C_OUTLINE)
    draw.line([(23, 53), (47, 53)], fill=C_GOLD_HL)

    # 4. Flared Sounding Rim & Hollow Interior at Bottom
    draw.ellipse([17, 60, 53, 68], fill=C_OUTLINE)
    draw.arc([17, 60, 53, 68], start=0, end=180, fill=C_GOLD_HL, width=2)
    draw.ellipse([19, 61, 51, 66], fill=(20, 24, 28, 255))

    # 5. Bronze Clapper
    draw.line([(35, 58), (37, 69)], fill=C_IRON, width=2)
    draw.ellipse([34, 66, 40, 72], fill=C_GOLD, outline=C_OUTLINE)
    draw.point((36, 68), fill=C_WHITE)
    draw.point((38, 70), fill=C_GOLD_SHADOW)

    # 6. Gaussian / Bell-Curve Acoustic Soundwaves
    draw.arc([12, 42, 22, 64], start=110, end=250, fill=C_CYAN, width=1)
    draw.arc([48, 42, 58, 64], start=290, end=70, fill=C_CYAN, width=1)
    draw.arc([8, 34, 20, 72], start=120, end=240, fill=(19, 175, 206, 180), width=1)
    draw.arc([50, 34, 62, 72], start=300, end=60, fill=(19, 175, 206, 180), width=1)

    # Ringing Acoustic Sparkles
    sparkles = [(13, 30), (57, 28), (11, 68), (59, 66), (35, 11), (25, 76), (45, 76)]
    for sx, sy in sparkles:
        draw.line([(sx - 1, sy), (sx + 1, sy)], fill=C_GOLD_HL)
        draw.line([(sx, sy - 1), (sx, sy + 1)], fill=C_GOLD_HL)
        draw.point((sx, sy), fill=C_WHITE)

    # 7. Vertical JOKER Lettering
    draw_vertical_joker_text(img, PALETTE["DARK_SLATE"], top_left=True, bottom_right=True)

    export_sprite(img, "j_the_bell.png")

def build_sleeve_echo():
    """Builds Echo Sleeve (73x95 px, 146x190 2x) for CardSleeves compatibility."""
    sleeve = Image.new("RGBA", (73, 95), (0, 0, 0, 0))
    draw = ImageDraw.Draw(sleeve)

    C_MIDNIGHT = (24, 38, 48, 255)
    C_CYAN = (19, 175, 206, 255)
    C_CYAN_DIM = (12, 100, 120, 255)
    C_GOLD = (243, 185, 88, 255)
    C_GOLD_HL = (255, 224, 130, 255)
    C_NOTCH_BACK = (18, 28, 36, 255)

    cardsleeves_path = os.path.expandvars(r"%APPDATA%\Balatro\Mods\CardSleeves-1.9.4\assets\1x\sleeves.png")
    if os.path.exists(cardsleeves_path):
        cs_img = Image.open(cardsleeves_path)
        red = cs_img.crop((0, 0, 73, 95))
        blue = cs_img.crop((73, 0, 146, 95))
        yellow = cs_img.crop((146, 0, 219, 95))

        for y in range(95):
            for x in range(73):
                if red.getpixel((x, y))[3] > 0:
                    if y < 31:
                        sleeve.putpixel((x, y), C_NOTCH_BACK)
                    else:
                        sleeve.putpixel((x, y), C_MIDNIGHT)

        cx, cy = 36, 58
        for r in range(26, 28):
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=C_CYAN_DIM)
        for r in range(20, 22):
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=C_CYAN)
        for r in range(14, 16):
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=C_GOLD)
        for r in range(8, 10):
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=C_GOLD_HL)

        draw.polygon([(cx, cy - 4), (cx + 4, cy), (cx, cy + 4), (cx - 4, cy)], fill=C_CYAN)
        draw.point((cx, cy), fill=C_GOLD_HL)

        wave_heights = [2, 4, 7, 10, 6, 3]
        for i, h in enumerate(wave_heights):
            lx = cx - 12 - i * 3
            draw.line([(lx, cy - h), (lx, cy + h)], fill=C_CYAN, width=1)
            rx = cx + 12 + i * 3
            draw.line([(rx, cy - h), (rx, cy + h)], fill=C_CYAN, width=1)

        for y in range(95):
            for x in range(73):
                pr = red.getpixel((x, y))
                pb = blue.getpixel((x, y))
                py_col = yellow.getpixel((x, y))
                if pr[3] > 0 and pr == pb == py_col:
                    sleeve.putpixel((x, y), pr)
                elif pr[3] == 0:
                    sleeve.putpixel((x, y), (0, 0, 0, 0))

        for x in range(73):
            pr = red.getpixel((x, 31))
            if pr[:3] in [(90, 90, 90), (75, 75, 75), (104, 104, 104), (45, 45, 45)]:
                sleeve.putpixel((x, 31), pr)
    else:
        # Fallback if CardSleeves asset is not found
        draw.rectangle([1, 25, 71, 93], fill=C_MIDNIGHT, outline=(90, 90, 90, 255))

    export_sprite(sleeve, "sleeve_echo.png")

# =============================================================================
# ENHANCEMENT CARD BACKGROUNDS (FOR ENHANCEMENT RETRIGGER JOKERS)
# =============================================================================

def load_enhancement_base(name: str) -> Image.Image:
    """Loads an authentic in-game Balatro enhancement card background from tools/enhancement_bases/1x."""
    path = os.path.join(BASE_DIR, "tools", "enhancement_bases", "1x", f"{name}.png")
    if os.path.exists(path):
        return Image.open(path).convert("RGBA")
    return create_card_base()

# =============================================================================
# JOKER BUILDERS
# =============================================================================

def build_j_lucky_clover():
    """Builds Lucky Clover Joker (71x95 px, 142x190 2x) on authentic Lucky Card background."""
    img = load_enhancement_base("lucky")
    draw = ImageDraw.Draw(img)

    C_OUTLINE = PALETTE["DEEP_OUTLINE"]
    C_GREEN = (75, 194, 146, 255)
    C_GREEN_DARK = (36, 122, 85, 255)
    C_GREEN_HL = (140, 235, 190, 255)
    C_GOLD = PALETTE["GOLD_YELLOW"]
    C_GOLD_HL = PALETTE["GOLD_HL"]
    C_WHITE = PALETTE["CARD_WHITE"]

    # Curving stem (y=54..82, x=28..46)
    draw.arc([28, 54, 46, 82], start=50, end=190, fill=C_GREEN_DARK, width=3)
    draw.arc([29, 55, 45, 81], start=50, end=190, fill=C_GREEN, width=1)

    # 4 Heart-shaped leaves centered at (35, 42)
    cx, cy = 35, 42
    leaf_offsets = [
        (0, -11),  # Top
        (11, 0),   # Right
        (0, 11),   # Bottom
        (-11, 0),  # Left
    ]

    for ox, oy in leaf_offsets:
        lx, ly = cx + ox, cy + oy
        draw.ellipse([lx - 9, ly - 9, lx + 9, ly + 9], fill=C_GREEN_DARK, outline=C_OUTLINE)
        draw.ellipse([lx - 8, ly - 8, lx + 8, ly + 8], fill=C_GREEN)
        draw.arc([lx - 7, ly - 7, lx + 7, ly + 7], start=180, end=330, fill=C_GREEN_HL, width=1)

    # Heart indent notches between lobes
    draw.polygon([(cx - 2, cy - 2), (cx + 2, cy - 2), (cx, cy + 2)], fill=C_GREEN_DARK)

    # Golden central knot & vein star
    draw.line([(cx, cy - 10), (cx, cy + 10)], fill=C_GOLD, width=1)
    draw.line([(cx - 10, cy), (cx + 10, cy)], fill=C_GOLD, width=1)
    draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=C_GOLD, outline=C_OUTLINE)
    draw.point((cx - 1, cy - 1), fill=C_GOLD_HL)
    draw.point((cx, cy), fill=C_WHITE)

    # Floating lucky sparkles
    sparkles = [(18, 24), (52, 22), (20, 64), (53, 62)]
    for sx, sy in sparkles:
        draw.point((sx, sy), fill=C_GOLD_HL)
        draw.point((sx + 1, sy), fill=C_GOLD)
        draw.point((sx - 1, sy), fill=C_GOLD)
        draw.point((sx, sy + 1), fill=C_GOLD)
        draw.point((sx, sy - 1), fill=C_GOLD)
        draw.point((sx, sy), fill=C_WHITE)

    draw_vertical_joker_text(img, PALETTE["DARK_SLATE"], top_left=True, bottom_right=True)
    export_sprite(img, "j_lucky_clover.png")

def build_j_multifaces():
    """Builds MultiFaces Joker (71x95 px, 142x190 2x) - Full-card dual composition (Sock & Buskin style + cubist flowing face profiles)."""
    img = Image.new("RGBA", (71, 95), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    C_OUTLINE = PALETTE["DEEP_OUTLINE"]
    C_TEAL_DEEP = (24, 66, 80, 255)
    C_TEAL_MID = (38, 108, 126, 255)
    C_TEAL_BRIGHT = (68, 162, 184, 255)
    C_OCHRE = (226, 162, 70, 255)
    C_OCHRE_LIGHT = (246, 208, 132, 255)
    C_IVORY = (248, 238, 218, 255)
    C_TERRACOTTA = (220, 92, 68, 255)
    C_RUBY_LIPS = (196, 42, 42, 255)
    C_WHITE = PALETTE["CARD_WHITE"]

    # 1. Base card blank
    draw.rectangle([1, 1, 69, 93], fill=C_IVORY)
    draw.line([(3, 0), (67, 0)], fill=C_OUTLINE)
    draw.line([(3, 94), (67, 94)], fill=C_OUTLINE)
    draw.line([(0, 3), (0, 91)], fill=C_OUTLINE)
    draw.line([(70, 3), (70, 91)], fill=C_OUTLINE)
    for pt in [(1, 2), (2, 1), (69, 2), (68, 1), (1, 92), (2, 93), (69, 92), (68, 93)]:
        draw.point(pt, fill=C_OUTLINE)

    # 2. Flowing S-split boundary across the whole card
    for y in range(1, 94):
        if y < 20:
            split_x = int(34 + (y / 20.0) * 4)
        elif y < 50:
            split_x = int(38 - ((y - 20) / 30.0) * 8)
        elif y < 75:
            split_x = int(30 + ((y - 50) / 25.0) * 12)
        else:
            split_x = int(42 - ((y - 75) / 19.0) * 6)
        draw.line([(split_x, y), (69, y)], fill=C_TEAL_DEEP)

    # 3. Flowing color ribbons and locks across the whole canvas
    # Top sweeping locks
    draw.polygon([(14, 1), (34, 1), (28, 18), (14, 22)], fill=C_TEAL_MID)
    draw.polygon([(14, 1), (26, 1), (22, 14), (14, 16)], fill=C_TEAL_BRIGHT)

    # Left face profile color fields (Ochre, Wheat, Terracotta)
    draw.polygon([(14, 22), (28, 18), (32, 34), (20, 42), (14, 38)], fill=C_OCHRE)
    draw.polygon([(14, 38), (20, 42), (24, 52), (18, 56), (14, 52)], fill=C_OCHRE_LIGHT)
    draw.polygon([(14, 52), (18, 56), (22, 68), (14, 68)], fill=C_TERRACOTTA)
    draw.polygon([(14, 68), (24, 68), (30, 84), (14, 88)], fill=C_OCHRE)

    # Central Ivory Nose / Profile Bridge
    nose_pts = [(34, 1), (38, 18), (34, 36), (36, 46), (30, 56), (28, 64), (32, 74), (34, 93),
                (30, 93), (26, 72), (24, 60), (30, 46), (28, 36), (30, 18), (28, 1)]
    draw.polygon(nose_pts, fill=C_IVORY)

    # Right face flowing patches
    draw.polygon([(46, 14), (56, 14), (58, 30), (46, 32)], fill=C_OCHRE)
    draw.polygon([(48, 44), (58, 46), (54, 64), (44, 62)], fill=C_OCHRE_LIGHT)
    draw.polygon([(56, 24), (66, 24), (64, 48), (56, 46)], fill=C_TERRACOTTA)
    draw.polygon([(42, 66), (54, 66), (56, 82), (40, 80)], fill=C_TERRACOTTA)
    draw.polygon([(46, 80), (62, 80), (58, 93), (42, 93)], fill=C_TEAL_BRIGHT)

    # 4. Fluid Black Contour Lines (Cubist / Matisse art style)
    draw.line([(34, 1), (38, 18), (34, 36), (36, 46), (30, 56), (32, 74), (34, 93)], fill=C_OUTLINE, width=2)
    draw.line([(28, 18), (32, 34), (20, 42), (24, 52), (22, 68), (30, 84)], fill=C_OUTLINE, width=2)
    draw.line([(42, 18), (48, 32), (44, 46), (46, 60), (42, 72)], fill=C_OUTLINE, width=2)
    draw.line([(52, 1), (56, 24), (54, 52), (58, 76), (54, 93)], fill=C_OUTLINE, width=2)

    # 5. Stylized Facial Features:
    # Left Almond Eye
    draw.arc([18, 27, 28, 35], start=180, end=360, fill=C_OUTLINE, width=2)
    draw.arc([18, 27, 28, 35], start=0, end=180, fill=C_OUTLINE, width=1)
    draw.ellipse([21, 29, 25, 33], fill=C_TEAL_DEEP)
    draw.point((22, 30), fill=C_WHITE)

    # Left Lips
    draw.polygon([(16, 49), (19, 47), (22, 49), (19, 51)], fill=C_RUBY_LIPS, outline=C_OUTLINE)

    # Right Expressive Eye
    draw.arc([45, 27, 55, 35], start=180, end=360, fill=C_OUTLINE, width=2)
    draw.arc([45, 27, 55, 35], start=0, end=180, fill=C_OUTLINE, width=1)
    draw.ellipse([48, 29, 52, 33], fill=C_IVORY)
    draw.ellipse([49, 30, 51, 32], fill=C_OUTLINE)
    draw.point((49, 30), fill=C_WHITE)

    # Right Sensual Lips
    draw.polygon([(42, 54), (46, 52), (50, 54), (46, 57)], fill=C_RUBY_LIPS, outline=C_OUTLINE)
    draw.line([(42, 54), (50, 54)], fill=C_OUTLINE, width=1)

    # Lower face resting lips
    draw.polygon([(24, 75), (27, 74), (29, 76), (26, 77)], fill=C_TERRACOTTA, outline=C_OUTLINE)

    # Decorative background rhythm curves
    draw.arc([10, 10, 36, 40], start=110, end=240, fill=C_OUTLINE, width=1)
    draw.arc([40, 50, 66, 80], start=20, end=160, fill=C_OUTLINE, width=1)

    # 6. Sock and Buskin dual text: Dark slate on light (top-left), White on dark teal (bottom-right)
    draw_vertical_joker_text(img, PALETTE["DARK_SLATE"], top_left=True, bottom_right=False)
    draw_vertical_joker_text(img, PALETTE["CARD_WHITE"], top_left=False, bottom_right=True)

    export_sprite(img, "j_multifaces.png")

def build_j_bonus_stage():
    """Builds Bonus Stage Joker (71x95 px, 142x190 2x) on authentic Bonus Card background.
    Features a classic retro arcade cabinet:
    - Illuminated top marquee sign reading 'BONUS'
    - CRT monitor screen with scanlines and glowing 8-bit retro golden star
    - Slanted arcade control panel with red ball-top joystick and colored push-buttons
    - Dual coin-op door with glowing coin insert slots
    - Vertical JOKER typography along margins
    """
    img = load_enhancement_base("bonus")

    # Clear blue arrow columns in JOKER text margin areas
    for y in range(0, 52):
        for x in range(0, 16):
            r, g, b, a = img.getpixel((x, y))
            if b > 180 and r < 120:
                img.putpixel((x, y), (255, 255, 255, 255))
    for y in range(43, 95):
        for x in range(55, 71):
            r, g, b, a = img.getpixel((x, y))
            if b > 180 and r < 120:
                img.putpixel((x, y), (255, 255, 255, 255))

    draw = ImageDraw.Draw(img)

    C_OUTLINE = (26, 34, 36, 255)
    C_CABINET = (47, 62, 70, 255)       # Slate body
    C_CABINET_SH = (35, 45, 50, 255)
    C_CABINET_HL = (85, 110, 120, 255)
    C_GOLD = (243, 185, 88, 255)
    C_WHITE = (255, 255, 255, 255)
    C_CYAN = (0, 195, 255, 255)
    C_RED = (254, 95, 85, 255)

    # 1. Main Cabinet Silhouette (y=14..80, x=16..54)
    draw.polygon([(19, 14), (51, 14), (54, 18), (54, 78), (51, 80), (19, 80), (16, 78), (16, 18)], fill=C_CABINET, outline=C_OUTLINE)
    draw.line([(19, 15), (51, 15)], fill=C_CABINET_HL)
    draw.line([(17, 18), (17, 78)], fill=C_CABINET_HL)
    draw.line([(53, 18), (53, 78)], fill=C_CABINET_SH)

    # 2. Illuminated Marquee Banner at Top (y=16..25, x=19..51)
    draw.rectangle([19, 16, 51, 25], fill=C_GOLD, outline=C_OUTLINE)
    draw.rectangle([20, 17, 50, 24], fill=(255, 235, 160, 255))
    # Marquee Lettering: 'BONUS' in crisp 3x5 pixel font
    for py, row in enumerate(['###', '# #', '## ', '# #', '###']):
        for px, ch in enumerate(row):
            if ch == '#': img.putpixel((23 + px, 18 + py), C_RED)
    for py, row in enumerate(['###', '# #', '# #', '# #', '###']):
        for px, ch in enumerate(row):
            if ch == '#': img.putpixel((28 + px, 18 + py), C_RED)
    for py, row in enumerate(['# #', '## ', '# #', '# #', '# #']):
        for px, ch in enumerate(row):
            if ch == '#': img.putpixel((33 + px, 18 + py), C_RED)
    for py, row in enumerate(['# #', '# #', '# #', '# #', '###']):
        for px, ch in enumerate(row):
            if ch == '#': img.putpixel((38 + px, 18 + py), C_RED)
    for py, row in enumerate(['###', '#  ', '###', '  #', '###']):
        for px, ch in enumerate(row):
            if ch == '#': img.putpixel((43 + px, 18 + py), C_RED)

    # 3. CRT Monitor Screen (y=27..52, x=19..51)
    draw.rectangle([18, 27, 52, 52], fill=(20, 26, 30, 255), outline=C_OUTLINE)
    draw.rectangle([21, 29, 49, 50], fill=(12, 28, 48, 255))
    for sy in range(30, 50, 2):
        draw.line([(21, sy), (49, sy)], fill=(18, 40, 68, 255))

    # Screen Graphics: Retro 8-bit Golden Star in center of screen!
    star_pixels = [
        (35, 33), (34, 34), (35, 34), (36, 34), (34, 35), (35, 35), (36, 35),
        (31, 37), (32, 37), (33, 37), (34, 37), (35, 37), (36, 37), (37, 37), (38, 37), (39, 37),
        (32, 38), (33, 38), (34, 38), (35, 38), (36, 38), (37, 38), (38, 38),
        (33, 39), (34, 39), (35, 39), (36, 39), (37, 39),
        (33, 40), (34, 40), (35, 40), (36, 40), (37, 40),
        (32, 41), (33, 41), (34, 41), (36, 41), (37, 41), (38, 41),
        (32, 42), (33, 42), (37, 42), (38, 42),
        (31, 43), (32, 43), (38, 43), (39, 43)
    ]
    for px, py in star_pixels:
        img.putpixel((px, py), C_GOLD)
    draw.rectangle([34, 36, 36, 39], fill=C_WHITE)

    for sx, sy in [(24, 34), (46, 34), (25, 46), (45, 46)]:
        img.putpixel((sx, sy), C_CYAN)
        draw.point((sx, sy), fill=C_WHITE)

    # 4. Angled Arcade Control Deck (y=53..63, x=17..53)
    draw.polygon([(17, 53), (53, 53), (52, 63), (18, 63)], fill=(32, 40, 44, 255), outline=C_OUTLINE)
    draw.line([(18, 54), (52, 54)], fill=C_CABINET_HL)

    # Joystick (x=26)
    draw.ellipse([23, 59, 29, 62], fill=(15, 18, 20, 255))
    draw.line([(26, 56), (26, 60)], fill=(180, 190, 200, 255), width=2)
    draw.ellipse([24, 53, 28, 57], fill=C_RED, outline=C_OUTLINE)
    draw.point((25, 54), fill=C_WHITE)

    # Buttons (x=35, 40, 45)
    draw.ellipse([34, 56, 37, 59], fill=C_CYAN, outline=C_OUTLINE)
    draw.point((35, 57), fill=C_WHITE)
    draw.ellipse([39, 57, 42, 60], fill=C_GOLD, outline=C_OUTLINE)
    draw.point((40, 58), fill=C_WHITE)
    draw.ellipse([44, 56, 47, 59], fill=C_RED, outline=C_OUTLINE)
    draw.point((45, 57), fill=C_WHITE)

    # 5. Lower Cabinet & Coin Door (y=64..78, x=18..52)
    draw.rectangle([18, 64, 52, 78], fill=(35, 45, 50, 255), outline=C_OUTLINE)
    draw.rectangle([25, 66, 45, 76], fill=(20, 25, 28, 255), outline=C_OUTLINE)
    for cx in [29, 39]:
        draw.rectangle([cx, 68, cx + 3, 73], fill=(255, 140, 0, 255), outline=C_OUTLINE)
        draw.line([(cx + 1, 69), (cx + 1, 72)], fill=(40, 10, 0, 255))
        draw.point((cx + 1, 74), fill=(180, 190, 200, 255))

    draw_vertical_joker_text(img, (79, 99, 103, 255), top_left=True, bottom_right=True)
    export_sprite(img, "j_bonus_stage.png")

def build_j_overdrive():
    """Builds Overdrive Joker (71x95 px, 142x190 2x) on authentic Mult Card fiery background.
    Features a high-performance hot-rod tachometer revving past 9,000 RPM into the redline:
    - Heavy chrome circular gauge bezel with corner mounting bolts and specular shine
    - Matte black dial face with white low-RPM ticks and vibrant glowing red OVERDRIVE redline zone
    - Pinned orange-red indicator needle revved to the max with heat sparks
    - Top redline shift warning light
    - Twin chrome exhaust pipes at base spitting backfire flames
    - Vertical JOKER typography along margins
    """
    img = load_enhancement_base("mult")
    draw = ImageDraw.Draw(img)

    C_OUTLINE = (26, 28, 30, 255)
    C_CHROME_HL = (245, 250, 255, 255)
    C_CHROME_MID = (185, 195, 205, 255)
    C_CHROME_DARK = (90, 100, 110, 255)
    C_DIAL_BG = (18, 20, 24, 255)

    C_RED_HOT = (255, 40, 30, 255)
    C_RED_MULT = (254, 95, 85, 255)
    C_GOLD = (243, 185, 88, 255)
    C_WHITE = (255, 255, 255, 255)

    cx, cy = 35, 46
    r_outer = 23
    r_bezel = 20
    r_dial = 18

    # 1. Hot Rod Gauge Mounting Bracket & Exhaust flame pipes
    draw.polygon([(16, 62), (22, 60), (25, 74), (18, 76)], fill=C_CHROME_DARK, outline=C_OUTLINE)
    draw.polygon([(54, 62), (48, 60), (45, 74), (52, 76)], fill=C_CHROME_DARK, outline=C_OUTLINE)
    draw.polygon([(17, 75), (15, 83), (21, 78), (24, 85), (25, 75)], fill=(255, 120, 0, 255))
    draw.polygon([(19, 75), (18, 80), (22, 77)], fill=C_GOLD)
    draw.polygon([(46, 75), (47, 85), (50, 78), (55, 83), (53, 75)], fill=(255, 120, 0, 255))
    draw.polygon([(49, 75), (51, 80), (48, 77)], fill=C_GOLD)

    # 2. Outer Chrome Gauge Bezel Ring
    draw.ellipse([cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer], fill=C_CHROME_MID, outline=C_OUTLINE)
    draw.ellipse([cx - r_bezel, cy - r_bezel, cx + r_bezel, cy + r_bezel], fill=C_CHROME_DARK)
    for deg in range(120, 240):
        rad = math.radians(deg)
        bx = int(cx + (r_outer - 1) * math.cos(rad))
        by = int(cy + (r_outer - 1) * math.sin(rad))
        img.putpixel((bx, by), C_CHROME_HL)

    # Bezel rivets
    for sx, sy in [(cx - 16, cy - 16), (cx + 16, cy - 16), (cx - 16, cy + 16), (cx + 16, cy + 16)]:
        draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=C_CHROME_HL, outline=C_OUTLINE)

    # 3. Tachometer Dial Face
    draw.ellipse([cx - r_dial, cy - r_dial, cx + r_dial, cy + r_dial], fill=C_DIAL_BG, outline=C_OUTLINE)

    # 4. RPM Ticks & Redline Band
    for deg in range(135, 271, 15):
        rad = math.radians(deg)
        x1 = int(cx + (r_dial - 1) * math.cos(rad))
        y1 = int(cy + (r_dial - 1) * math.sin(rad))
        x2 = int(cx + (r_dial - 4) * math.cos(rad))
        y2 = int(cy + (r_dial - 4) * math.sin(rad))
        draw.line([(x1, y1), (x2, y2)], fill=(180, 190, 200, 255))

    # REDLINE / OVERDRIVE ZONE: 270 deg to 405 deg (7,000 to 10,000+ RPM)
    for deg in range(270, 406, 2):
        rad = math.radians(deg)
        rx = int(cx + (r_dial - 2) * math.cos(rad))
        ry = int(cy + (r_dial - 2) * math.sin(rad))
        img.putpixel((rx, ry), C_RED_HOT)
        rx2 = int(cx + (r_dial - 3) * math.cos(rad))
        ry2 = int(cy + (r_dial - 3) * math.sin(rad))
        img.putpixel((rx2, ry2), C_RED_MULT)

    for deg in range(270, 406, 15):
        rad = math.radians(deg)
        x1 = int(cx + (r_dial - 1) * math.cos(rad))
        y1 = int(cy + (r_dial - 1) * math.sin(rad))
        x2 = int(cx + (r_dial - 5) * math.cos(rad))
        y2 = int(cy + (r_dial - 5) * math.sin(rad))
        draw.line([(x1, y1), (x2, y2)], fill=C_RED_HOT, width=1)

    # Dial text: 'RPM x1000' and red 'O/D' marking
    draw.line([(31, 56), (39, 56)], fill=(120, 130, 140, 255))
    draw.point((42, 36), fill=C_RED_HOT)
    draw.point((43, 36), fill=C_RED_HOT)
    draw.point((44, 36), fill=C_RED_HOT)

    # 5. Overdrive Warning Light at Top of Gauge
    draw.ellipse([33, 29, 37, 33], fill=C_RED_HOT, outline=C_OUTLINE)
    draw.point((35, 31), fill=C_WHITE)

    # 6. Pinned Tachometer Needle (into Redline at ~9,500 RPM)
    tip_x, tip_y = 48, 38
    draw.line([(cx, cy), (tip_x, tip_y)], fill=C_RED_HOT, width=2)
    draw.line([(cx, cy), (tip_x, tip_y)], fill=C_WHITE, width=1)
    draw.point((tip_x, tip_y), fill=C_WHITE)
    draw.point((tip_x + 1, tip_y), fill=C_RED_HOT)

    # Center Hub
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=C_CHROME_MID, outline=C_OUTLINE)
    draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(30, 30, 35, 255))
    draw.point((cx - 1, cy - 1), fill=C_WHITE)

    # 7. Red heat haze & sparks
    sparks = [(47, 33), (52, 36), (50, 42), (44, 30), (51, 30)]
    for sx, sy in sparks:
        img.putpixel((sx, sy), C_WHITE)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            img.putpixel((sx+dx, sy+dy), C_RED_HOT)

    draw_vertical_joker_text(img, (79, 99, 103, 255), top_left=True, bottom_right=True)
    export_sprite(img, "j_overdrive.png")

def build_j_kaleidoscope():
    """Builds Kaleidoscope Joker (71x95 px, 142x190 2x) on authentic Wild Card background."""
    img = load_enhancement_base("wild")

    # Relocate bleeding red suit pips inward so the red dot does not cover or occlude JOKER text:
    tl_red = []
    for y in range(15, 42):
        for x in range(4, 15):
            if img.getpixel((x, y))[:3] == (254, 95, 85):
                tl_red.append((x, y))
                img.putpixel((x, y), (255, 255, 255, 255))
    for x, y in tl_red:
        img.putpixel((x + 8, y), (254, 95, 85, 255))

    br_red = []
    for y in range(54, 80):
        for x in range(56, 68):
            if img.getpixel((x, y))[:3] == (254, 95, 85):
                br_red.append((x, y))
                img.putpixel((x, y), (255, 255, 255, 255))
    for x, y in br_red:
        img.putpixel((x - 8, y), (254, 95, 85, 255))

    draw = ImageDraw.Draw(img)

    C_OUTLINE = PALETTE["DEEP_OUTLINE"]
    C_BRASS = (205, 155, 60, 255)
    C_BRASS_HL = (255, 220, 120, 255)
    C_BRASS_DARK = (130, 95, 30, 255)
    C_RED = PALETTE["MULT_RED"]
    C_BLUE = PALETTE["CHIPS_BLUE"]
    C_GREEN = (75, 194, 146, 255)
    C_PURPLE = (158, 123, 181, 255)
    C_WHITE = PALETTE["CARD_WHITE"]

    cx, cy, r = 35, 46, 21
    draw.ellipse([cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2], fill=C_BRASS_DARK, outline=C_OUTLINE)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=C_BRASS)
    draw.ellipse([cx - r + 3, cy - r + 3, cx + r - 3, cy + r - 3], fill=C_OUTLINE)

    # 4 Prismatic Petals
    draw.polygon([(cx, cy), (cx - 14, cy - 14), (cx, cy - 17), (cx + 14, cy - 14)], fill=C_RED, outline=C_OUTLINE)
    draw.polygon([(cx, cy), (cx + 14, cy - 14), (cx + 17, cy), (cx + 14, cy + 14)], fill=C_BLUE, outline=C_OUTLINE)
    draw.polygon([(cx, cy), (cx + 14, cy + 14), (cx, cy + 17), (cx - 14, cy + 14)], fill=C_GREEN, outline=C_OUTLINE)
    draw.polygon([(cx, cy), (cx - 14, cy + 14), (cx - 17, cy), (cx - 14, cy - 14)], fill=C_PURPLE, outline=C_OUTLINE)

    # Prismatic faceted lines from center
    draw.line([(cx - 12, cy), (cx + 12, cy)], fill=C_WHITE, width=1)
    draw.line([(cx, cy - 12), (cx, cy + 12)], fill=C_WHITE, width=1)
    draw.line([(cx - 9, cy - 9), (cx + 9, cy + 9)], fill=C_WHITE, width=1)
    draw.line([(cx - 9, cy + 9), (cx + 9, cy - 9)], fill=C_WHITE, width=1)

    # Center jewel facet
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=C_BRASS_HL, outline=C_OUTLINE)
    draw.point((cx - 1, cy - 1), fill=C_WHITE)

    for deg in range(0, 360, 45):
        rad = math.radians(deg)
        nx = int(cx + (r + 1) * math.cos(rad))
        ny = int(cy + (r + 1) * math.sin(rad))
        draw.point((nx, ny), fill=C_BRASS_HL)

    draw_vertical_joker_text(img, PALETTE["DARK_SLATE"], top_left=True, bottom_right=True)
    export_sprite(img, "j_kaleidoscope.png")

def build_j_glassblower():
    """Builds Glassblower Joker (71x95 px, 142x190 2x) on authentic Glass Card background."""
    img = load_enhancement_base("glass")
    draw = ImageDraw.Draw(img)

    C_OUTLINE = PALETTE["DEEP_OUTLINE"]
    C_IRON = (70, 75, 80, 255)
    C_IRON_HL = (120, 130, 138, 255)
    C_CYAN = (120, 220, 245, 230)
    C_CYAN_DIM = (60, 140, 175, 200)
    C_ORANGE = (255, 120, 40, 255)
    C_YELLOW = (255, 210, 80, 255)
    C_WHITE = PALETTE["CARD_WHITE"]

    # Diagonal iron blowpipe
    draw.line([(14, 78), (34, 46)], fill=C_OUTLINE, width=4)
    draw.line([(14, 78), (34, 46)], fill=C_IRON, width=2)
    draw.line([(15, 77), (35, 45)], fill=C_IRON_HL, width=1)
    draw.ellipse([12, 76, 17, 81], fill=C_IRON, outline=C_OUTLINE)

    # Crystal Glass Sphere
    cx, cy, r = 42, 36, 16
    draw.ellipse([cx - r - 1, cy - r - 1, cx + r + 1, cy + r + 1], fill=(40, 70, 90, 255), outline=C_OUTLINE)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=C_CYAN_DIM)
    draw.ellipse([cx - r + 2, cy - r + 2, cx + r - 2, cy + r - 2], fill=C_CYAN)

    # Molten glass core
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=C_ORANGE)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=C_YELLOW)
    draw.point((cx - 1, cy - 1), fill=C_WHITE)

    # Glass fractures
    draw.line([(cx + 3, cy - 12), (cx + 8, cy - 6)], fill=C_WHITE, width=1)
    draw.line([(cx + 8, cy - 6), (cx + 5, cy + 2)], fill=C_WHITE, width=1)
    draw.line([(cx - 10, cy + 4), (cx - 4, cy + 9)], fill=C_WHITE, width=1)
    draw.arc([cx - r + 3, cy - r + 3, cx + r - 3, cy + r - 3], start=200, end=290, fill=C_WHITE, width=2)

    for sx, sy in [(58, 22), (61, 38), (30, 26), (54, 52)]:
        draw.point((sx, sy), fill=C_YELLOW)
        draw.point((sx + 1, sy), fill=C_ORANGE)

    draw_vertical_joker_text(img, PALETTE["DARK_SLATE"], top_left=True, bottom_right=True)
    export_sprite(img, "j_glassblower.png")

def build_j_the_anvil():
    """Builds The Anvil Joker (71x95 px, 142x190 2x) on authentic Steel Card background."""
    img = load_enhancement_base("steel")
    draw = ImageDraw.Draw(img)

    C_OUTLINE = PALETTE["DEEP_OUTLINE"]
    C_IRON = (70, 78, 85, 255)
    C_IRON_HL = (130, 142, 155, 255)
    C_IRON_DARK = (45, 50, 55, 255)
    C_HOT_RED = (235, 65, 45, 255)
    C_HOT_GOLD = (255, 195, 60, 255)
    C_WOOD = (95, 62, 38, 255)

    # Oak stump base
    draw.rectangle([22, 66, 48, 82], fill=C_WOOD, outline=C_OUTLINE)
    draw.line([(24, 68), (46, 68)], fill=(130, 90, 55, 255))
    draw.line([(23, 75), (47, 75)], fill=(65, 42, 25, 255))

    # Anvil silhouette
    draw.polygon([(20, 66), (50, 66), (46, 58), (24, 58)], fill=C_IRON_DARK, outline=C_OUTLINE)
    draw.rectangle([28, 52, 42, 58], fill=C_IRON, outline=C_OUTLINE)
    face_pts = [(14, 46), (26, 44), (56, 44), (56, 52), (44, 52), (24, 52)]
    draw.polygon(face_pts, fill=C_IRON, outline=C_OUTLINE)
    draw.line([(27, 45), (55, 45)], fill=C_IRON_HL, width=1)

    # Red-hot glowing steel bar
    draw.rectangle([32, 41, 46, 44], fill=C_HOT_RED, outline=C_OUTLINE)
    draw.line([(33, 42), (45, 42)], fill=C_HOT_GOLD, width=1)

    # Sledgehammer
    draw.line([(48, 20), (38, 38)], fill=C_WOOD, width=3)
    draw.line([(48, 20), (38, 38)], fill=C_OUTLINE, width=1)
    draw.polygon([(34, 34), (43, 29), (46, 34), (37, 39)], fill=C_IRON_HL, outline=C_OUTLINE)

    sparks = [(30, 39), (48, 38), (36, 32), (44, 42), (28, 35)]
    for sx, sy in sparks:
        draw.point((sx, sy), fill=C_HOT_GOLD)
        draw.point((sx + 1, sy), fill=C_HOT_RED)

    draw_vertical_joker_text(img, PALETTE["DARK_SLATE"], top_left=True, bottom_right=True)
    export_sprite(img, "j_the_anvil.png")

def build_j_monolith():
    """Builds Monolith Joker (71x95 px, 142x190 2x) on authentic Stone Card background."""
    img = load_enhancement_base("stone")
    draw = ImageDraw.Draw(img)

    C_OUTLINE = PALETTE["DEEP_OUTLINE"]
    C_STONE = (115, 125, 130, 255)
    C_STONE_HL = (170, 180, 185, 255)
    C_STONE_DARK = (65, 75, 80, 255)
    C_RUNE_CYAN = (0, 215, 255, 255)
    C_RUNE_GLOW = (0, 140, 200, 255)
    C_WHITE = PALETTE["CARD_WHITE"]

    # Stone pile base
    for bx, by, bw, bh in [(18, 72, 12, 8), (40, 71, 14, 9), (28, 74, 16, 7)]:
        draw.ellipse([bx, by, bx + bw, by + bh], fill=C_STONE_DARK, outline=C_OUTLINE)
        draw.point((bx + 3, by + 2), fill=C_STONE_HL)

    # Monolith slab
    slab_pts = [(28, 20), (43, 22), (46, 72), (24, 72)]
    draw.polygon(slab_pts, fill=C_STONE_DARK, outline=C_OUTLINE)
    front_pts = [(29, 22), (41, 23), (43, 71), (26, 71)]
    draw.polygon(front_pts, fill=C_STONE)
    draw.line([(29, 22), (26, 71)], fill=C_STONE_HL, width=1)

    # Runes
    draw.polygon([(35, 27), (38, 30), (35, 33), (32, 30)], fill=C_RUNE_GLOW, outline=C_RUNE_CYAN)
    draw.point((35, 30), fill=C_WHITE)

    draw.line([(31, 38), (39, 38)], fill=C_RUNE_CYAN, width=2)
    draw.line([(35, 35), (35, 42)], fill=C_RUNE_CYAN, width=1)
    draw.point((35, 38), fill=C_WHITE)

    draw.line([(32, 51), (35, 47)], fill=C_RUNE_CYAN, width=2)
    draw.line([(35, 47), (38, 51)], fill=C_RUNE_CYAN, width=2)
    draw.point((35, 48), fill=C_WHITE)

    draw.ellipse([33, 57, 37, 61], fill=C_RUNE_GLOW, outline=C_RUNE_CYAN)
    draw.point((35, 59), fill=C_WHITE)

    draw.line([(40, 32), (43, 36)], fill=C_OUTLINE, width=1)
    draw.line([(28, 54), (31, 57)], fill=C_OUTLINE, width=1)

    draw_vertical_joker_text(img, PALETTE["DARK_SLATE"], top_left=True, bottom_right=True)
    export_sprite(img, "j_monolith.png")

def build_j_bullion():
    """Builds Bullion Joker (71x95 px, 142x190 2x) on authentic Gold Card background."""
    img = load_enhancement_base("gold")
    draw = ImageDraw.Draw(img)

    C_OUTLINE = PALETTE["DEEP_OUTLINE"]
    C_GOLD = PALETTE["GOLD_YELLOW"]
    C_GOLD_HL = PALETTE["GOLD_HL"]
    C_GOLD_SHADOW = PALETTE["GOLD_SHADOW"]
    C_BRONZE = (150, 95, 30, 255)
    C_GREEN_FELT = (35, 95, 65, 255)
    C_WHITE = PALETTE["CARD_WHITE"]

    draw.ellipse([15, 68, 55, 80], fill=C_GREEN_FELT, outline=C_OUTLINE)

    def draw_gold_bar(x, y, w, h):
        draw.polygon([(x + 2, y + h), (x + w - 2, y + h), (x + w, y + h - 2), (x, y + h - 2)], fill=C_BRONZE)
        draw.rectangle([x, y + 3, x + w, y + h], fill=C_GOLD_SHADOW, outline=C_OUTLINE)
        top_pts = [(x + 3, y), (x + w - 3, y), (x + w, y + 4), (x, y + 4)]
        draw.polygon(top_pts, fill=C_GOLD, outline=C_OUTLINE)
        draw.line([(x + 4, y + 1), (x + w - 4, y + 1)], fill=C_GOLD_HL, width=1)
        cx = x + w // 2
        draw.line([(cx - 5, y + h - 3), (cx + 5, y + h - 3)], fill=C_BRONZE, width=1)

    draw_gold_bar(19, 56, 16, 9)
    draw_gold_bar(36, 56, 16, 9)
    draw_gold_bar(23, 46, 16, 9)
    draw_gold_bar(32, 46, 16, 9)
    draw_gold_bar(27, 36, 17, 9)

    sparkles = [(22, 34), (48, 32), (18, 52), (53, 50), (35, 26)]
    for sx, sy in sparkles:
        draw.point((sx, sy), fill=C_GOLD_HL)
        draw.point((sx + 1, sy), fill=C_GOLD)
        draw.point((sx, sy), fill=C_WHITE)

    draw_vertical_joker_text(img, PALETTE["DARK_SLATE"], top_left=True, bottom_right=True)
    export_sprite(img, "j_bullion.png")

def build_j_golden_horseshoe():
    """Builds Golden Horseshoe Joker (71x95 px, 142x190 2x) - Solid, unbroken continuous 24k gold horseshoe on authentic Lucky Card background."""
    img = load_enhancement_base("lucky")
    draw = ImageDraw.Draw(img)

    C_OUTLINE = PALETTE["DEEP_OUTLINE"]
    C_GOLD = PALETTE["GOLD_YELLOW"]
    C_GOLD_HL = PALETTE["GOLD_HL"]
    C_GOLD_SHADOW = PALETTE["GOLD_SHADOW"]
    C_BRONZE = (155, 105, 35, 255)
    C_GREEN = (75, 194, 146, 255)
    C_WHITE = PALETTE["CARD_WHITE"]

    # Emerald ribbon bow at base
    draw.polygon([(30, 64), (35, 68), (40, 64), (35, 62)], fill=C_GREEN, outline=C_OUTLINE)
    draw.line([(32, 68), (30, 75)], fill=C_GREEN, width=2)
    draw.line([(38, 68), (40, 75)], fill=C_GREEN, width=2)

    # 100% Solid Continuous Horseshoe Polygon:
    # Outer contour from left tip (18, 24) curving down around to (35, 68) and up to right tip (52, 24).
    # Then inner contour carving out the center hollow smoothly without cutting through!
    horseshoe_poly = [
        # Left heel flat top
        (18, 24), (26, 24),
        # Inner contour curving down
        (26, 44), (28, 50), (31, 54), (35, 56), (39, 54), (42, 50), (44, 44),
        # Right heel flat top
        (44, 24), (52, 24),
        # Outer contour curving down
        (52, 44), (51, 52), (48, 60), (43, 65), (35, 68), (27, 65), (22, 60), (19, 52), (18, 44)
    ]
    # Draw drop shadow
    shadow_poly = [(px + 1, py + 1) for px, py in horseshoe_poly]
    draw.polygon(shadow_poly, fill=C_BRONZE)

    # Draw solid gold horseshoe body (continuous yellow uniting upper heels with the U)
    draw.polygon(horseshoe_poly, fill=C_GOLD, outline=C_OUTLINE)

    # Continuous golden highlight stripe down the center of each arm and around the arch
    draw.line([(22, 26), (22, 46)], fill=C_GOLD_HL, width=2)
    draw.line([(48, 26), (48, 46)], fill=C_GOLD_HL, width=2)
    draw.arc([23, 44, 47, 64], start=30, end=150, fill=C_GOLD_HL, width=2)

    # Outer and inner rim shading
    draw.arc([19, 26, 51, 66], start=0, end=180, fill=C_GOLD_SHADOW, width=1)

    # 7 Square Nail Holes along the horseshoe
    holes = [
        (22, 28), (21, 36), (23, 45),
        (35, 62),
        (47, 45), (49, 36), (48, 28)
    ]
    for hx, hy in holes:
        draw.rectangle([hx - 1, hy - 1, hx + 1, hy + 1], fill=C_OUTLINE)
        draw.point((hx, hy), fill=(40, 40, 40, 255))

    # Lucky sparkles radiating from horseshoe
    sparkles = [(14, 20), (56, 18), (35, 18), (13, 56), (57, 56)]
    for sx, sy in sparkles:
        draw.point((sx, sy), fill=C_GOLD_HL)
        draw.point((sx + 1, sy), fill=C_GOLD)
        draw.point((sx - 1, sy), fill=C_GOLD)
        draw.point((sx, sy + 1), fill=C_GOLD)
        draw.point((sx, sy - 1), fill=C_GOLD)
        draw.point((sx, sy), fill=C_WHITE)

    draw_vertical_joker_text(img, PALETTE["DARK_SLATE"], top_left=True, bottom_right=True)
    export_sprite(img, "j_golden_horseshoe.png")

def build_j_fortune_cookie():
    """Builds Fortune Cookie Joker (71x95 px, 142x190 2x) - Golden-brown cracked fortune cookie with white paper slip showing Tarot & Planet symbols."""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    C_OUTLINE = PALETTE["DEEP_OUTLINE"]
    C_COOKIE_BASE = (224, 162, 78, 255)
    C_COOKIE_DARK = (152, 90, 34, 255)
    C_COOKIE_DEEP = (102, 54, 18, 255)
    C_COOKIE_HL = (248, 210, 140, 255)
    C_COOKIE_PALE = (255, 232, 178, 255)
    C_PAPER = (255, 255, 255, 255)
    C_PAPER_SHADOW = (212, 220, 218, 255)
    C_TAROT_PURPLE = (158, 123, 181, 255)
    C_PLANET_CYAN = (19, 175, 206, 255)
    C_GOLD_SPARK = PALETTE["GOLD_HL"]
    C_WHITE = PALETTE["CARD_WHITE"]

    # 1. Soft oval drop shadow on table
    draw.ellipse([14, 58, 58, 72], fill=(215, 222, 218, 200))

    # 2. White fortune paper slip sticking out between halves
    paper_poly = [(26, 36), (46, 32), (48, 42), (28, 46)]
    draw.polygon([(px + 1, py + 1) for px, py in paper_poly], fill=C_PAPER_SHADOW)
    draw.polygon(paper_poly, fill=C_PAPER, outline=C_OUTLINE)

    # Dithered Planet symbol (cyan circle with tilted orbit ring) at (33, 39)
    draw.ellipse([32, 38, 35, 41], fill=C_PLANET_CYAN)
    draw.line([(30, 40), (37, 39)], fill=C_PLANET_CYAN, width=1)
    draw.point((33, 39), fill=C_WHITE)

    # Dithered Tarot symbol (mystical purple diamond / eye) at (41, 37)
    draw.polygon([(41, 35), (43, 37), (41, 39), (39, 37)], fill=C_TAROT_PURPLE)
    draw.point((41, 37), fill=C_WHITE)

    # 3. Left Cookie Half (cracked & tilted leftward)
    left_cookie = [
        (17, 50), (19, 42), (24, 38), (30, 40), (33, 44),
        (31, 52), (28, 58), (22, 60), (18, 56)
    ]
    draw.polygon(left_cookie, fill=C_COOKIE_BASE, outline=C_OUTLINE)
    # Inner fold / hollow toasted shadow
    draw.polygon([(26, 42), (32, 45), (29, 52), (25, 48)], fill=C_COOKIE_DEEP)
    draw.polygon([(24, 40), (28, 42), (27, 49), (23, 46)], fill=C_COOKIE_DARK)
    # Toasted highlight ridge along outer curve
    draw.arc([18, 38, 30, 58], start=120, end=260, fill=C_COOKIE_HL, width=2)
    draw.line([(20, 44), (22, 54)], fill=C_COOKIE_PALE, width=1)
    # Jagged fracture edge
    draw.line([(30, 40), (33, 44), (30, 48), (32, 52), (28, 58)], fill=C_OUTLINE, width=1)

    # 4. Right Cookie Half (cracked & tilted rightward)
    right_cookie = [
        (39, 44), (42, 40), (48, 38), (53, 42), (55, 50),
        (54, 56), (50, 60), (44, 58), (41, 52)
    ]
    draw.polygon(right_cookie, fill=C_COOKIE_BASE, outline=C_OUTLINE)
    # Inner fold / hollow toasted shadow
    draw.polygon([(40, 45), (46, 42), (47, 48), (43, 52)], fill=C_COOKIE_DEEP)
    draw.polygon([(44, 42), (48, 40), (49, 46), (45, 49)], fill=C_COOKIE_DARK)
    # Toasted highlight ridge along outer curve
    draw.arc([42, 38, 54, 58], start=280, end=60, fill=C_COOKIE_HL, width=2)
    draw.line([(52, 44), (50, 54)], fill=C_COOKIE_PALE, width=1)
    # Jagged fracture edge
    draw.line([(39, 44), (42, 48), (40, 52), (44, 58)], fill=C_OUTLINE, width=1)

    # 5. Crisp cookie crumbs scattered beneath the break
    crumbs = [(35, 58), (37, 63), (33, 65), (24, 63), (48, 64), (36, 68)]
    for cx, cy in crumbs:
        draw.point((cx, cy), fill=C_COOKIE_DARK)
        draw.point((cx + 1, cy), fill=C_COOKIE_BASE)

    # 6. Floating lucky golden sparkles
    sparkles = [(16, 28), (54, 26), (36, 22), (20, 68), (52, 68)]
    for sx, sy in sparkles:
        draw.point((sx, sy), fill=C_GOLD_SPARK)
        draw.point((sx + 1, sy), fill=PALETTE["GOLD_YELLOW"])
        draw.point((sx, sy), fill=C_WHITE)

    draw_vertical_joker_text(img, PALETTE["DARK_SLATE"], top_left=True, bottom_right=True)
    export_sprite(img, "j_fortune_cookie.png")

def build_j_hot_pepper(variant=1):
    """Builds Hot Pepper Joker (71x95 px, 142x190 2x) - Red hot chili pepper with dynamic fire backdrop.
    variant=1: Dark flame border framing (inspired by reference image with dark center & licking side flames)
    variant=2: Chromatic/psychedelic fire (blue, magenta, yellow)
    variant=3: Full golden roaring inferno
    """
    img = create_card_base()
    draw = ImageDraw.Draw(img)
    C_OUTLINE = (20, 10, 10, 255)

    if variant == 2:
        # Deep abyss navy-blue background
        for y in range(1, 94):
            factor = y / 94.0
            r = int(12 + 10 * factor)
            g = int(14 + 12 * factor)
            b = int(28 + 20 * factor)
            draw.line([(1, y), (69, y)], fill=(r, g, b, 255))

        draw.rectangle([3, 3, 67, 91], outline=(30, 40, 75, 255))

        # Outer Electric Blue / Cyan flames
        flame_blue_pts = [
            (4, 93), (6, 65), (10, 40), (14, 54), (18, 30), (22, 48), (26, 24),
            (32, 40), (36, 18), (42, 38), (46, 22), (50, 44), (54, 28), (58, 52),
            (62, 38), (66, 62), (66, 93)
        ]
        draw.polygon(flame_blue_pts, fill=(0, 160, 255, 255))

        # Vibrant Magenta / Purple layer
        flame_magenta_pts = [
            (8, 93), (11, 72), (14, 50), (18, 62), (22, 38), (26, 54), (30, 32),
            (35, 46), (38, 26), (42, 44), (46, 32), (50, 52), (54, 40), (58, 62),
            (61, 74), (62, 93)
        ]
        draw.polygon(flame_magenta_pts, fill=(235, 30, 140, 255))

        # Fiery Orange / Coral transition
        flame_coral_pts = [
            (12, 93), (15, 78), (18, 60), (22, 68), (26, 48), (30, 60),
            (35, 38), (40, 52), (44, 42), (48, 58), (52, 48), (56, 68), (58, 93)
        ]
        draw.polygon(flame_coral_pts, fill=(255, 110, 40, 255))

        # Core Golden Yellow / White
        flame_yellow_pts = [
            (16, 93), (20, 80), (25, 62), (30, 70), (35, 48), (40, 60), (45, 52), (50, 72), (54, 93)
        ]
        draw.polygon(flame_yellow_pts, fill=(255, 235, 80, 255))
        draw.polygon([(26, 85), (32, 66), (36, 56), (40, 66), (44, 85)], fill=(255, 255, 220, 255))

        # Chromatic Sparks (cyan, pink, yellow)
        sparks = [
            ((12, 22), (0, 220, 255, 255)),
            ((18, 14), (255, 80, 180, 255)),
            ((35, 10), (255, 240, 120, 255)),
            ((52, 14), (0, 220, 255, 255)),
            ((58, 22), (255, 80, 180, 255)),
            ((28, 18), (255, 220, 80, 255)),
            ((42, 16), (0, 230, 255, 255))
        ]
        for (sx, sy), col in sparks:
            draw.point((sx, sy), fill=col)
            draw.point((sx, sy + 1), fill=col)

        text_color = (220, 245, 255, 255)

    elif variant == 3:
        # Deep fiery ember background
        for y in range(1, 94):
            factor = y / 94.0
            r = int(50 + 40 * factor)
            g = int(10 + 15 * factor)
            b = int(6 + 8 * factor)
            draw.line([(1, y), (69, y)], fill=(r, g, b, 255))

        # Dense swirling flame tendrils (Deep Amber Orange)
        flame_amber_pts = [
            (3, 93), (4, 55), (8, 34), (12, 48), (17, 24), (21, 42), (27, 18),
            (33, 36), (37, 14), (43, 32), (47, 18), (53, 38), (57, 22), (62, 45),
            (66, 32), (67, 60), (67, 93)
        ]
        draw.polygon(flame_amber_pts, fill=(255, 90, 20, 255))

        # Bright Golden Tendrils
        flame_gold_pts = [
            (6, 93), (8, 62), (12, 42), (16, 56), (20, 32), (25, 48), (29, 26),
            (34, 42), (38, 22), (42, 38), (46, 26), (50, 46), (54, 30), (58, 54),
            (62, 40), (64, 68), (64, 93)
        ]
        draw.polygon(flame_gold_pts, fill=(255, 175, 30, 255))

        # Brilliant Lemon / Cream White Flame Ribbons
        flame_ribbon_pts = [
            (10, 93), (14, 70), (18, 50), (22, 64), (26, 40), (31, 56),
            (35, 32), (40, 48), (44, 34), (48, 54), (52, 42), (56, 62), (59, 78), (60, 93)
        ]
        draw.polygon(flame_ribbon_pts, fill=(255, 235, 75, 255))

        # Pure white hot curling tips
        tips = [(26, 40), (35, 32), (44, 34), (52, 42), (38, 22), (29, 26), (46, 26)]
        for tx, ty in tips:
            draw.line([(tx - 1, ty), (tx + 1, ty)], fill=(255, 255, 220, 255))
            draw.point((tx, ty - 1), fill=(255, 255, 255, 255))

        # Dense swirling ember storm
        embers = [
            (8, 20), (15, 12), (24, 8), (35, 6), (46, 8), (56, 14), (63, 18),
            (12, 28), (20, 22), (31, 16), (42, 14), (52, 20), (60, 26),
            (18, 36), (48, 32), (28, 28)
        ]
        for ex, ey in embers:
            draw.point((ex, ey), fill=(255, 255, 180, 255))
            draw.point((ex, ey + 1), fill=(255, 190, 50, 255))

        text_color = (255, 255, 255, 255)

    else:
        # VARIANT 1: Natural, fluid organic curving flame tongues
        # Deep dark crimson-charcoal gradient background
        for y in range(1, 94):
            factor = y / 94.0
            r = int(20 + 22 * factor)
            g = int(4 + 3 * factor)
            b = int(6 + 3 * factor)
            draw.line([(1, y), (69, y)], fill=(r, g, b, 255))

        # Dark inner border
        draw.rectangle([3, 3, 67, 91], outline=(55, 12, 16, 255))

        # Ambient fiery glow behind center
        for rad in range(28, 0, -3):
            alpha = int(115 * (1 - rad / 28.0))
            glow_box = [35 - rad, 54 - rad, 35 + rad, 54 + rad]
            draw.ellipse(glow_box, fill=(185, 42, 12, alpha))

        # Natural Curving Flames (Using smooth Bezier curves)
        # Layer 1: Outer Red Flame Contour
        red_curves = [(3, 93)]
        red_curves.extend(bezier_points((3, 93), (4, 70), (3, 50), (4, 32)))
        red_curves.extend(bezier_points((4, 32), (6, 24), (10, 26), (9, 36)))
        red_curves.extend(bezier_points((9, 36), (11, 48), (14, 52), (16, 42)))
        red_curves.extend(bezier_points((16, 42), (18, 28), (24, 25), (25, 35)))
        red_curves.extend(bezier_points((25, 35), (27, 46), (30, 48), (32, 38)))
        red_curves.extend(bezier_points((32, 38), (34, 24), (40, 22), (42, 34)))
        red_curves.extend(bezier_points((42, 34), (44, 46), (47, 48), (49, 38)))
        red_curves.extend(bezier_points((49, 38), (51, 26), (56, 28), (57, 42)))
        red_curves.extend(bezier_points((57, 42), (59, 52), (62, 48), (64, 34)))
        red_curves.extend(bezier_points((64, 34), (66, 26), (67, 30), (67, 50)))
        red_curves.extend(bezier_points((67, 50), (67, 72), (67, 85), (67, 93)))
        draw.polygon(red_curves, fill=(225, 42, 20, 255))

        # Layer 2: Mid Fiery Orange Flame
        orange_curves = [(5, 93)]
        orange_curves.extend(bezier_points((5, 93), (6, 75), (5, 55), (7, 42)))
        orange_curves.extend(bezier_points((7, 42), (9, 34), (12, 36), (12, 46)))
        orange_curves.extend(bezier_points((12, 46), (14, 58), (17, 60), (19, 50)))
        orange_curves.extend(bezier_points((19, 50), (21, 38), (26, 36), (28, 46)))
        orange_curves.extend(bezier_points((28, 46), (30, 56), (33, 56), (35, 44)))
        orange_curves.extend(bezier_points((35, 44), (37, 32), (43, 30), (45, 44)))
        orange_curves.extend(bezier_points((45, 44), (47, 56), (50, 56), (52, 46)))
        orange_curves.extend(bezier_points((52, 46), (54, 36), (59, 38), (60, 50)))
        orange_curves.extend(bezier_points((60, 50), (62, 60), (64, 55), (65, 42)))
        orange_curves.extend(bezier_points((65, 42), (66, 36), (66, 50), (65, 93)))
        draw.polygon(orange_curves, fill=(255, 115, 25, 255))

        # Layer 3: Core Luminous Golden-Yellow Flame
        yellow_curves = [(8, 93)]
        yellow_curves.extend(bezier_points((8, 93), (9, 78), (8, 65), (10, 52)))
        yellow_curves.extend(bezier_points((10, 52), (12, 45), (15, 47), (16, 56)))
        yellow_curves.extend(bezier_points((16, 56), (18, 68), (21, 68), (23, 58)))
        yellow_curves.extend(bezier_points((23, 58), (25, 48), (30, 46), (32, 56)))
        yellow_curves.extend(bezier_points((32, 56), (34, 64), (37, 64), (39, 52)))
        yellow_curves.extend(bezier_points((39, 52), (41, 42), (46, 40), (48, 54)))
        yellow_curves.extend(bezier_points((48, 54), (50, 64), (53, 64), (55, 56)))
        yellow_curves.extend(bezier_points((55, 56), (57, 48), (61, 48), (62, 58)))
        yellow_curves.extend(bezier_points((62, 58), (63, 68), (63, 80), (62, 93)))
        draw.polygon(yellow_curves, fill=(255, 215, 45, 255))

        # Layer 4: White-Hot Smooth Rounded Cores
        white_core_1 = bezier_points((32, 85), (34, 66), (42, 64), (44, 85))
        draw.polygon([(32, 85)] + white_core_1 + [(44, 85)], fill=(255, 250, 195, 255))

        # Soft glowing rounded tongue crests
        tips = [(26, 48), (38, 44), (49, 46), (12, 48), (59, 50)]
        for tx, ty in tips:
            draw.ellipse([tx - 1, ty - 1, tx + 2, ty + 2], fill=(255, 250, 195, 255))

        # Floating glowing embers & sparks
        embers = [
            (6, 18), (11, 14), (64, 18), (59, 14),
            (22, 20), (48, 18), (35, 15), (28, 12), (42, 10),
            (16, 26), (54, 24), (20, 32), (50, 30)
        ]
        for ex, ey in embers:
            draw.point((ex, ey), fill=(255, 240, 120, 255))
            draw.point((ex, ey + 1), fill=(255, 130, 30, 255))

        # JOKER text in crisp clean white as requested
        text_color = (255, 255, 255, 255)

    # Chili Pepper Colors
    C_RED_DARK = (150, 14, 14, 255)
    C_RED_MID = (235, 32, 28, 255)
    C_RED_BRIGHT = (255, 75, 55, 255)
    C_RED_HL = (255, 185, 175, 255)
    C_STEM_MID = (55, 170, 85, 255)
    C_STEM_HL = (140, 235, 155, 255)
    C_WHITE = PALETTE["CARD_WHITE"]

    # Drop shadow beneath the pepper
    draw.ellipse([18, 64, 54, 76], fill=(30, 8, 8, 180))

    # Curving chili body polygon
    chili_outer = [
        (43, 34), (48, 32), (51, 36),
        (52, 44), (49, 54), (42, 63), (34, 69), (26, 72),
        (20, 72), (18, 70), (19, 67),
        (25, 63), (32, 56), (37, 47), (39, 40)
    ]
    draw.polygon(chili_outer, fill=C_RED_MID, outline=C_OUTLINE)

    # Inner shade / 3D volume
    chili_shade = [
        (20, 70), (26, 72), (34, 69), (42, 63), (49, 54), (46, 57), (38, 65), (30, 69), (22, 69)
    ]
    draw.polygon(chili_shade, fill=C_RED_DARK)

    # Highlight ridge along upper curve
    draw.polygon([(41, 38), (46, 40), (48, 48), (43, 57), (36, 63), (33, 59), (40, 53), (43, 46)], fill=C_RED_BRIGHT)
    # Glossy shine streak
    draw.line([(45, 40), (47, 47)], fill=C_RED_HL, width=2)
    draw.line([(44, 48), (40, 56)], fill=C_RED_HL, width=2)
    draw.point((45, 42), fill=C_WHITE)
    draw.point((46, 43), fill=C_WHITE)

    # Green Calyx / Cap
    calyx_pts = [(39, 34), (45, 39), (49, 33), (54, 37), (51, 31), (41, 30)]
    draw.polygon(calyx_pts, fill=C_STEM_MID, outline=C_OUTLINE)
    draw.point((46, 34), fill=C_STEM_HL)

    # Curving green stem
    stem_pts = [(46, 30), (48, 24), (54, 20), (56, 21), (51, 26), (48, 30)]
    draw.polygon(stem_pts, fill=C_STEM_MID, outline=C_OUTLINE)
    draw.line([(48, 24), (53, 21)], fill=C_STEM_HL, width=1)

    draw_vertical_joker_text(img, text_color, top_left=True, bottom_right=True)
    export_sprite(img, "j_hot_pepper.png")

def build_j_the_scythe():
    """Builds The Scythe Joker (71x95 px, 142x190 2x) - Menacing curved reaper scythe slicing two outer cards while middle card duplicates."""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    C_OUTLINE = (20, 24, 28, 255)
    C_BG = (24, 28, 36, 255) # Gothic midnight indigo slate
    draw.rectangle([1, 1, 69, 93], fill=C_BG)

    # Background subtle spectral mist & reaping arc
    C_MIST = (38, 62, 74, 255)
    C_SPECTRAL = (54, 180, 160, 255)
    C_SPECTRAL_GLOW = (30, 120, 110, 180)
    C_WHITE = PALETTE["CARD_WHITE"]

    # Swirling mist in bottom half
    draw.ellipse([10, 55, 60, 90], fill=C_MIST)
    draw.arc([16, 12, 60, 56], start=180, end=330, fill=C_SPECTRAL_GLOW, width=3)

    # 1. Three mini cards at bottom: Left sliced, Middle whole & glowing, Right sliced
    # Middle Card (Whole & Glowing with cyan aura)
    draw.rectangle([31, 64, 39, 76], fill=C_SPECTRAL_GLOW)
    draw.rectangle([32, 65, 38, 75], fill=(245, 245, 240, 255), outline=C_OUTLINE)
    draw.line([(34, 67), (36, 67)], fill=(200, 40, 40, 255))
    draw.point((35, 71), fill=(200, 40, 40, 255))
    draw.point((35, 63), fill=C_SPECTRAL)

    # Left Card (Sliced in two)
    draw.polygon([(20, 70), (26, 68), (24, 73), (19, 75)], fill=(220, 220, 215, 255), outline=C_OUTLINE)
    draw.polygon([(22, 76), (27, 74), (25, 80), (21, 80)], fill=(180, 180, 175, 255), outline=C_OUTLINE)
    draw.point((26, 70), fill=(240, 80, 80, 255))

    # Right Card (Sliced in two)
    draw.polygon([(44, 69), (50, 71), (49, 76), (43, 74)], fill=(220, 220, 215, 255), outline=C_OUTLINE)
    draw.polygon([(45, 77), (51, 79), (49, 81), (44, 80)], fill=(180, 180, 175, 255), outline=C_OUTLINE)
    draw.point((45, 71), fill=(240, 80, 80, 255))

    # 2. Scythe Wooden Snath (Shaft)
    C_WOOD_MID = (95, 60, 32, 255)
    C_WOOD_HL = (145, 95, 52, 255)
    C_IRON = (50, 58, 65, 255)
    C_STEEL = (175, 195, 210, 255)
    C_STEEL_HL = (235, 245, 255, 255)

    # Curved shaft from (52, 86) up to (22, 26)
    draw.line([(52, 86), (42, 60), (32, 40), (22, 26)], fill=C_OUTLINE, width=4)
    draw.line([(52, 86), (42, 60), (32, 40), (22, 26)], fill=C_WOOD_MID, width=2)
    draw.line([(51, 85), (41, 59), (31, 39), (21, 25)], fill=C_WOOD_HL, width=1)

    # Grips
    draw.line([(45, 64), (49, 61)], fill=C_WOOD_HL, width=2)
    draw.line([(34, 45), (38, 42)], fill=C_WOOD_HL, width=2)

    # Collar/Mount at top of shaft
    draw.rectangle([20, 24, 24, 28], fill=C_IRON, outline=C_OUTLINE)

    # 3. Giant Curved Scythe Blade
    blade_pts = [
        (21, 26), (23, 20), (28, 15), (36, 12), (44, 14), (52, 20),
        (46, 22), (38, 20), (30, 23), (24, 30), (21, 32)
    ]
    draw.polygon(blade_pts, fill=C_IRON, outline=C_OUTLINE)

    blade_bevel = [
        (23, 24), (28, 18), (36, 15), (43, 17), (51, 20),
        (46, 22), (38, 20), (30, 23), (24, 30)
    ]
    draw.polygon(blade_bevel, fill=C_STEEL)

    # Razor cutting edge & spectral sheen line
    edge_pts = [(24, 30), (30, 23), (38, 20), (46, 22), (52, 20)]
    draw.line(edge_pts, fill=C_STEEL_HL, width=1)
    draw.line([(34, 18), (48, 21)], fill=C_SPECTRAL, width=1)
    draw.point((52, 20), fill=C_WHITE)

    # Spectral death particles
    particles = [(53, 18), (48, 14), (38, 10), (28, 12), (18, 22), (36, 26), (46, 28)]
    for px, py in particles:
        draw.point((px, py), fill=C_SPECTRAL)
        draw.point((px + 1, py), fill=C_WHITE)

    draw_vertical_joker_text(img, PALETTE["CARD_WHITE"], top_left=True, bottom_right=True)
    export_sprite(img, "j_the_scythe.png")

def create_voucher_ticket_base(bg_color, outline_color, inner_border_color=None):
    """Creates authentic Balatro voucher ticket with top, bottom, and side semicircular notch holes."""
    mask_path = "tools/voucher_ticket_mask.png"
    if os.path.exists(mask_path):
        mask = Image.open(mask_path)
    else:
        mask = Image.open("tools/scratch/vanilla_voucher_alpha_mask.png")

    img = Image.new("RGBA", (71, 95), (0, 0, 0, 0))

    # Fill base and outline based on the exact vanilla mask
    for y in range(95):
        for x in range(71):
            if mask.getpixel((x, y)) > 0:
                is_edge = False
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if nx < 0 or nx >= 71 or ny < 0 or ny >= 95 or mask.getpixel((nx, ny)) == 0:
                        is_edge = True
                        break
                if is_edge:
                    img.putpixel((x, y), outline_color)
                else:
                    img.putpixel((x, y), bg_color)

    draw = ImageDraw.Draw(img)

    # Inner decorative border if requested (contouring around top & bottom holes)
    if inner_border_color:
        inner_poly = [
            (10, 4), (28, 4), (28, 8), (30, 10), (40, 10), (42, 8), (42, 4), (60, 4),
            (61, 5), (61, 17),
            (60, 18), (59, 20), (60, 22),
            (61, 23), (61, 89),
            (60, 90), (42, 90), (42, 86), (40, 84), (30, 84), (28, 86), (28, 90), (10, 90),
            (9, 89), (9, 23),
            (10, 22), (11, 20), (10, 18),
            (9, 17), (9, 5)
        ]
        draw.polygon(inner_poly, outline=inner_border_color)

    # Perforation dotted line across y=20
    for x in range(12, 59, 3):
        draw.point((x, 20), fill=outline_color)

    return img

def build_v_market():
    """Builds Market Voucher with exact authentic Balatro top & bottom semicircular notch holes."""
    C_OUTLINE = (42, 34, 26, 255)
    C_BG = (248, 242, 228, 255)
    C_INNER = (215, 195, 160, 255)
    C_RED_STALL = (220, 50, 45, 255)
    C_WHITE_STALL = (255, 252, 245, 255)
    C_WOOD = (165, 115, 55, 255)
    C_WOOD_DARK = (115, 75, 30, 255)
    C_BASKET = (195, 140, 65, 255)
    C_BASKET_DARK = (135, 90, 40, 255)
    C_GOLD = (245, 195, 50, 255)
    C_GOLD_HL = (255, 230, 110, 255)

    img = create_voucher_ticket_base(C_BG, C_OUTLINE, C_INNER)
    draw = ImageDraw.Draw(img)

    # Header banner (y=10 to 18, below top semicircular hole)
    draw.rectangle([16, 10, 54, 18], fill=(45, 125, 80, 255), outline=C_OUTLINE)
    draw.line([(17, 11), (53, 11)], fill=(110, 195, 145, 255))
    draw.point((20, 14), fill=C_GOLD)
    draw.point((50, 14), fill=C_GOLD)
    draw.line([(26, 14), (44, 14)], fill=C_WHITE_STALL)

    # 1. Market Awning Canopy (Striped red and white, y=25 to 39)
    draw.polygon([(14, 39), (56, 39), (53, 43), (17, 43)], fill=(180, 165, 140, 180))

    stripes = [
        ((14, 25, 20, 38), C_RED_STALL),
        ((20, 25, 26, 38), C_WHITE_STALL),
        ((26, 25, 32, 38), C_RED_STALL),
        ((32, 25, 38, 38), C_WHITE_STALL),
        ((38, 25, 44, 38), C_RED_STALL),
        ((44, 25, 50, 38), C_WHITE_STALL),
        ((50, 25, 56, 38), C_RED_STALL)
    ]
    for (x1, y1, x2, y2), col in stripes:
        draw.rectangle([x1, y1, x2, y2], fill=col)

    draw.line([(14, 25), (56, 25)], fill=C_OUTLINE, width=1)
    draw.line([(14, 38), (56, 38)], fill=C_OUTLINE, width=1)
    draw.line([(14, 25), (14, 38)], fill=C_OUTLINE, width=1)
    draw.line([(56, 25), (56, 38)], fill=C_OUTLINE, width=1)
    for sc in range(14, 56, 6):
        draw.arc([sc, 36, sc + 6, 42], start=0, end=180, fill=C_OUTLINE)

    # Support posts
    draw.line([(16, 39), (16, 73)], fill=C_WOOD, width=2)
    draw.line([(15, 39), (15, 73)], fill=C_WOOD_DARK, width=1)
    draw.line([(54, 39), (54, 73)], fill=C_WOOD, width=2)
    draw.line([(55, 39), (55, 73)], fill=C_WOOD_DARK, width=1)

    # 2. Booster Packs Peeking Out
    # Celestial Pack (Left)
    celestial_pts = [(20, 47), (28, 43), (32, 59), (24, 63)]
    draw.polygon(celestial_pts, fill=(28, 42, 95, 255), outline=C_OUTLINE)
    draw.point((25, 52), fill=(100, 220, 255, 255))
    draw.point((26, 53), fill=C_GOLD)

    # Arcana Pack (Right)
    arcana_pts = [(38, 43), (48, 47), (44, 63), (34, 59)]
    draw.polygon(arcana_pts, fill=(115, 42, 130, 255), outline=C_OUTLINE)
    draw.point((42, 52), fill=(255, 220, 90, 255))
    draw.point((43, 53), fill=(255, 255, 255, 255))

    # Center Buffoon Pack
    draw.rectangle([27, 42, 43, 61], fill=(225, 40, 40, 255), outline=C_OUTLINE)
    draw.rectangle([30, 45, 40, 58], fill=(255, 70, 60, 255))
    draw.polygon([(35, 47), (39, 51), (35, 55), (31, 51)], fill=C_GOLD, outline=C_OUTLINE)
    draw.point((35, 51), fill=C_GOLD_HL)

    # 3. Wicker Basket
    basket_pts = [(19, 55), (51, 55), (47, 74), (23, 74)]
    draw.polygon(basket_pts, fill=C_BASKET, outline=C_OUTLINE)
    for y in range(58, 73, 4):
        draw.line([(21, y), (49, y)], fill=C_BASKET_DARK)
    for x in range(23, 48, 5):
        draw.line([(x, 56), (x - 2, 73)], fill=C_BASKET_DARK)

    # 4. Golden Wax Seal (+1 PACK)
    draw.ellipse([30, 69, 40, 79], fill=C_GOLD, outline=C_OUTLINE)
    draw.point((35, 74), fill=(60, 40, 10, 255))
    draw.line([(33, 74), (37, 74)], fill=C_OUTLINE)
    draw.line([(35, 72), (35, 76)], fill=C_OUTLINE)

    sparkles = [(14, 50), (56, 48), (35, 36), (17, 76), (53, 76)]
    for sx, sy in sparkles:
        draw.point((sx, sy), fill=C_GOLD_HL)
        draw.point((sx, sy + 1), fill=C_GOLD)

    # Bottom Banner label (y=80 to 85, above bottom hole)
    draw.rectangle([15, 80, 55, 85], fill=(235, 222, 195, 255), outline=C_OUTLINE)
    draw.line([(19, 82), (51, 82)], fill=(120, 85, 45, 255))

    export_sprite(img, "v_market.png")
    return img

def build_v_supermarket():
    """Builds Supermarket Voucher with exact authentic Balatro top & bottom semicircular notch holes."""
    C_OUTLINE = (20, 18, 30, 255)
    C_BG = (24, 28, 44, 255)
    C_INNER = (240, 195, 60, 255)
    C_NEON_CYAN = (0, 235, 255, 255)
    C_NEON_PINK = (255, 55, 175, 255)
    C_CHROME = (215, 225, 240, 255)
    C_CHROME_DARK = (120, 135, 160, 255)
    C_GOLD = (250, 205, 55, 255)
    C_GOLD_HL = (255, 245, 140, 255)
    C_WHITE = PALETTE["CARD_WHITE"]

    img = create_voucher_ticket_base(C_BG, C_OUTLINE, C_INNER)
    draw = ImageDraw.Draw(img)

    # Top Marquee Sign (y=10 to 18, below top hole)
    draw.rectangle([14, 10, 56, 18], fill=(12, 14, 24, 255), outline=C_OUTLINE)
    draw.line([(15, 11), (55, 11)], fill=C_NEON_CYAN)
    draw.line([(15, 17), (55, 17)], fill=C_NEON_PINK)
    draw.line([(22, 14), (48, 14)], fill=C_WHITE, width=2)
    draw.point((17, 14), fill=C_NEON_PINK)
    draw.point((53, 14), fill=C_NEON_CYAN)

    # Golden Laurel Wreath
    laurel_left = [(14, 32), (12, 40), (13, 50), (15, 60), (18, 68), (22, 73)]
    for lx, ly in laurel_left:
        draw.polygon([(lx, ly), (lx + 3, ly - 2), (lx + 4, ly + 2)], fill=C_GOLD, outline=C_OUTLINE)
    laurel_right = [(56, 32), (58, 40), (57, 50), (55, 60), (52, 68), (48, 73)]
    for rx, ry in laurel_right:
        draw.polygon([(rx, ry), (rx - 3, ry - 2), (rx - 4, ry + 2)], fill=C_GOLD, outline=C_OUTLINE)

    # Cart Body
    cart_poly = [
        (21, 37), (49, 37),
        (46, 55), (25, 55)
    ]
    draw.polygon(cart_poly, fill=(35, 45, 65, 255), outline=C_OUTLINE)

    for y in range(40, 55, 4):
        draw.line([(23, y), (47, y)], fill=C_CHROME)
    for x in range(25, 46, 5):
        draw.line([(x, 37), (x - 1, 55)], fill=C_CHROME_DARK)

    draw.line([(17, 35), (22, 39)], fill=C_CHROME, width=2)
    draw.line([(17, 34), (20, 34)], fill=C_NEON_PINK, width=2)
    draw.line([(26, 55), (24, 65)], fill=C_CHROME, width=2)
    draw.line([(44, 55), (46, 65)], fill=C_CHROME, width=2)
    draw.line([(23, 65), (47, 65)], fill=C_CHROME, width=2)
    draw.ellipse([21, 63, 26, 68], fill=(20, 20, 25, 255), outline=C_CHROME)
    draw.ellipse([44, 63, 49, 68], fill=(20, 20, 25, 255), outline=C_CHROME)

    # Overflowing Vouchers & Golden Passes
    draw.polygon([(26, 29), (36, 25), (38, 39), (28, 43)], fill=C_GOLD, outline=C_OUTLINE)
    draw.point((31, 33), fill=C_WHITE)
    draw.polygon([(34, 26), (44, 30), (41, 44), (31, 40)], fill=(225, 45, 65, 255), outline=C_OUTLINE)
    draw.line([(34, 34), (41, 37)], fill=C_WHITE)
    draw.polygon([(28, 35), (42, 33), (44, 45), (30, 47)], fill=C_NEON_CYAN, outline=C_OUTLINE)
    draw.point((36, 39), fill=C_WHITE)

    # Golden Seal (y=69 to 79)
    draw.ellipse([30, 69, 40, 79], fill=C_GOLD, outline=C_OUTLINE)
    draw.point((35, 71), fill=C_WHITE)
    draw.line([(33, 74), (37, 74)], fill=(60, 40, 10, 255))
    draw.line([(35, 72), (35, 76)], fill=(60, 40, 10, 255))

    draw.point((26, 74), fill=C_GOLD_HL)
    draw.point((44, 74), fill=C_GOLD_HL)

    sparkles = [(16, 25), (54, 25), (35, 21), (18, 54), (52, 54)]
    for sx, sy in sparkles:
        draw.point((sx, sy), fill=C_NEON_CYAN)
        draw.point((sx + 1, sy), fill=C_GOLD_HL)

    # Bottom Banner (y=80 to 85, above bottom hole)
    draw.rectangle([14, 80, 56, 85], fill=C_GOLD, outline=C_OUTLINE)
    draw.line([(17, 82), (53, 82)], fill=(50, 35, 10, 255), width=1)

    export_sprite(img, "v_supermarket.png")
    return img

def build_j_antivirus():
    """Builds Antivirus Joker (71x95 px, 142x190 2x) - Titanium Security Shield with Jester Cap & Quarantined Bug."""
    img = create_card_base()
    draw = ImageDraw.Draw(img)

    C_OUTLINE = PALETTE["DEEP_OUTLINE"]
    C_PAPER_SHADOW = PALETTE["PAPER_SHADOW"]
    C_GRID_FAINT = (232, 242, 238, 255)

    C_TITANIUM_HL = (245, 250, 255, 255)
    C_TITANIUM = (195, 208, 220, 255)
    C_TITANIUM_SH = (130, 145, 160, 255)
    C_TITANIUM_DARK = (75, 88, 102, 255)

    C_CYBER_DARK = (14, 38, 28, 255)
    C_CYBER_MID = (24, 72, 48, 255)
    C_CYBER_BRIGHT = (45, 185, 95, 255)
    C_CYBER_NEON = (80, 255, 140, 255)
    C_CYBER_SCAN = (35, 120, 75, 255)

    C_CAP_CYAN = (30, 135, 215, 255)
    C_CAP_CYAN_HL = (85, 185, 255, 255)
    C_CAP_CYAN_SH = (18, 80, 140, 255)
    C_CAP_GREEN = (25, 160, 80, 255)
    C_CAP_GREEN_HL = (70, 215, 120, 255)
    C_CAP_GREEN_SH = (15, 95, 50, 255)
    C_GOLD = PALETTE["GOLD_YELLOW"]
    C_GOLD_HL = PALETTE["GOLD_HL"]

    C_BUG_DARK = (130, 20, 35, 255)
    C_BUG_RED = (225, 45, 60, 255)
    C_BUG_HL = (255, 110, 125, 255)
    C_BUG_EYE = (255, 245, 100, 255)

    # 1. Subtle digital circuit grid trace on card
    for y in range(5, 90, 8):
        for x in range(5, 66):
            if (x + y) % 4 == 0:
                img.putpixel((x, y), C_GRID_FAINT)
    for x in range(9, 65, 8):
        for y in range(5, 90):
            if (x + y) % 4 == 0:
                img.putpixel((x, y), C_GRID_FAINT)

    # 2. Table shadow under shield
    draw.ellipse([18, 72, 53, 85], fill=C_PAPER_SHADOW)

    # 3. Shield silhouette & beveled metal frame (x: 18..52, y: 30..77)
    for y in range(30, 78):
        if y <= 54:
            x_min = 18
            x_max = 52
        else:
            t = (y - 54) / 23.0
            x_min = int(round(18 + t * t * (35 - 18)))
            x_max = int(round(52 - t * t * (52 - 35)))

        for x in range(x_min, x_max + 1):
            dist_left = x - x_min
            dist_right = x_max - x
            dist_top = y - 30
            dist_bottom = 77 - y
            edge_dist = min(dist_left, dist_right, dist_top, dist_bottom)

            if edge_dist == 0:
                img.putpixel((x, y), C_OUTLINE)
            elif edge_dist == 1:
                if x < 35 and y < 60:
                    img.putpixel((x, y), C_TITANIUM_HL)
                else:
                    img.putpixel((x, y), C_TITANIUM_SH)
            elif edge_dist == 2:
                img.putpixel((x, y), C_TITANIUM)
            elif edge_dist == 3:
                img.putpixel((x, y), C_TITANIUM_DARK)
            else:
                if y % 2 == 0:
                    img.putpixel((x, y), C_CYBER_DARK)
                else:
                    img.putpixel((x, y), C_CYBER_MID)

    # 4. Radar scan circles & crosshairs on shield face
    cx, cy = 35, 52
    draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], outline=C_CYBER_SCAN)
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], outline=C_CYBER_SCAN)
    draw.line([(cx - 13, cy), (cx + 13, cy)], fill=C_CYBER_SCAN)
    draw.line([(cx, cy - 13), (cx, cy + 13)], fill=C_CYBER_SCAN)

    # Radar sweeping beam
    draw.line([(cx, cy), (cx + 10, cy - 8)], fill=C_CYBER_BRIGHT)
    draw.line([(cx, cy), (cx + 11, cy - 6)], fill=C_CYBER_BRIGHT)
    draw.line([(cx, cy), (cx + 9, cy - 10)], fill=C_CYBER_SCAN)

    # 5. Quarantined Red Virus Bug in Center
    bx, by = 35, 52
    legs = [
        (bx - 5, by - 3), (bx - 6, by - 4),
        (bx + 5, by - 3), (bx + 6, by - 4),
        (bx - 5, by + 1), (bx - 7, by + 2),
        (bx + 5, by + 1), (bx + 7, by + 2),
        (bx - 4, by + 4), (bx - 6, by + 6),
        (bx + 4, by + 4), (bx + 6, by + 6),
    ]
    for lx, ly in legs:
        img.putpixel((lx, ly), C_BUG_DARK)

    draw.line([(bx - 2, by - 4), (bx - 4, by - 7)], fill=C_BUG_RED)
    img.putpixel((bx - 5, by - 8), C_BUG_HL)
    draw.line([(bx + 2, by - 4), (bx + 4, by - 7)], fill=C_BUG_RED)
    img.putpixel((bx + 5, by - 8), C_BUG_HL)

    draw.ellipse([bx - 4, by - 3, bx + 4, by + 4], fill=C_BUG_RED, outline=C_BUG_DARK)
    draw.ellipse([bx - 2, by - 2, bx + 2, by + 1], fill=C_BUG_HL)
    img.putpixel((bx - 2, by - 1), C_BUG_EYE)
    img.putpixel((bx + 2, by - 1), C_BUG_EYE)

    # Quarantine lock brackets
    draw.line([(bx - 9, by - 8), (bx - 6, by - 8)], fill=C_CYBER_NEON)
    draw.line([(bx - 9, by - 8), (bx - 9, by - 5)], fill=C_CYBER_NEON)
    draw.line([(bx + 9, by - 8), (bx + 6, by - 8)], fill=C_CYBER_NEON)
    draw.line([(bx + 9, by - 8), (bx + 9, by - 5)], fill=C_CYBER_NEON)
    draw.line([(bx - 9, by + 8), (bx - 6, by + 8)], fill=C_CYBER_NEON)
    draw.line([(bx - 9, by + 8), (bx - 9, by + 5)], fill=C_CYBER_NEON)
    draw.line([(bx + 9, by + 8), (bx + 6, by + 8)], fill=C_CYBER_NEON)
    draw.line([(bx + 9, by + 8), (bx + 9, by + 5)], fill=C_CYBER_NEON)

    # Diagonal slash barrier
    draw.ellipse([bx - 8, by - 8, bx + 8, by + 8], outline=C_CYBER_NEON)
    draw.line([(bx - 5, by + 5), (bx + 5, by - 5)], fill=C_CYBER_NEON)

    # 6. Jester Hat atop Shield
    draw.polygon([(30, 30), (35, 12), (40, 30)], fill=C_CAP_GREEN, outline=C_OUTLINE)
    draw.line([(31, 28), (35, 14)], fill=C_CAP_GREEN_HL)
    draw.line([(39, 28), (36, 14)], fill=C_CAP_GREEN_SH)
    draw.ellipse([33, 9, 37, 13], fill=C_GOLD, outline=C_OUTLINE)
    img.putpixel((34, 10), C_GOLD_HL)

    draw.polygon([(20, 30), (28, 30), (19, 18), (14, 23)], fill=C_CAP_CYAN, outline=C_OUTLINE)
    draw.line([(22, 28), (16, 22)], fill=C_CAP_CYAN_HL)
    draw.ellipse([11, 21, 15, 25], fill=C_GOLD, outline=C_OUTLINE)
    img.putpixel((12, 22), C_GOLD_HL)

    draw.polygon([(42, 30), (50, 30), (56, 23), (51, 18)], fill=C_CAP_CYAN, outline=C_OUTLINE)
    draw.line([(48, 28), (54, 22)], fill=C_CAP_CYAN_SH)
    draw.ellipse([55, 21, 59, 25], fill=C_GOLD, outline=C_OUTLINE)
    img.putpixel((56, 22), C_GOLD_HL)

    # Collar bells
    draw.ellipse([27, 28, 31, 32], fill=C_GOLD, outline=C_OUTLINE)
    draw.ellipse([39, 28, 43, 32], fill=C_GOLD, outline=C_OUTLINE)

    # Status LED at top of shield
    draw.ellipse([33, 33, 37, 37], fill=C_CYBER_DARK, outline=C_OUTLINE)
    img.putpixel((35, 35), C_CYBER_NEON)
    img.putpixel((34, 35), C_CYBER_BRIGHT)
    img.putpixel((36, 35), C_CYBER_BRIGHT)

    # Clean Checkmark emblem
    draw.polygon([(31, 65), (35, 63), (39, 65), (35, 71)], fill=C_CYBER_BRIGHT, outline=C_OUTLINE)
    draw.line([(33, 67), (35, 69)], fill=C_TITANIUM_HL)
    draw.line([(35, 69), (38, 65)], fill=C_TITANIUM_HL)

    # 7. Authentic vertical JOKER text in cyber teal
    draw_vertical_joker_text(img, (45, 110, 100, 255), top_left=True, bottom_right=True)

    export_sprite(img, "j_antivirus.png")
    return img

def build_j_sommers():
    """
    Builds Legendary Joker 'Sommers' sprite sheet (71x190, 2x 142x380) following vanilla Legendary Joker anatomy:
    - Row 0 (0..94): Authentic Localthunk wavy marbled background mapped to luminous Cyan,
      with the vanilla cream plaque at the bottom reading 'SOMMERS'.
    - Row 1 (95..189): Floating soul layer (transparent background) of Will Sommers:
      Tudor jester cowl with cyan and navy horns, golden bells, knowing Renaissance jester face,
      ornate scalloped mantle, floating Blue Seal (left) and floating Red Seal (right).
    """
    sheet = Image.new("RGBA", (71, 190), (0, 0, 0, 0))

    # --- ROW 0: CARD BASE (0, 0) -> 71x95 ---
    # Load vanilla legendary base template
    template_path = os.path.join(BASE_DIR, "tools", "scratch", "chicot_bg.png")
    if os.path.exists(template_path):
        chicot = Image.open(template_path)
    else:
        # Fallback to jokers sheet if scratch not present
        with zipfile.ZipFile("D:/GG/Balatro.v1.0.1o/game/Balatro.exe", "r") as z:
            data = z.read("resources/textures/1x/Jokers.png")
            j_sheet = Image.open(io.BytesIO(data))
            chicot = j_sheet.crop((6 * 71, 8 * 95, 7 * 71, 9 * 95))

    base_img = Image.new("RGBA", (71, 95), (0, 0, 0, 0))

    # Complete 8-tone Localthunk marble wave mapping to luminous cyan
    CYAN_PALETTE = {
        (177, 134, 164, 255): (15, 95, 145, 255),    # Deepest boundary cyan
        (185, 151, 184, 255): (20, 115, 165, 255),   # Deep cyan wave
        (200, 134, 135, 255): (35, 135, 185, 255),   # Low cyan wave
        (200, 164, 193, 255): (55, 160, 210, 255),   # Mid-low cyan wave
        (217, 173, 200, 255): (75, 180, 225, 255),   # Mid cyan wave
        (238, 143, 141, 255): (110, 205, 240, 255),  # Bright cyan wave
        (244, 180, 178, 255): (155, 225, 248, 255),  # High crest cyan
        (253, 223, 221, 255): (215, 248, 255, 255),  # Pure icy white-cyan highlight
    }

    # Cyan gradient mapping
    for y in range(95):
        for x in range(71):
            p = chicot.getpixel((x, y))
            if p[3] == 0:
                continue

            # Plaque region: strictly y=78..87 and x=8..62
            is_plaque = (78 <= y <= 87 and 8 <= x <= 62)
            if is_plaque:
                # Clear existing dark text from template inside the name area
                if 80 <= y <= 84 and 15 <= x <= 55 and p[0] < 120 and p[1] < 120 and p[2] < 120:
                    base_img.putpixel((x, y), (247, 241, 228, 255))
                else:
                    base_img.putpixel((x, y), p) # retain authentic cream plaque, bevels, and drop shadow
            elif p in CYAN_PALETTE:
                base_img.putpixel((x, y), CYAN_PALETTE[p])
            else:
                base_img.putpixel((x, y), (20, 115, 165, p[3]))

    # Draw SOMMERS on the plaque - perfectly centered horizontally and vertically
    C_TEXT = (42, 38, 48, 255)
    font_5px = {
        'S': [
            " ###",
            "#   ",
            " ## ",
            "   #",
            "### "
        ],
        'O': [
            " ## ",
            "#  #",
            "#  #",
            "#  #",
            " ## "
        ],
        'M': [
            "#   #",
            "## ##",
            "# # #",
            "#   #",
            "#   #"
        ],
        'E': [
            "####",
            "#   ",
            "### ",
            "#   ",
            "####"
        ],
        'R': [
            "### ",
            "#  #",
            "### ",
            "# # ",
            "#  #"
        ]
    }
    word = ['S', 'O', 'M', 'M', 'E', 'R', 'S']
    widths = [len(font_5px[ch][0]) for ch in word]
    total_w = sum(widths) + (len(word) - 1) # 36 px
    start_x = int(round(35.0 - total_w / 2.0)) # 17 -> spans 17..52
    start_y = 80 # spans 80..84 -> center 82.0 (matches vanilla Canio, Chicot, Yorick, Perkeo)

    cur_x = start_x
    for ch in word:
        grid = font_5px[ch]
        for row_idx, row in enumerate(grid):
            for col_idx, char in enumerate(row):
                if char == '#':
                    base_img.putpixel((cur_x + col_idx, start_y + row_idx), C_TEXT)
        cur_x += len(grid[0]) + 1

    sheet.paste(base_img, (0, 0))

    # --- ROW 1: FLOATING SOUL SPRITE (0, 95) ---
    soul_img = Image.new("RGBA", (71, 95), (0, 0, 0, 0))
    draw_soul = ImageDraw.Draw(soul_img)

    C_OUTLINE = (35, 30, 40, 255)
    C_FACE = (252, 245, 235, 255)
    C_FACE_SH = (225, 215, 200, 255)
    C_COWL_CYAN = (0, 165, 210, 255)
    C_COWL_CYAN_HL = (90, 225, 248, 255)
    C_COWL_NAVY = (28, 48, 85, 255)
    C_COWL_NAVY_HL = (45, 75, 130, 255)
    C_COWL_NAVY_SH = (15, 28, 52, 255)
    C_GOLD = PALETTE["GOLD_YELLOW"]
    C_GOLD_HL = PALETTE["GOLD_HL"]
    C_GOLD_SH = (160, 120, 30, 255)

    # 1. Hood Horns & Bells
    # Left horn
    draw_soul.polygon([(34, 20), (22, 12), (16, 18), (18, 26), (32, 25)], fill=C_COWL_CYAN, outline=C_OUTLINE)
    draw_soul.line([(22, 14), (17, 20)], fill=C_COWL_CYAN_HL)
    draw_soul.ellipse([12, 17, 18, 23], fill=C_GOLD, outline=C_OUTLINE)
    soul_img.putpixel((14, 19), C_GOLD_HL)

    # Right horn
    draw_soul.polygon([(36, 20), (48, 12), (54, 18), (52, 26), (38, 25)], fill=C_COWL_NAVY, outline=C_OUTLINE)
    draw_soul.line([(48, 14), (53, 20)], fill=C_COWL_NAVY_HL)
    draw_soul.ellipse([52, 17, 58, 23], fill=C_GOLD, outline=C_OUTLINE)
    soul_img.putpixel((54, 19), C_GOLD_HL)

    # Center peak
    draw_soul.polygon([(30, 22), (35, 14), (40, 22)], fill=C_COWL_CYAN_HL, outline=C_OUTLINE)
    draw_soul.ellipse([33, 11, 37, 15], fill=C_GOLD, outline=C_OUTLINE)
    soul_img.putpixel((34, 12), C_GOLD_HL)

    # 2. Head & Hood Silhouette
    draw_soul.ellipse([23, 16, 47, 44], fill=C_COWL_NAVY_SH, outline=C_OUTLINE)
    draw_soul.ellipse([25, 18, 45, 42], fill=C_COWL_CYAN)

    # 3. Face
    draw_soul.ellipse([27, 23, 43, 41], fill=C_FACE, outline=C_OUTLINE)
    draw_soul.arc([27, 23, 43, 41], start=45, end=135, fill=C_FACE_SH)

    # 4. Facial Features (Witty Renaissance Jester)
    draw_soul.line([(29, 28), (33, 27)], fill=C_GOLD_SH, width=1)
    draw_soul.line([(37, 27), (41, 28)], fill=C_GOLD_SH, width=1)
    soul_img.putpixel((31, 29), C_OUTLINE)
    soul_img.putpixel((39, 29), C_OUTLINE)
    soul_img.putpixel((35, 32), C_FACE_SH)
    soul_img.putpixel((35, 33), C_OUTLINE)
    draw_soul.arc([32, 34, 38, 38], start=0, end=180, fill=C_OUTLINE)
    soul_img.putpixel((38, 35), C_OUTLINE)

    # 5. Scalloped Jester Mantle & Robe (y=43 to 72)
    draw_soul.polygon([(18, 70), (22, 50), (35, 46), (48, 50), (52, 70)], fill=C_COWL_NAVY, outline=C_OUTLINE)
    draw_soul.polygon([(22, 44), (28, 54), (35, 47)], fill=C_COWL_CYAN, outline=C_OUTLINE)
    draw_soul.polygon([(35, 47), (42, 54), (48, 44)], fill=C_COWL_CYAN_HL, outline=C_OUTLINE)
    draw_soul.ellipse([26, 53, 30, 57], fill=C_GOLD, outline=C_OUTLINE)
    draw_soul.ellipse([40, 53, 44, 57], fill=C_GOLD, outline=C_OUTLINE)
    draw_soul.ellipse([33, 48, 37, 52], fill=C_GOLD, outline=C_OUTLINE)

    draw_soul.line([(35, 52), (35, 70)], fill=C_GOLD, width=1)
    draw_soul.line([(34, 52), (34, 70)], fill=C_GOLD_HL, width=1)

    # 6. Floating Blue Seal (Left, y=44..60)
    bs_cx, bs_cy = 13, 50
    draw_soul.ellipse([bs_cx - 9, bs_cy - 9, bs_cx + 9, bs_cy + 9], fill=(0, 200, 255, 60))
    draw_soul.ellipse([bs_cx - 7, bs_cy - 7, bs_cx + 7, bs_cy + 7], fill=(0, 110, 230, 180), outline=(0, 240, 255, 255))
    draw_soul.ellipse([bs_cx - 5, bs_cy - 5, bs_cx + 5, bs_cy + 5], fill=(0, 140, 255, 255), outline=C_OUTLINE)
    soul_img.putpixel((bs_cx, bs_cy), (255, 255, 255, 255))
    soul_img.putpixel((bs_cx - 1, bs_cy), (180, 230, 255, 255))
    soul_img.putpixel((bs_cx + 1, bs_cy), (180, 230, 255, 255))
    soul_img.putpixel((bs_cx, bs_cy - 1), (180, 230, 255, 255))
    soul_img.putpixel((bs_cx, bs_cy + 1), (180, 230, 255, 255))

    # 7. Floating Red Seal (Right, y=44..60)
    rs_cx, rs_cy = 57, 50
    draw_soul.ellipse([rs_cx - 9, rs_cy - 9, rs_cx + 9, rs_cy + 9], fill=(255, 50, 80, 60))
    draw_soul.ellipse([rs_cx - 7, rs_cy - 7, rs_cx + 7, rs_cy + 7], fill=(210, 30, 50, 180), outline=(255, 120, 140, 255))
    draw_soul.ellipse([rs_cx - 5, rs_cy - 5, rs_cx + 5, rs_cy + 5], fill=(235, 45, 60, 255), outline=C_OUTLINE)
    soul_img.putpixel((rs_cx, rs_cy), (255, 255, 255, 255))
    soul_img.putpixel((rs_cx - 1, rs_cy), (255, 180, 190, 255))
    soul_img.putpixel((rs_cx + 1, rs_cy), (255, 180, 190, 255))
    soul_img.putpixel((rs_cx, rs_cy - 1), (255, 180, 190, 255))
    soul_img.putpixel((rs_cx, rs_cy + 1), (255, 180, 190, 255))

    sheet.paste(soul_img, (0, 95))

    export_sprite(sheet, "j_sommers.png")
    return sheet

def build_j_taxi_driver():
    """Builds Taxi Driver Joker (71x95 px, 142x190 2x) - Jimbo transformed into a classic NYC Taxi Driver.
    Starts directly from authentic vanilla Jimbo (j_joker), preserving his iconic jester face, eyes, and smile,
    with a yellow NYC cabbie flat cap (with black-and-white checkered band and golden taxi medallion),
    a rooftop illuminated TAXI sign, taxi-yellow driver uniform with checkered tie, and a driver steering wheel."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    vanilla_path = os.path.join(script_dir, "vanilla", "vanilla_jimbo.png")
    if os.path.exists(vanilla_path):
        base = Image.open(vanilla_path).convert("RGBA")
    else:
        sheet_path = os.path.join(os.path.dirname(script_dir), "PC _ Computer - Balatro - Jokers and Consumables - Jokers.png")
        sheet = Image.open(sheet_path).convert("RGBA")
        base = sheet.crop((0, 0, 71, 95))

    OUTLINE = (79, 99, 103, 255)
    SHADOW = (191, 199, 213, 255)
    BG = (255, 255, 255, 255)

    TAXI_YELLOW = (246, 196, 24, 255)
    TAXI_YELLOW_HL = (255, 230, 95, 255)
    TAXI_YELLOW_SH = (196, 138, 16, 255)

    CHECKER_BLACK = (60, 72, 75, 255)
    CHECKER_WHITE = (248, 248, 248, 255)

    GOLD = (253, 162, 0, 255)
    GOLD_HL = (255, 215, 60, 255)
    GOLD_SH = (180, 110, 0, 255)

    STEERING_GREY = (50, 60, 65, 255)
    STEERING_HL = (110, 125, 130, 255)

    img = base.copy()
    base_pixels = base.load()

    # 1. Clear out original jester bells and horns (above y=34, and sides x<23 or x>47 for y < 44)
    # Keeping Jimbo's exact face, eyes, nose, and smile untouched.
    for y in range(12, 44):
        for x in range(12, 60):
            is_face = False
            if y >= 37 and 24 <= x <= 47:
                r, g, b, a = base_pixels[x, y]
                # Keep face skin / eyes / nose (red cowl is replaced by cap flaps)
                if (r, g, b) not in [(253, 95, 85), (0, 156, 253), (0, 139, 227), (129, 206, 253)]:
                    is_face = True
            if not is_face:
                img.putpixel((x, y), BG)

    draw = ImageDraw.Draw(img)

    # 2. Taxi Rooftop Sign perched on top of cap (y=13..19, x=25..46)
    draw.rounded_rectangle([25, 13, 46, 19], radius=2, fill=TAXI_YELLOW, outline=OUTLINE)
    draw.line([(26, 14), (45, 14)], fill=TAXI_YELLOW_HL)
    draw.line([(26, 18), (45, 18)], fill=TAXI_YELLOW_SH)
    # Pixel text 'TAXI'
    # T
    draw.line([(27, 15), (29, 15)], fill=OUTLINE)
    draw.line([(28, 16), (28, 17)], fill=OUTLINE)
    # A
    draw.line([(31, 15), (33, 15)], fill=OUTLINE)
    draw.line([(31, 16), (31, 17)], fill=OUTLINE)
    draw.line([(33, 16), (33, 17)], fill=OUTLINE)
    draw.point((32, 16), fill=OUTLINE)
    # X
    draw.point((35, 15), fill=OUTLINE)
    draw.point((37, 15), fill=OUTLINE)
    draw.point((36, 16), fill=OUTLINE)
    draw.point((35, 17), fill=OUTLINE)
    draw.point((37, 17), fill=OUTLINE)
    # I
    draw.line([(39, 15), (41, 15)], fill=OUTLINE)
    draw.line([(40, 16), (40, 16)], fill=OUTLINE)
    draw.line([(39, 17), (41, 17)], fill=OUTLINE)
    # Side amber lights
    draw.point((24, 16), fill=GOLD)
    draw.point((47, 16), fill=GOLD)

    # Brackets connecting sign to cap at line 20
    draw.line([(28, 20), (29, 20)], fill=OUTLINE)
    draw.line([(42, 20), (43, 20)], fill=OUTLINE)

    # 3. Cabbie Cap Crown (y=21..33, x=18..53) - Newsboy / driver flat cap
    cap_points = [
        (26, 21), (45, 21),
        (51, 23), (53, 27), (53, 30),
        (52, 33), (19, 33),
        (18, 30), (18, 27), (20, 23)
    ]
    draw.polygon(cap_points, fill=TAXI_YELLOW, outline=OUTLINE)
    draw.line([(27, 22), (44, 22)], fill=TAXI_YELLOW_HL)
    draw.line([(23, 23), (48, 23)], fill=TAXI_YELLOW_HL)
    draw.line([(19, 29), (19, 32)], fill=TAXI_YELLOW_SH)
    draw.line([(52, 29), (52, 32)], fill=TAXI_YELLOW_SH)

    # 4. Checkerboard Band (y=29..32, x=19..52) - Iconic black & white taxi pattern
    for cx in range(19, 53):
        for cy in range(29, 33):
            block_x = (cx - 19) // 3
            block_y = (cy - 29)
            is_black = (block_x + block_y) % 2 == 0
            img.putpixel((cx, cy), CHECKER_BLACK if is_black else CHECKER_WHITE)
    draw.line([(18, 28), (53, 28)], fill=OUTLINE)
    draw.line([(18, 33), (53, 33)], fill=OUTLINE)
    draw.line([(18, 28), (18, 33)], fill=OUTLINE)
    draw.line([(53, 28), (53, 33)], fill=OUTLINE)

    # Golden taxi medallion badge in center (x=34..37, y=28..31)
    draw.rectangle([34, 28, 37, 31], fill=GOLD, outline=OUTLINE)
    draw.point((35, 29), fill=GOLD_HL)
    draw.point((36, 30), fill=GOLD_SH)

    # 5. Cap Visor / Peak (y=33..36, x=22..49)
    visor_points = [
        (22, 33), (49, 33),
        (47, 36), (24, 36)
    ]
    draw.polygon(visor_points, fill=TAXI_YELLOW_SH, outline=OUTLINE)
    draw.line([(25, 35), (46, 35)], fill=OUTLINE)

    # 6. Recolor Cowl along sides of face (y=37..52) to Taxi Yellow
    for y in range(37, 53):
        for x in range(18, 54):
            r, g, b, a = base_pixels[x, y]
            if (r, g, b) == (253, 95, 85): # Red cowl
                is_mouth = (47 <= y <= 52 and 26 <= x <= 45)
                if not is_mouth:
                    img.putpixel((x, y), TAXI_YELLOW if x > 30 else TAXI_YELLOW_SH)
            elif (r, g, b) in [(0, 156, 253), (0, 139, 227)]:
                img.putpixel((x, y), TAXI_YELLOW_SH)

    # 7. Recolor Jimbo's body (y=54..75) from blue to Taxi Yellow uniform
    for y in range(54, 76):
        for x in range(14, 58):
            r, g, b, a = base_pixels[x, y]
            if (r, g, b) in [(0, 156, 253), (129, 206, 253), (223, 242, 253)]:
                img.putpixel((x, y), TAXI_YELLOW)
            elif (r, g, b) == (0, 139, 227):
                img.putpixel((x, y), TAXI_YELLOW_SH)
            elif (r, g, b) == (253, 95, 85) and y >= 64:
                img.putpixel((x, y), TAXI_YELLOW_SH)

    # 8. Checkered Necktie (y=54..59, x=34..37)
    tie_pts = [(34, 54), (37, 54), (38, 58), (36, 60), (33, 58)]
    draw.polygon(tie_pts, fill=CHECKER_BLACK, outline=OUTLINE)
    for ty in range(55, 59):
        for tx in range(34, 38):
            if ((tx + ty) % 2 == 0):
                img.putpixel((tx, ty), CHECKER_WHITE)
    draw.polygon(tie_pts, outline=OUTLINE)

    # 9. Clean Pixel-Art Steering Wheel (y=58..68, x=24..47)
    # Top rim
    draw.line([(31, 58), (40, 58)], fill=OUTLINE)
    draw.line([(31, 59), (40, 59)], fill=STEERING_HL)

    # Upper curves
    draw.line([(28, 59), (30, 59)], fill=OUTLINE)
    draw.point((27, 60), fill=OUTLINE)
    draw.point((26, 61), fill=OUTLINE)
    draw.point((28, 60), fill=STEERING_HL)
    draw.point((27, 61), fill=STEERING_HL)

    draw.line([(41, 59), (43, 59)], fill=OUTLINE)
    draw.point((44, 60), fill=OUTLINE)
    draw.point((45, 61), fill=OUTLINE)
    draw.point((43, 60), fill=STEERING_HL)
    draw.point((44, 61), fill=STEERING_HL)

    # Vertical sides
    draw.line([(25, 61), (25, 65)], fill=OUTLINE)
    draw.line([(26, 62), (26, 65)], fill=STEERING_GREY)
    draw.line([(27, 62), (27, 65)], fill=OUTLINE)

    draw.line([(46, 61), (46, 65)], fill=OUTLINE)
    draw.line([(45, 62), (45, 65)], fill=STEERING_GREY)
    draw.line([(44, 62), (44, 65)], fill=OUTLINE)

    # Lower curves
    draw.point((26, 65), fill=OUTLINE)
    draw.point((27, 66), fill=OUTLINE)
    draw.line([(28, 67), (30, 67)], fill=OUTLINE)
    draw.point((28, 66), fill=STEERING_GREY)

    draw.point((45, 65), fill=OUTLINE)
    draw.point((44, 66), fill=OUTLINE)
    draw.line([(41, 67), (43, 67)], fill=OUTLINE)
    draw.point((43, 66), fill=STEERING_GREY)

    # Bottom rim
    draw.line([(31, 67), (40, 67)], fill=STEERING_GREY)
    draw.line([(31, 68), (40, 68)], fill=OUTLINE)

    # Center Horn Hub (medallion)
    draw.rectangle([34, 62, 37, 64], fill=GOLD, outline=OUTLINE)
    draw.point((35, 63), fill=GOLD_HL)

    # Spokes
    draw.line([(28, 63), (33, 63)], fill=OUTLINE)
    draw.line([(38, 63), (43, 63)], fill=OUTLINE)
    draw.line([(35, 65), (35, 66)], fill=OUTLINE)
    draw.line([(36, 65), (36, 66)], fill=OUTLINE)

    # Driver hands (white gloves) gripping the steering wheel at 10 and 2 o'clock
    draw.rounded_rectangle([23, 60, 26, 63], radius=1, fill=CHECKER_WHITE, outline=OUTLINE)
    draw.line([(24, 61), (24, 62)], fill=SHADOW)
    draw.rounded_rectangle([45, 60, 48, 63], radius=1, fill=CHECKER_WHITE, outline=OUTLINE)
    draw.line([(47, 61), (47, 62)], fill=SHADOW)

    export_sprite(img, "j_taxi_driver.png")

def build_j_river():
    """Builds River Joker (71x95 px, 142x190 2x) - Full-surface scenic landscape.
    Features a towering mountain range with multiple peaks and diagonal shadow hatching,
    golden sun with radiant sunburst rays and dots, flock of soaring birds,
    lush rolling green valley hills dotted with evergreen pine clusters,
    a vibrant winding river flowing continuously through the valley all the way to the bottom border,
    and authentic vertical 'JOKER' lettering on the margins."""
    w, h = 71, 95
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    C_OUTLINE = (30, 37, 40, 255)       # Deep slate outline
    C_SKY_TOP = (108, 172, 228, 255)    # Rich sky blue
    C_SKY_MID = (156, 204, 238, 255)    # Light sky blue
    C_SKY_BOT = (212, 235, 245, 255)    # Atmospheric warm horizon

    C_SUN_BODY = (255, 218, 68, 255)    # Golden sun
    C_SUN_HL   = (255, 242, 140, 255)   # Sun highlight
    C_SUN_OUT  = (220, 150, 30, 255)    # Sun outline / rays

    C_SNOW     = (250, 252, 255, 255)   # Crisp snow
    C_SNOW_SH  = (205, 220, 235, 255)   # Snow shadow
    C_ROCK_LGT = (185, 198, 212, 255)   # Sunlit granite
    C_ROCK_MID = (135, 150, 168, 255)   # Mid rock
    C_ROCK_DRK = (75, 88, 105, 255)     # Deep shadow rock
    C_ROCK_HATCH = (52, 62, 75, 255)    # Shadow hatching stripes
    C_RIDGE    = (40, 48, 58, 255)      # Ridge dividing line

    C_HILL_FAR = (95, 148, 115, 255)    # Distant hill
    C_HILL_LGT = (82, 185, 108, 255)    # Lush grass hill light
    C_HILL_MID = (55, 148, 85, 255)     # Lush grass hill mid
    C_HILL_SH  = (38, 105, 62, 255)     # Hill shadow / base
    C_MEADOW_FLAT = (68, 165, 96, 255)  # Valley meadow
    C_TREE     = (22, 58, 36, 255)      # Pine tree dark
    C_TREE_HL  = (40, 92, 55, 255)      # Pine tree highlight
    C_TREE_TRK = (45, 32, 22, 255)      # Tree trunk

    C_WATER_DP = (0, 107, 179, 255)     # Deep Balatro blue
    C_WATER_MD = (0, 156, 253, 255)     # Bright Balatro Chips blue
    C_WATER_LT = (120, 215, 255, 255)   # Light cyan water
    C_FOAM     = (255, 255, 255, 255)   # Foam white

    C_BIRD     = (45, 52, 60, 255)      # Soaring birds

    # 1. Sky background gradient
    for y in range(1, 94):
        for x in range(1, 70):
            if y < 16:
                col = C_SKY_TOP
            elif y < 28:
                t = (y - 16) / 12.0
                if (x + y) % 2 == 0 and t > 0.4:
                    col = C_SKY_MID
                elif t > 0.7:
                    col = C_SKY_MID
                else:
                    col = C_SKY_TOP
            elif y < 42:
                t = (y - 28) / 14.0
                if (x + y) % 2 == 0 and t > 0.4:
                    col = C_SKY_BOT
                elif t > 0.7:
                    col = C_SKY_BOT
                else:
                    col = C_SKY_MID
            else:
                col = C_SKY_BOT
            img.putpixel((x, y), col)

    # 2. Sun in upper right
    sun_cx, sun_cy = 55, 14
    sun_r = 5
    ray_coords = [
        (0, -8), (0, -10),
        (5, -5), (7, -7),
        (8, 0), (10, 0),
        (5, 5), (7, 7),
        (-5, -5), (-7, -7),
        (-8, 0), (-10, 0),
        (-5, 5), (-7, 7),
        (3, -8), (-3, -8),
        (8, -3), (8, 3)
    ]
    for dx, dy in ray_coords:
        rx, ry = sun_cx + dx, sun_cy + dy
        if 1 <= rx < 70 and 1 <= ry < 94:
            img.putpixel((rx, ry), C_SUN_OUT)

    for y in range(sun_cy - sun_r, sun_cy + sun_r + 1):
        for x in range(sun_cx - sun_r, sun_cx + sun_r + 1):
            dist_sq = (x - sun_cx)**2 + (y - sun_cy)**2
            if dist_sq <= (sun_r - 0.2)**2:
                img.putpixel((x, y), C_SUN_BODY)
            elif dist_sq <= (sun_r + 0.8)**2:
                img.putpixel((x, y), C_SUN_OUT)
    img.putpixel((sun_cx - 1, sun_cy - 1), C_SUN_HL)
    img.putpixel((sun_cx, sun_cy - 1), C_SUN_HL)

    # 3. Birds soaring near the peak
    birds = [
        (18, 18),
        (24, 14),
        (37, 21),
        (46, 24),
        (61, 26)
    ]
    for bx, by in birds:
        img.putpixel((bx - 1, by - 1), C_BIRD)
        img.putpixel((bx, by), C_BIRD)
        img.putpixel((bx + 1, by - 1), C_BIRD)

    # 4. MOUNTAIN RANGE (Multiple peaks: Left Peak, Main Central Peak, Right Peak)
    # Peak 1: Left Peak (summit at x=15, y=18)
    for y in range(18, 43):
        t_left = (y - 18) / (43 - 18)
        x_left = max(1, int(15 - t_left * 16))
        x_right = min(32, int(15 + t_left * 14))
        ridge_x = 15 - int(t_left * 2)
        for x in range(x_left, x_right + 1):
            if x < 1 or x >= 70: continue
            if x < ridge_x:
                col = C_SNOW_SH if y < 22 else (C_ROCK_DRK if (x + y * 2) % 3 == 0 else C_ROCK_HATCH)
            elif x == ridge_x:
                col = C_RIDGE
            else:
                col = C_SNOW if y < 21 else (C_ROCK_MID if (x * 3 + y) % 5 == 0 else C_ROCK_LGT)
            img.putpixel((x, y), col)
        img.putpixel((x_left, y), C_OUTLINE)

    # Peak 2: Right Peak (summit at x=52, y=19)
    for y in range(19, 43):
        t_right = (y - 19) / (43 - 19)
        x_left = max(33, int(52 - t_right * 15))
        x_right = min(69, int(52 + t_right * 17))
        ridge_x = 52 + int(t_right * 2)
        for x in range(x_left, x_right + 1):
            if x < 1 or x >= 70: continue
            if x < ridge_x:
                col = C_SNOW_SH if y < 23 else (C_ROCK_DRK if (x + y * 2) % 3 == 0 else C_ROCK_HATCH)
            elif x == ridge_x:
                col = C_RIDGE
            else:
                col = C_SNOW if y < 22 else (C_ROCK_MID if (x * 3 + y) % 5 == 0 else C_ROCK_LGT)
            img.putpixel((x, y), col)
        img.putpixel((x_right, y), C_OUTLINE)

    # Peak 3: Main Central Peak (Towering tall horn, summit at x=34, y=10)
    for y in range(10, 46):
        t_left = (y - 10) / (42 - 10)
        x_left = int(34 - t_left * 19)
        if y > 24: x_left -= 1
        t_right = (y - 10) / (44 - 10)
        x_right = int(34 + t_right * 19)

        if y < 15:
            ridge_x = 34
        elif y < 22:
            ridge_x = 34 + int((y - 14) * 0.4)
        elif y < 30:
            ridge_x = 36 - int((y - 22) * 0.5)
        else:
            ridge_x = 32 + int((y - 30) * 0.4)

        for x in range(x_left, x_right + 1):
            if x < 1 or x >= 70: continue
            if x < ridge_x:
                is_snow_crest = (y < 15 and (ridge_x - x) < 3) or (y < 13)
                if is_snow_crest:
                    col = C_SNOW_SH
                else:
                    col = C_ROCK_DRK if (x + y * 2) % 4 in (0, 1) else C_ROCK_HATCH
            elif x == ridge_x:
                col = C_RIDGE
            else:
                is_snow_crest = (y < 14) or (x - ridge_x < 2 and y < 19)
                if is_snow_crest:
                    col = C_SNOW
                else:
                    if (x * 3 + y) % 7 == 0:
                        col = C_ROCK_MID
                    elif (x + y) % 5 == 0:
                        col = C_ROCK_LGT
                    else:
                        col = C_ROCK_LGT
            img.putpixel((x, y), col)

        img.putpixel((x_left, y), C_OUTLINE)
        img.putpixel((x_right, y), C_OUTLINE)

    # 5. Distant Rolling Green Hills behind the pass (y=38..52)
    for x in range(1, 70):
        hill_y = int(39 + 4 * math.sin((x - 8) * 0.1))
        for y in range(max(1, hill_y), 50):
            img.putpixel((x, y), C_HILL_FAR)

    # 6. Valley Hills & Meadows covering middle and foreground (y=44..94)
    def get_river_path(y):
        t = (y - 44) / 50.0
        meander = -7.0 * math.sin(t * math.pi * 1.5) + 6.0 * math.sin(t * math.pi * 2.8)
        cx = 34.0 + meander
        hw = 1.2 + t * 7.5
        return cx, hw

    for y in range(44, 94):
        for x in range(1, 70):
            if y < 58:
                dist_from_hill_crest = y - int(38 + 9 * ((x - 18) / 16.0)**2 if x <= 34 else 39 + 8 * ((x - 54) / 18.0)**2)
                if dist_from_hill_crest <= 1:
                    col = C_HILL_LGT
                elif dist_from_hill_crest < 5:
                    col = C_HILL_LGT if (x + y) % 3 != 0 else C_HILL_MID
                else:
                    col = C_HILL_MID
            else:
                if (x + y * 2) % 7 == 0:
                    col = C_HILL_LGT
                elif (x + y) % 5 == 0:
                    col = C_HILL_SH
                elif (x * 2 + y) % 3 == 0:
                    col = C_MEADOW_FLAT
                else:
                    col = C_HILL_MID
                
                if (y % 5 == 0) and ((x + y) % 6 in (0, 1)):
                    col = C_HILL_SH

            img.putpixel((x, y), col)

    for x in range(1, 70):
        hy = int(38 + 9 * ((x - 18) / 16.0)**2 if x <= 34 else 39 + 8 * ((x - 54) / 18.0)**2)
        if 1 <= hy < 94:
            img.putpixel((x, hy), C_OUTLINE)

    # 7. Evergreen Pine Trees
    trees = [
        (7, 44, 7), (13, 42, 8), (19, 43, 7), (25, 46, 8),
        (43, 47, 7), (50, 44, 8), (57, 43, 7), (64, 45, 8),
        (10, 58, 8), (17, 63, 9), (56, 61, 9), (62, 57, 8),
        (8, 76, 8), (15, 82, 9), (54, 78, 8), (61, 85, 9),
        (11, 91, 7), (60, 92, 7)
    ]
    for tx, ty, th in trees:
        for yk in range(ty - 1, ty + 1):
            if 1 <= tx < 70 and 1 <= yk < 94:
                img.putpixel((tx, yk), C_TREE_TRK)
        for i in range(th):
            curr_y = ty - 2 - i
            half_w = int((i / float(th)) * 3.0)
            for dx in range(-half_w, half_w + 1):
                px, py = tx + dx, curr_y
                if 1 <= px < 70 and 1 <= py < 94:
                    if abs(dx) == half_w and half_w > 0:
                        img.putpixel((px, py), C_OUTLINE)
                    elif dx < 0:
                        img.putpixel((px, py), C_TREE_HL)
                    else:
                        img.putpixel((px, py), C_TREE)
        tip_y = ty - 2 - th
        if 1 <= tx < 70 and 1 <= tip_y < 94:
            img.putpixel((tx, tip_y), C_OUTLINE)

    # 8. WINDING RIVER (Flows continuously all the way to bottom border y=94)
    for y in range(44, 95):
        cx, hw = get_river_path(y)
        x_start = int(cx - hw)
        x_end = int(cx + hw)
        for x in range(x_start, x_end + 1):
            if 1 <= x < 70 and 1 <= y < 95:
                if x == x_start or x == x_end:
                    img.putpixel((x, y), C_OUTLINE)
                else:
                    dist_from_left = (x - x_start) / float(x_end - x_start)
                    if (x + y * 2) % 3 == 0:
                        col = C_WATER_LT
                    elif dist_from_left < 0.45:
                        col = C_WATER_MD
                    else:
                        col = C_WATER_DP
                    if (x + y) % 4 == 0 and 0.3 < dist_from_left < 0.7:
                        col = C_FOAM
                    img.putpixel((x, y), col)

    # 9. 1-pixel Crisp White Frame & Card Outer Border
    C_WHITE_FRAME = (255, 255, 255, 255)
    for x in range(3, 68):
        img.putpixel((x, 1), C_WHITE_FRAME)
        img.putpixel((x, 93), C_WHITE_FRAME)
    for y in range(3, 92):
        img.putpixel((1, y), C_WHITE_FRAME)
        img.putpixel((69, y), C_WHITE_FRAME)
    img.putpixel((2, 1), C_WHITE_FRAME)
    img.putpixel((1, 2), C_WHITE_FRAME)
    img.putpixel((68, 1), C_WHITE_FRAME)
    img.putpixel((69, 2), C_WHITE_FRAME)
    img.putpixel((1, 92), C_WHITE_FRAME)
    img.putpixel((2, 93), C_WHITE_FRAME)
    img.putpixel((69, 92), C_WHITE_FRAME)
    img.putpixel((68, 93), C_WHITE_FRAME)

    for x in range(3, 68):
        img.putpixel((x, 0), C_OUTLINE)
        img.putpixel((x, 94), C_OUTLINE)
    for y in range(3, 92):
        img.putpixel((0, y), C_OUTLINE)
        img.putpixel((70, y), C_OUTLINE)

    corner_pixels = [
        (2, 0), (1, 1), (0, 2),
        (68, 0), (69, 1), (70, 2),
        (0, 92), (1, 93), (2, 94),
        (70, 92), (69, 93), (68, 94)
    ]
    for cx, cy in corner_pixels:
        img.putpixel((cx, cy), C_OUTLINE)

    transparent_corners = [
        (0, 0), (1, 0), (0, 1),
        (69, 0), (70, 0), (70, 1),
        (0, 93), (0, 94), (1, 94),
        (70, 93), (70, 94), (69, 94)
    ]
    for tx, ty in transparent_corners:
        img.putpixel((tx, ty), (0, 0, 0, 0))

    # 10. AUTHENTIC VERTICAL "JOKER" LETTERING
    mask_path = os.path.join(BASE_DIR, "tools", "vertical_joker_mask.png")
    if os.path.exists(mask_path):
        mask = Image.open(mask_path)
        white_layer = Image.new("RGBA", mask.size, (255, 255, 255, 220))
        slate_layer = Image.new("RGBA", mask.size, C_OUTLINE)

        # Top-left vertical text
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            img.paste(white_layer, (3 + dx, 7 + dy), mask)
        img.paste(slate_layer, (3, 7), mask)

        # Bottom-right vertical text
        mask_rot = mask.rotate(180)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            img.paste(white_layer, (58 + dx, 44 + dy), mask_rot)
        img.paste(slate_layer, (58, 44), mask_rot)

    export_sprite(img, "j_river.png")

def build_j_stone_tablet():
    """Builds Stone Tablet Joker (71x95 px, 142x190 2x) on authentic Stone Card background.
    Features an ancient weathered cracked stone face with:
    - 'JOKER' carved directly into the stone texture with chiseled relief highlights & shadows
    - Two deeply engraved circular seal petroglyphs (matching reference photo: top-right seal with cross, bottom-right seal with spirals)
    - Ancient carved runic seal glyphs and petroglyphs on the left
    - Deep organic stone fracture fissures splitting the slab."""
    img = load_enhancement_base("stone")
    draw = ImageDraw.Draw(img)

    C_OUTLINE = (30, 37, 40, 255)
    C_ENGRAVE_SH = (45, 52, 62, 255)    # Deep shadow inside carved groove
    C_ENGRAVE_MD = (75, 84, 96, 255)    # Mid tone inside carved groove
    C_ENGRAVE_HL = (245, 248, 252, 255)  # Sunlit beveled stone lip / highlight

    def draw_chiseled_line(p1, p2, width=1):
        x1, y1 = p1
        x2, y2 = p2
        draw.line([p1, p2], fill=C_ENGRAVE_SH, width=width)
        draw.line([(x1 + 1, y1 + 1), (x2 + 1, y2 + 1)], fill=C_ENGRAVE_HL, width=1)

    def draw_chiseled_circle(cx, cy, r):
        for a in range(-r, r + 1):
            for b in range(-r, r + 1):
                d_sq = a * a + b * b
                if (r - 0.7) ** 2 <= d_sq <= (r + 0.7) ** 2:
                    if a + b < 0:
                        img.putpixel((cx + a, cy + b), C_ENGRAVE_SH)
                    else:
                        img.putpixel((cx + a, cy + b), C_ENGRAVE_HL)

    # 1. Major organic stone fissure running down the tablet
    crack_points = [
        (36, 1), (35, 7), (38, 14), (37, 21), (34, 28), (35, 36),
        (33, 44), (32, 53), (35, 62), (34, 71), (37, 80), (35, 88), (36, 94)
    ]
    for i in range(len(crack_points) - 1):
        p1 = crack_points[i]
        p2 = crack_points[i + 1]
        draw.line([p1, p2], fill=C_ENGRAVE_SH, width=1)
        draw.line([(p1[0] + 1, p1[1]), (p2[0] + 1, p2[1])], fill=C_ENGRAVE_HL, width=1)

    branch1 = [(37, 21), (45, 17), (52, 18), (58, 15)]
    for i in range(len(branch1) - 1):
        draw.line([branch1[i], branch1[i+1]], fill=C_ENGRAVE_SH, width=1)
        draw.line([(branch1[i][0] + 1, branch1[i][1] + 1), (branch1[i+1][0] + 1, branch1[i+1][1] + 1)], fill=C_ENGRAVE_HL, width=1)

    branch2 = [(32, 53), (25, 59), (18, 57), (12, 62)]
    for i in range(len(branch2) - 1):
        draw.line([branch2[i], branch2[i+1]], fill=C_ENGRAVE_SH, width=1)
        draw.line([(branch2[i][0] + 1, branch2[i][1] + 1), (branch2[i+1][0] + 1, branch2[i+1][1] + 1)], fill=C_ENGRAVE_HL, width=1)

    # 2. Carved "JOKER" across the top in ancient chiseled lettering
    joker_glyphs = {
        # 'J'
        (16, 10): 1, (17, 10): 1, (18, 10): 1, (19, 10): 1, (20, 10): 1,
        (19, 11): 1, (19, 12): 1, (19, 13): 1, (19, 14): 1, (19, 15): 1,
        (18, 16): 1, (17, 16): 1, (16, 15): 1, (16, 14): 1,

        # 'O'
        (25, 10): 1, (26, 10): 1, (27, 10): 1, (28, 10): 1,
        (24, 11): 1, (29, 11): 1,
        (24, 12): 1, (29, 12): 1,
        (24, 13): 1, (29, 13): 1,
        (24, 14): 1, (29, 14): 1,
        (24, 15): 1, (29, 15): 1,
        (25, 16): 1, (26, 16): 1, (27, 16): 1, (28, 16): 1,

        # 'K'
        (33, 10): 1, (38, 10): 1,
        (33, 11): 1, (37, 11): 1,
        (33, 12): 1, (36, 12): 1,
        (33, 13): 1, (34, 13): 1, (35, 13): 1,
        (33, 14): 1, (36, 14): 1,
        (33, 15): 1, (37, 15): 1,
        (33, 16): 1, (38, 16): 1,

        # 'E'
        (42, 10): 1, (43, 10): 1, (44, 10): 1, (45, 10): 1, (46, 10): 1,
        (42, 11): 1,
        (42, 12): 1,
        (42, 13): 1, (43, 13): 1, (44, 13): 1, (45, 13): 1,
        (42, 14): 1,
        (42, 15): 1,
        (42, 16): 1, (43, 16): 1, (44, 16): 1, (45, 16): 1, (46, 16): 1,

        # 'R'
        (50, 10): 1, (51, 10): 1, (52, 10): 1, (53, 10): 1, (54, 10): 1,
        (50, 11): 1, (55, 11): 1,
        (50, 12): 1, (55, 12): 1,
        (50, 13): 1, (51, 13): 1, (52, 13): 1, (53, 13): 1, (54, 13): 1,
        (50, 14): 1, (53, 14): 1,
        (50, 15): 1, (54, 15): 1,
        (50, 16): 1, (55, 16): 1,
    }

    for (gx, gy) in joker_glyphs:
        img.putpixel((gx, gy), C_ENGRAVE_SH)
        if (gx + 1, gy + 1) not in joker_glyphs:
            img.putpixel((gx + 1, gy + 1), C_ENGRAVE_HL)

    # 3. Two Carved Seal Circles (Matching reference photo)
    # Circle 1: Upper Right Seal Circle with Cross (cx=51, cy=38, radius=12)
    draw_chiseled_circle(51, 38, 12)
    draw_chiseled_circle(51, 38, 9)
    draw_chiseled_line((45, 32), (57, 44))
    draw_chiseled_line((45, 44), (57, 32))
    for angle_deg in [0, 45, 90, 135, 180, 225, 270, 315]:
        rad = angle_deg * 3.14159 / 180.0
        bx = int(51 + 10.5 * math.cos(rad))
        by = int(38 + 10.5 * math.sin(rad))
        img.putpixel((bx, by), C_ENGRAVE_SH)

    # Circle 2: Lower Right Seal Circle with Spirals (cx=51, cy=68, radius=12)
    draw_chiseled_circle(51, 68, 12)
    draw_chiseled_circle(51, 68, 10)
    for t_step in range(11):
        st = t_step / 10.0
        sx = int(45 + st * 12)
        sy = int(68 - 4.5 * math.sin(st * 3.14159))
        img.putpixel((sx, sy), C_ENGRAVE_SH)
        img.putpixel((sx + 1, sy + 1), C_ENGRAVE_HL)
    for t_step in range(13):
        st = t_step / 12.0
        sx = int(44 + st * 14)
        sy = int(68 + 4.5 * math.sin((st - 0.5) * 3.14159))
        img.putpixel((sx, sy), C_ENGRAVE_SH)
        img.putpixel((sx + 1, sy + 1), C_ENGRAVE_HL)
    for t_step in range(11):
        st = t_step / 10.0
        sx = int(45 + st * 12)
        sy = int(68 + 4.5 * math.sin(st * 3.14159))
        img.putpixel((sx, sy), C_ENGRAVE_SH)
        img.putpixel((sx + 1, sy + 1), C_ENGRAVE_HL)

    # 4. Left side Carved Petroglyphic Symbols
    draw_chiseled_line((12, 45), (28, 45))
    draw_chiseled_line((12, 45), (20, 39))
    draw_chiseled_line((28, 45), (20, 39))
    draw_chiseled_line((20, 31), (20, 43))
    draw_chiseled_line((14, 33), (26, 41))
    draw_chiseled_line((14, 41), (26, 33))

    # Center T-pillar
    draw_chiseled_line((31, 23), (39, 23))
    draw_chiseled_line((35, 23), (35, 29))
    draw_chiseled_line((32, 29), (38, 29))
    draw_chiseled_line((35, 19), (37, 21))
    draw_chiseled_line((37, 18), (39, 20))

    # Lower Left Petroglyph (Triangle + Star)
    draw_chiseled_line((20, 58), (12, 76))
    draw_chiseled_line((20, 58), (28, 76))
    draw_chiseled_line((12, 76), (28, 76))
    draw_chiseled_line((20, 63), (20, 71))
    draw_chiseled_line((16, 66), (24, 70))
    draw_chiseled_line((16, 70), (24, 66))

    # 5. Bottom ancient horizontal hash marks
    for hx in [16, 25, 34, 43, 52]:
        draw_chiseled_line((hx, 85), (hx + 5, 85))
        draw_chiseled_line((hx, 88), (hx + 5, 88))

    export_sprite(img, "j_stone_tablet.png")

def build_j_overkill():
    """Builds Overkill Joker (71x95 px, 142x190 2x).
    Effect: Creates a Spectral card when Boss Blind is defeated if any single hand beat the Blind requirement.
    Features:
    - Heavy cast iron mortar/cannon angled at 35 degrees with brass bands and rivet details
    - Engraved skull emblem on the cannon body
    - Wood and bronze wheeled artillery carriage at base
    - Massive billowing spectral ectoplasm smoke cloud with an embedded grinning ghostly skull
    - Floating spectral stars, embers, and cyan smoke wisps
    - Radial comic-book blast lines in background
    - Authentic vertical JOKER typography along margins
    """
    img = create_card_base(bg_color=PALETTE["CARD_CREAM"], border_color=PALETTE["DEEP_OUTLINE"])
    draw = ImageDraw.Draw(img)

    # Inner border line
    draw.rectangle([3, 3, 67, 91], outline=PALETTE["PAPER_SHADOW"])
    draw_vertical_joker_text(img, PALETTE["DARK_SLATE"], top_left=True, bottom_right=True)

    C_OUTLINE    = (47, 62, 70, 255)       # #2F3E46
    C_IRON_DARK  = (55, 66, 68, 255)       # #374244
    C_IRON_MID   = (79, 99, 103, 255)      # #4F6367
    C_IRON_LIGHT = (130, 155, 160, 255)
    C_BRASS      = (218, 183, 114, 255)     # #DAB772
    C_BRASS_DARK = (165, 133, 71, 255)     # #A58547

    # Spectral palette
    C_SPEC_GLOW  = (163, 203, 255, 255)    # #A3CBFF
    C_SPEC_CYAN  = (19, 175, 206, 255)     # #13AFCE
    C_SPEC_BLUE  = (75, 123, 236, 255)     # #4B7BEC
    C_SPEC_LIGHT = (112, 161, 255, 255)    # #70A1FF
    C_WHITE      = (255, 255, 255, 255)

    # 1. Background radial blast lines from cannon muzzle (approx cx=42, cy=38)
    mx, my = 42, 38
    for angle_deg in [10, 25, 45, 65, 80, 290, 310, 330, 350]:
        rad = math.radians(angle_deg)
        for r in range(12, 28):
            if r % 2 == 0:
                bx = int(mx + r * math.cos(rad))
                by = int(my + r * math.sin(rad))
                if 4 <= bx <= 66 and 4 <= by <= 90:
                    img.putpixel((bx, by), (230, 215, 190, 255))

    # 2. Wooden Cannon Carriage / Wheel (at bottom left, x=15..35, y=56..78)
    # Carriage base
    draw.polygon([(16, 68), (38, 62), (40, 72), (18, 76)], fill=(92, 64, 51, 255), outline=C_OUTLINE)
    draw.polygon([(18, 69), (36, 64), (37, 70), (19, 74)], fill=(139, 90, 43, 255))

    # Heavy iron-rimmed carriage wheel (centered at x=25, y=70)
    draw.ellipse([17, 62, 33, 78], fill=C_IRON_DARK, outline=C_OUTLINE)
    draw.ellipse([19, 64, 31, 76], fill=(107, 78, 40, 255), outline=C_OUTLINE)
    # Wheel hub
    draw.ellipse([23, 68, 27, 72], fill=C_BRASS, outline=C_OUTLINE)
    # Wheel spokes
    draw.line([(25, 64), (25, 76)], fill=C_BRASS_DARK)
    draw.line([(19, 70), (31, 70)], fill=C_BRASS_DARK)

    # 3. Heavy Iron Cannon Barrel (aimed up-right at ~35 deg angle)
    # Cannon body polygon from breech (18, 54) to muzzle (42, 34)
    draw.polygon([(18, 54), (40, 34), (46, 40), (24, 62)], fill=C_IRON_MID, outline=C_OUTLINE)
    # Shading on barrel
    draw.line([(19, 55), (41, 35)], fill=C_IRON_LIGHT)
    draw.line([(23, 61), (45, 39)], fill=C_IRON_DARK)

    # Brass reinforcement hoops around barrel
    # Breech band
    draw.line([(20, 52), (25, 60)], fill=C_BRASS, width=2)
    # Mid band
    draw.line([(29, 44), (34, 52)], fill=C_BRASS, width=2)
    # Muzzle ring / flared mouth
    draw.polygon([(39, 33), (43, 31), (49, 39), (45, 41)], fill=C_BRASS, outline=C_OUTLINE)
    draw.ellipse([42, 33, 48, 39], fill=C_IRON_DARK, outline=C_OUTLINE)

    # Skull emblem on the cannon body
    draw.ellipse([27, 49, 31, 53], fill=C_WHITE, outline=C_OUTLINE)
    draw.point((28, 50), fill=C_OUTLINE)
    draw.point((30, 50), fill=C_OUTLINE)
    draw.rectangle([28, 53, 30, 54], fill=C_WHITE)

    # 4. Billowing Spectral Ectoplasm Smoke & Ghostly Skull Plume
    # Plume clouds expanding from muzzle into upper-right quadrant
    # Outer dark spectral blue clouds
    draw.ellipse([38, 14, 58, 34], fill=C_SPEC_BLUE, outline=C_OUTLINE)
    draw.ellipse([46, 22, 64, 40], fill=C_SPEC_BLUE, outline=C_OUTLINE)
    draw.ellipse([34, 24, 48, 38], fill=C_SPEC_CYAN, outline=C_OUTLINE)

    # Mid spectral cyan / light blue body
    draw.ellipse([40, 16, 56, 32], fill=C_SPEC_CYAN)
    draw.ellipse([48, 24, 62, 38], fill=C_SPEC_LIGHT)
    draw.ellipse([42, 18, 54, 30], fill=C_SPEC_GLOW)

    # Ghostly skull face inside the smoke plume!
    # Skull eye sockets
    draw.ellipse([44, 21, 47, 25], fill=C_SPEC_BLUE)
    draw.ellipse([50, 21, 53, 25], fill=C_SPEC_BLUE)
    # Nose cavity
    draw.point((48, 25), fill=C_SPEC_BLUE)
    draw.point((49, 25), fill=C_SPEC_BLUE)
    # Teeth / mouth grinning
    draw.line([(45, 28), (52, 28)], fill=C_SPEC_BLUE)
    draw.point((47, 28), fill=C_WHITE)
    draw.point((49, 28), fill=C_WHITE)
    draw.point((51, 28), fill=C_WHITE)

    # Floating spectral soul wisps, embers, and stars
    stars = [(56, 12), (62, 20), (36, 14), (60, 42), (48, 8)]
    for sx, sy in stars:
        draw.line([(sx - 1, sy), (sx + 1, sy)], fill=C_SPEC_GLOW)
        draw.line([(sx, sy - 1), (sx, sy + 1)], fill=C_SPEC_GLOW)
        img.putpixel((sx, sy), C_WHITE)

    # Smoke curls around the cannon base
    draw.ellipse([14, 50, 22, 58], fill=C_SPEC_GLOW, outline=C_SPEC_BLUE)
    draw.ellipse([16, 52, 20, 56], fill=C_WHITE)

    export_sprite(img, "j_overkill.png")

def build_j_spotlight():
    """Builds Spotlight Joker (71x95 px, 142x190 2x).
    Effect: If played hand is a 5-card High Card, the scoring card becomes Enhanced.
    Features:
    - Dark atmospheric theatrical stage backdrop
    - Overhead stage spotlight fixture beaming down warm golden and creamy light
    - Brilliant conical beam of light bathing the center stage
    - A single illuminated hero playing card standing proud in the spotlight
    - 4 shadowy card silhouettes standing back in the dark wings (the uncredited High Card fodder)
    - Golden stage dust motes and sparkling stars in the beam
    - Authentic vertical JOKER typography along margins
    """
    img = create_card_base(bg_color=(35, 30, 42, 255), border_color=PALETTE["DEEP_OUTLINE"])
    draw = ImageDraw.Draw(img)

    # Inner border line
    draw.rectangle([3, 3, 67, 91], outline=(55, 48, 65, 255))
    draw_vertical_joker_text(img, (180, 160, 200, 255), top_left=True, bottom_right=True)

    C_OUTLINE = (47, 62, 70, 255)
    C_GOLD = (218, 183, 114, 255)
    C_GOLD_LIGHT = (245, 225, 150, 255)
    C_CREAM = (255, 240, 200, 255)
    C_WHITE = (255, 255, 255, 255)
    C_STAGE_WOOD = (85, 55, 35, 255)
    C_STAGE_DARK = (55, 35, 22, 255)

    # 1. Wooden stage floor at bottom (y=66..91)
    draw.rectangle([4, 66, 66, 90], fill=C_STAGE_WOOD)
    for sy in range(66, 91, 5):
        draw.line([(4, sy), (66, sy)], fill=C_STAGE_DARK)
    for sx in [18, 32, 46, 58]:
        draw.line([(sx, 66), (sx, 90)], fill=C_STAGE_DARK)

    # 2. Four shadowy card silhouettes standing in the dark wings!
    C_SHADOW_CARD = (50, 45, 60, 255)
    C_SHADOW_BORDER = (38, 34, 46, 255)
    draw.rectangle([10, 50, 19, 68], fill=C_SHADOW_CARD, outline=C_SHADOW_BORDER)
    draw.rectangle([16, 54, 25, 72], fill=C_SHADOW_CARD, outline=C_SHADOW_BORDER)
    draw.rectangle([46, 54, 55, 72], fill=C_SHADOW_CARD, outline=C_SHADOW_BORDER)
    draw.rectangle([52, 50, 61, 68], fill=C_SHADOW_CARD, outline=C_SHADOW_BORDER)

    # 3. Overhead Theatre Spotlight Lamp at top (centered at x=35, y=8)
    draw.line([(31, 4), (39, 4)], fill=(120, 120, 130, 255), width=2)
    draw.polygon([(30, 6), (40, 6), (42, 12), (28, 12)], fill=(45, 45, 52, 255), outline=C_OUTLINE)
    draw.polygon([(26, 11), (44, 11), (46, 16), (24, 16)], fill=(70, 70, 80, 255), outline=C_OUTLINE)
    draw.ellipse([27, 13, 43, 17], fill=C_WHITE, outline=C_GOLD)

    # 4. Conical Spotlight Beam of Light cutting through the air
    for y in range(16, 82):
        progress = (y - 16) / (82 - 16)
        x_left = int(31 - progress * (31 - 12))
        x_right = int(39 + progress * (58 - 39))
        for x in range(x_left, x_right + 1):
            if 4 <= x <= 66 and 4 <= y <= 90:
                mid_x = (x_left + x_right) / 2.0
                dist_norm = abs(x - mid_x) / ((x_right - x_left) / 2.0 + 0.1)
                if dist_norm < 0.4:
                    img.putpixel((x, y), C_CREAM if (x + y) % 2 == 0 else C_GOLD_LIGHT)
                elif dist_norm < 0.8:
                    if (x + y) % 2 == 0:
                        img.putpixel((x, y), C_GOLD)
                else:
                    if (x ^ y) % 3 == 0:
                        img.putpixel((x, y), C_GOLD)

    # Stage light pool on the floor
    draw.ellipse([16, 68, 54, 84], fill=C_GOLD, outline=C_GOLD_LIGHT)
    draw.ellipse([22, 70, 48, 82], fill=C_CREAM)

    # 5. The Hero Card standing proudly in the dead center of the Spotlight!
    draw.rectangle([28, 44, 42, 68], fill=C_WHITE, outline=C_OUTLINE)
    draw.rectangle([30, 46, 40, 66], outline=C_GOLD)
    draw.polygon([(35, 50), (38, 56), (32, 56)], fill=(254, 95, 85, 255))
    draw.polygon([(35, 62), (32, 56), (38, 56)], fill=(254, 95, 85, 255))
    draw.point((35, 56), fill=C_WHITE)

    # 6. Floating golden dust motes and sparkling stars around the card
    sparkles = [(25, 34), (45, 36), (22, 50), (48, 48), (35, 30), (35, 74)]
    for sx, sy in sparkles:
        draw.line([(sx - 1, sy), (sx + 1, sy)], fill=C_GOLD_LIGHT)
        draw.line([(sx, sy - 1), (sx, sy + 1)], fill=C_GOLD_LIGHT)
        img.putpixel((sx, sy), C_WHITE)

    export_sprite(img, "j_spotlight.png")

def build_j_short_circuit():
    """Builds Short Circuit Joker (71x95 px, 142x190 2x).
    Effect: If a card is retriggered, has a 1 in 4 chance to retrigger its neighbors as well.
    Features:
    - Electronic green printed circuit board (PCB) background with gold conductive traces and solder vias
    - Integrated circuit microchip and band-coded resistor components
    - Scorched, burned impact crater in the center from an electrical surge
    - Severed red and blue insulated copper wires crossing and short-circuiting
    - Violent high-voltage electric lightning arcs jumping across the gap
    - Branching lightning bolts jumping outwards towards the left and right card edges (neighboring cards)
    - Flying electric sparks, plasma bursts, and rising smoke wisps
    - Authentic vertical JOKER typography along margins
    """
    C_PCB_DARK   = (18, 42, 28, 255)
    C_PCB_LIGHT  = (35, 78, 52, 255)
    C_TRACE_GOLD = (218, 183, 114, 255)
    C_TRACE_DARK = (145, 115, 60, 255)
    C_SOLDER     = (180, 195, 205, 255)
    C_OUTLINE    = (20, 25, 22, 255)

    C_ELEC_CORE  = (255, 255, 255, 255)
    C_ELEC_CYAN  = (0, 215, 255, 255)
    C_ELEC_BLUE  = (75, 123, 236, 255)

    img = create_card_base(bg_color=C_PCB_DARK, border_color=PALETTE["DEEP_OUTLINE"])
    draw = ImageDraw.Draw(img)

    # Inner border line
    draw.rectangle([3, 3, 67, 91], outline=C_PCB_LIGHT)
    draw_vertical_joker_text(img, (130, 175, 145, 255), top_left=True, bottom_right=True)

    # 1. Background PCB Grid / Bus Traces
    traces = [
        [(6, 18), (64, 18)],
        [(6, 28), (28, 28)],
        [(42, 28), (64, 28)],
        [(6, 74), (64, 74)],
        [(6, 82), (64, 82)],
        [(15, 18), (15, 74)],
        [(55, 18), (55, 74)],
        [(25, 18), (25, 36)],
        [(45, 18), (45, 36)],
        [(25, 58), (25, 82)],
        [(45, 58), (45, 82)],
        [(15, 40), (22, 47)],
        [(55, 40), (48, 47)],
    ]
    for tr in traces:
        draw.line(tr, fill=C_TRACE_DARK, width=1)

    # Solder pads / vias
    vias = [
        (15, 18), (55, 18), (25, 18), (45, 18),
        (15, 74), (55, 74), (25, 82), (45, 82),
        (25, 36), (45, 36), (25, 58), (45, 58),
        (15, 40), (55, 40), (22, 47), (48, 47)
    ]
    for vx, vy in vias:
        draw.ellipse([vx-1, vy-1, vx+1, vy+1], fill=C_TRACE_GOLD, outline=C_TRACE_DARK)
        img.putpixel((vx, vy), C_SOLDER)

    # Small electronic IC microchip at top center
    draw.rectangle([28, 12, 42, 22], fill=(30, 30, 35, 255), outline=C_OUTLINE)
    draw.point((30, 14), fill=(200, 200, 200, 255))
    for px in [30, 33, 36, 39]:
        draw.line([(px, 10), (px, 12)], fill=C_SOLDER)
        draw.line([(px, 22), (px, 24)], fill=C_SOLDER)

    # Resistor at bottom
    draw.rectangle([28, 76, 42, 80], fill=(215, 185, 140, 255), outline=C_OUTLINE)
    draw.line([(26, 78), (28, 78)], fill=C_SOLDER)
    draw.line([(42, 78), (44, 78)], fill=C_SOLDER)
    draw.line([(31, 76), (31, 80)], fill=(200, 40, 40, 255))
    draw.line([(34, 76), (34, 80)], fill=(40, 40, 40, 255))
    draw.line([(37, 76), (37, 80)], fill=(218, 183, 114, 255))

    # 2. Burned / scorched crater in center
    draw.ellipse([24, 38, 46, 60], fill=(12, 14, 13, 255))
    draw.ellipse([27, 41, 43, 57], fill=(25, 20, 18, 255))

    # 3. Two severed heavy copper wires crossing and short-circuiting
    draw.polygon([(16, 50), (16, 53), (29, 49), (29, 46)], fill=(220, 50, 45, 255), outline=C_OUTLINE)
    draw.line([(16, 51), (28, 47)], fill=(255, 120, 110, 255))
    draw.polygon([(29, 46), (33, 44), (32, 47), (29, 49)], fill=C_TRACE_GOLD, outline=C_OUTLINE)

    draw.polygon([(54, 49), (54, 52), (41, 54), (41, 51)], fill=(45, 115, 220, 255), outline=C_OUTLINE)
    draw.line([(54, 50), (42, 52)], fill=(110, 170, 255, 255))
    draw.polygon([(41, 51), (37, 53), (38, 56), (41, 54)], fill=C_TRACE_GOLD, outline=C_OUTLINE)

    # 4. Violent Electric Lightning Arcs exploding across the gap
    arc_points = [
        (33, 45), (32, 48), (36, 47), (34, 51), (38, 50), (37, 54)
    ]
    for i in range(len(arc_points)-1):
        draw.line([arc_points[i], arc_points[i+1]], fill=C_ELEC_CYAN, width=2)
        draw.line([arc_points[i], arc_points[i+1]], fill=C_ELEC_CORE, width=1)

    # Secondary branching arcs jumping outwards towards neighbors
    left_arc = [(32, 48), (27, 44), (22, 47), (18, 43), (13, 46)]
    for i in range(len(left_arc)-1):
        draw.line([left_arc[i], left_arc[i+1]], fill=C_ELEC_BLUE, width=2)
        draw.line([left_arc[i], left_arc[i+1]], fill=C_ELEC_CORE, width=1)

    right_arc = [(38, 50), (43, 53), (48, 49), (53, 54), (58, 50)]
    for i in range(len(right_arc)-1):
        draw.line([right_arc[i], right_arc[i+1]], fill=C_ELEC_BLUE, width=2)
        draw.line([right_arc[i], right_arc[i+1]], fill=C_ELEC_CORE, width=1)

    top_arc = [(35, 47), (33, 40), (38, 35), (35, 30)]
    for i in range(len(top_arc)-1):
        draw.line([top_arc[i], top_arc[i+1]], fill=C_ELEC_CYAN, width=1)
        img.putpixel(top_arc[i+1], C_ELEC_CORE)

    # 5. Exploding electrical sparks and plasma bursts
    sparks = [
        (35, 48), (30, 42), (40, 44), (28, 53), (42, 58),
        (20, 41), (50, 46), (15, 48), (56, 52), (35, 27),
        (24, 34), (46, 36), (36, 62), (32, 59)
    ]
    for sx, sy in sparks:
        img.putpixel((sx, sy), C_ELEC_CORE)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if (sx+dx, sy+dy) not in sparks:
                img.putpixel((sx+dx, sy+dy), C_ELEC_CYAN)

    draw.ellipse([32, 33, 38, 38], outline=(100, 110, 105, 255))
    draw.ellipse([36, 28, 41, 33], outline=(80, 90, 85, 255))

    export_sprite(img, "j_short_circuit.png")

def draw_kinetic_shockwaves(img, bg_base, ring_color, ring_highlight, ring_dark, text_color):
    """
    Draws the shared kinetic shockwave background:
    - Base suit color fill
    - Expanding harmonic ripple ellipses radiating from (35, 47)
    - Radiating dashed deflection speed beams
    - Card framing & authentic vertical JOKER text
    """
    draw = ImageDraw.Draw(img)
    draw.rectangle([2, 2, 68, 92], fill=bg_base)
    
    radii = [10, 17, 25, 33, 42, 52, 62]
    cx, cy = 35, 47
    for r in radii:
        rx = int(r * 0.88)
        ry = int(r * 1.08)
        draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=ring_dark, width=1)
        draw.ellipse([cx - rx + 1, cy - ry + 1, cx + rx - 1, cy + ry - 1], outline=ring_color, width=1)
        
    for deg in range(15, 360, 30):
        rad = math.radians(deg)
        x1 = cx + 8 * math.cos(rad)
        y1 = cy + 8 * math.sin(rad)
        x2 = cx + 46 * math.cos(rad)
        y2 = cy + 46 * math.sin(rad)
        steps = 8
        for s in range(steps):
            if s % 2 == 0:
                sx = int(x1 + (x2 - x1) * (s / steps))
                sy = int(y1 + (y2 - y1) * (s / steps))
                ex = int(x1 + (x2 - x1) * ((s + 0.6) / steps))
                ey = int(y1 + (y2 - y1) * ((s + 0.6) / steps))
                if 2 <= sx <= 68 and 2 <= sy <= 92 and 2 <= ex <= 68 and 2 <= ey <= 92:
                    draw.line([(sx, sy), (ex, ey)], fill=ring_highlight)

    draw.rectangle([3, 3, 67, 91], outline=ring_dark)
    draw_vertical_joker_text(img, text_color, top_left=True, bottom_right=True)

def build_j_ricochet():
    """Builds Ricochet Joker (Diamonds) - Angular bouncing diamond crystal with kinetic spark rays."""
    img = create_card_base()
    draw = ImageDraw.Draw(img)
    
    bg_base = (235, 145, 45, 255)
    ring_color = (255, 185, 80, 255)
    ring_highlight = (255, 230, 140, 255)
    ring_dark = (160, 85, 20, 255)
    text_color = (255, 255, 255, 255)
    draw_kinetic_shockwaves(img, bg_base, ring_color, ring_highlight, ring_dark, text_color)
    
    C_OUTLINE = PALETTE["DEEP_OUTLINE"]
    C_WHITE = (255, 255, 255, 255)
    C_CYAN_LIGHT = (225, 248, 255, 255)
    C_CYAN_MID = (150, 215, 245, 255)
    C_CYAN_DARK = (85, 155, 200, 255)
    C_GOLD_SPARK = (255, 225, 100, 255)
    
    draw.line([(16, 68), (35, 47)], fill=C_GOLD_SPARK, width=2)
    draw.line([(17, 67), (35, 47)], fill=C_WHITE, width=1)
    draw.line([(35, 47), (56, 22)], fill=C_GOLD_SPARK, width=2)
    draw.line([(35, 47), (55, 23)], fill=C_WHITE, width=1)
    
    draw.polygon([(35, 32), (47, 43), (35, 62), (23, 43)], fill=C_CYAN_DARK, outline=C_OUTLINE)
    draw.polygon([(35, 32), (47, 43), (35, 45)], fill=C_CYAN_MID)
    draw.polygon([(35, 32), (23, 43), (35, 45)], fill=C_CYAN_LIGHT)
    draw.polygon([(23, 43), (35, 62), (35, 45)], fill=C_CYAN_MID)
    draw.polygon([(47, 43), (35, 62), (35, 45)], fill=C_CYAN_DARK)
    
    draw.line([(35, 32), (35, 62)], fill=C_OUTLINE)
    draw.line([(23, 43), (47, 43)], fill=C_OUTLINE)
    draw.polygon([(31, 38), (39, 38), (35, 43)], fill=C_WHITE)
    
    draw.line([(31, 47), (39, 47)], fill=C_WHITE, width=2)
    draw.line([(35, 43), (35, 51)], fill=C_WHITE, width=2)
    draw.point((35, 47), fill=C_GOLD_SPARK)
    
    shards = [
        ([(21, 31), (24, 30), (22, 35)], C_CYAN_LIGHT),
        ([(49, 31), (52, 34), (48, 36)], C_WHITE),
        ([(46, 57), (50, 59), (48, 62)], C_CYAN_MID),
        ([(19, 53), (22, 54), (20, 58)], C_CYAN_DARK),
    ]
    for s_poly, col in shards:
        draw.polygon(s_poly, fill=col, outline=C_OUTLINE)
        
    export_sprite(img, "j_ricochet.png")

def build_j_rebound():
    """Builds Rebound Joker (Hearts) - Plump rubbery heart squashing on impact and springing upward."""
    img = create_card_base()
    draw = ImageDraw.Draw(img)
    
    bg_base = (215, 50, 60, 255)
    ring_color = (245, 95, 110, 255)
    ring_highlight = (255, 190, 205, 255)
    ring_dark = (140, 25, 35, 255)
    text_color = (255, 255, 255, 255)
    draw_kinetic_shockwaves(img, bg_base, ring_color, ring_highlight, ring_dark, text_color)
    
    C_OUTLINE = PALETTE["DEEP_OUTLINE"]
    C_WHITE = (255, 255, 255, 255)
    C_RUBY_LIGHT = (255, 130, 145, 255)
    C_RUBY_CORE = (235, 45, 65, 255)
    C_RUBY_DARK = (150, 20, 35, 255)
    
    for w, y_arc in [(18, 62), (26, 65), (34, 68)]:
        draw.arc([35 - w//2, y_arc - 4, 35 + w//2, y_arc + 4], start=0, end=180, fill=C_RUBY_LIGHT, width=2)
        
    draw.ellipse([21, 33, 37, 49], fill=C_RUBY_CORE, outline=C_OUTLINE)
    draw.ellipse([33, 33, 49, 49], fill=C_RUBY_CORE, outline=C_OUTLINE)
    draw.polygon([(22, 44), (48, 44), (35, 60)], fill=C_RUBY_CORE, outline=C_OUTLINE)
    
    draw.ellipse([23, 35, 35, 47], fill=C_RUBY_CORE)
    draw.ellipse([35, 35, 47, 47], fill=C_RUBY_CORE)
    draw.polygon([(24, 43), (46, 43), (35, 58)], fill=C_RUBY_CORE)
    
    draw.polygon([(26, 48), (44, 48), (35, 59)], fill=C_RUBY_DARK)
    
    draw.arc([24, 35, 34, 45], start=180, end=300, fill=C_WHITE, width=2)
    draw.point((27, 36), fill=C_WHITE)
    draw.point((28, 36), fill=C_WHITE)
    draw.point((41, 36), fill=C_RUBY_LIGHT)
    
    draw.line([(35, 25), (35, 30)], fill=C_WHITE, width=2)
    draw.line([(28, 26), (29, 31)], fill=C_RUBY_LIGHT, width=1)
    draw.line([(42, 26), (41, 31)], fill=C_RUBY_LIGHT, width=1)
    
    for bx, by in [(20, 32), (50, 34), (18, 52), (52, 53)]:
        draw.ellipse([bx-2, by-2, bx+2, by+2], fill=C_RUBY_LIGHT, outline=C_OUTLINE)
        draw.point((bx, by), fill=C_WHITE)
        
    export_sprite(img, "j_rebound.png")

def build_j_backlash():
    """Builds Backlash Joker (Spades) - Heavy pointed steel blade vibrating with violent parry recoil."""
    img = create_card_base()
    draw = ImageDraw.Draw(img)
    
    bg_base = (60, 70, 115, 255)
    ring_color = (95, 115, 175, 255)
    ring_highlight = (185, 210, 255, 255)
    ring_dark = (35, 40, 75, 255)
    text_color = (255, 255, 255, 255)
    draw_kinetic_shockwaves(img, bg_base, ring_color, ring_highlight, ring_dark, text_color)
    
    C_OUTLINE = PALETTE["DEEP_OUTLINE"]
    C_WHITE = (255, 255, 255, 255)
    C_STEEL_HL = (215, 230, 245, 255)
    C_STEEL_MID = (155, 170, 190, 255)
    C_STEEL_DARK = (90, 105, 125, 255)
    C_PARRY_ECHO = (120, 140, 200, 140)
    C_SPARK = (255, 225, 110, 255)
    
    for offset in [-3, 3]:
        echo_poly = [
            (35 + offset, 29), (48 + offset, 45), (42 + offset, 54),
            (37 + offset, 54), (38 + offset, 62), (32 + offset, 62),
            (33 + offset, 54), (28 + offset, 54), (22 + offset, 45)
        ]
        draw.polygon(echo_poly, outline=C_PARRY_ECHO)
        
    spade_poly = [
        (35, 28), (47, 44), (41, 53),
        (37, 53), (38, 63), (32, 63),
        (33, 53), (29, 53), (23, 44)
    ]
    draw.polygon(spade_poly, fill=C_STEEL_MID, outline=C_OUTLINE)
    
    left_facet = [(35, 29), (24, 44), (30, 52), (35, 52)]
    draw.polygon(left_facet, fill=C_STEEL_HL)
    
    right_facet = [(35, 29), (46, 44), (40, 52), (35, 52)]
    draw.polygon(right_facet, fill=C_STEEL_DARK)
    
    draw.line([(35, 28), (35, 53)], fill=C_OUTLINE, width=1)
    draw.line([(35, 29), (35, 48)], fill=C_WHITE, width=1)
    draw.line([(24, 44), (35, 29)], fill=C_WHITE, width=1)
    
    draw.rectangle([33, 53, 37, 63], fill=C_STEEL_DARK, outline=C_OUTLINE)
    draw.line([(34, 54), (34, 62)], fill=C_STEEL_HL)
    
    sparks = [
        (35, 24), (31, 23), (39, 22), (20, 42), (50, 41),
        (18, 47), (52, 48), (35, 20), (33, 17), (37, 18)
    ]
    for sx, sy in sparks:
        draw.point((sx, sy), fill=C_WHITE)
        draw.point((sx + 1, sy), fill=C_SPARK)
        draw.point((sx, sy + 1), fill=C_SPARK)
        
    export_sprite(img, "j_backlash.png")

def build_j_aftershock():
    """Builds Aftershock Joker (Clubs) - Heavy cracked stone club head impacting ground with seismic fissures."""
    img = create_card_base()
    draw = ImageDraw.Draw(img)
    
    bg_base = (35, 110, 85, 255)
    ring_color = (65, 160, 120, 255)
    ring_highlight = (165, 230, 190, 255)
    ring_dark = (20, 65, 48, 255)
    text_color = (255, 255, 255, 255)
    draw_kinetic_shockwaves(img, bg_base, ring_color, ring_highlight, ring_dark, text_color)
    
    C_OUTLINE = PALETTE["DEEP_OUTLINE"]
    C_WHITE = (255, 255, 255, 255)
    C_STONE_HL = (150, 175, 165, 255)
    C_STONE_MID = (95, 115, 108, 255)
    C_STONE_DARK = (52, 70, 64, 255)
    C_FISSURE = (16, 42, 32, 255)
    C_DUST = (175, 225, 190, 255)
    
    cracks = [
        [(35, 60), (30, 66), (24, 70), (17, 75)],
        [(35, 60), (41, 67), (48, 71), (54, 76)],
        [(35, 60), (35, 69), (33, 76), (36, 82)],
        [(30, 66), (28, 74), (22, 79)],
        [(41, 67), (44, 75), (49, 81)]
    ]
    for seg in cracks:
        for i in range(len(seg) - 1):
            draw.line([seg[i], seg[i+1]], fill=C_FISSURE, width=2)
            draw.line([(seg[i][0]+1, seg[i][1]), (seg[i+1][0]+1, seg[i+1][1])], fill=C_STONE_DARK, width=1)
            
    draw.ellipse([27, 28, 43, 44], fill=C_STONE_MID, outline=C_OUTLINE)
    draw.ellipse([19, 39, 35, 55], fill=C_STONE_MID, outline=C_OUTLINE)
    draw.ellipse([35, 39, 51, 55], fill=C_STONE_MID, outline=C_OUTLINE)
    
    draw.polygon([(32, 47), (38, 47), (40, 61), (30, 61)], fill=C_STONE_DARK, outline=C_OUTLINE)
    
    draw.ellipse([29, 30, 41, 42], fill=C_STONE_MID)
    draw.ellipse([21, 41, 33, 53], fill=C_STONE_MID)
    draw.ellipse([37, 41, 49, 53], fill=C_STONE_MID)
    draw.rectangle([30, 42, 40, 52], fill=C_STONE_MID)
    
    draw.arc([29, 30, 41, 42], start=180, end=300, fill=C_STONE_HL, width=2)
    draw.arc([21, 41, 33, 53], start=160, end=270, fill=C_STONE_HL, width=2)
    draw.arc([37, 41, 49, 53], start=270, end=360, fill=C_STONE_DARK, width=2)
    
    draw.line([(33, 31), (36, 36), (34, 40)], fill=C_OUTLINE)
    draw.line([(34, 31), (37, 36)], fill=C_STONE_HL)
    
    rubble = [
        ([(16, 56), (19, 54), (18, 59)], C_STONE_MID),
        ([(51, 57), (55, 55), (53, 60)], C_STONE_HL),
        ([(20, 66), (23, 64), (22, 68)], C_STONE_DARK),
        ([(47, 65), (50, 63), (49, 67)], C_STONE_MID),
    ]
    for r_poly, col in rubble:
        draw.polygon(r_poly, fill=col, outline=C_OUTLINE)
        
    dust_points = [(26, 61), (44, 61), (31, 63), (39, 63), (23, 63), (47, 63)]
    for dx, dy in dust_points:
        draw.point((dx, dy), fill=C_DUST)
        draw.point((dx, dy-1), fill=C_WHITE)
        
    export_sprite(img, "j_aftershock.png")

def build_j_sticky_note():
    """
    Builds Sticky Note Joker (Common).
    A bright canary yellow Post-it square with no white card border,
    pinned with a 3D red push-pin, featuring handwritten 'JOKER' in ink
    and a big, detailed doodled Jimbo face.
    """
    img = Image.new("RGBA", (71, 95), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([11, 16, 63, 83], fill=(35, 40, 45, 70))
    
    C_NOTE_YELLOW = (255, 245, 105, 255)
    C_NOTE_EDGE = (210, 195, 75, 255)
    
    draw.rectangle([8, 13, 62, 73], fill=C_NOTE_YELLOW, outline=C_NOTE_EDGE)
    draw.polygon([(8, 73), (54, 73), (54, 81), (8, 81)], fill=C_NOTE_YELLOW, outline=C_NOTE_EDGE)
    draw.rectangle([9, 14, 61, 80], fill=C_NOTE_YELLOW)
    
    draw.polygon([(54, 73), (62, 73), (54, 81)], fill=(185, 170, 55, 255))
    draw.polygon([(54, 73), (62, 81), (58, 79)], fill=(255, 250, 165, 255), outline=C_NOTE_EDGE)
    
    C_PIN_RED = (235, 35, 45, 255)
    C_PIN_DARK = (140, 15, 25, 255)
    C_PIN_HL = (255, 165, 170, 255)
    C_OUTLINE = (30, 37, 40, 255)
    
    draw.ellipse([36, 17, 42, 21], fill=(170, 155, 40, 220))
    draw.ellipse([31, 14, 39, 18], fill=C_PIN_DARK, outline=C_OUTLINE)
    draw.ellipse([32, 14, 38, 17], fill=C_PIN_RED)
    draw.ellipse([30, 8, 40, 13], fill=C_PIN_RED, outline=C_OUTLINE)
    draw.ellipse([31, 9, 39, 12], fill=C_PIN_RED)
    draw.ellipse([33, 9, 36, 11], fill=(255, 255, 255, 255))
    draw.point((32, 10), fill=C_PIN_HL)
    
    C_INK = (25, 42, 85, 255)
    C_INK_MED = (50, 70, 120, 255)
    
    # "JOKER"
    draw.line([(18, 20), (22, 20)], fill=C_INK)
    draw.line([(21, 20), (21, 25)], fill=C_INK)
    draw.point((20, 26), fill=C_INK)
    draw.point((19, 25), fill=C_INK)
    draw.ellipse([24, 20, 29, 26], outline=C_INK)
    draw.line([(32, 20), (32, 26)], fill=C_INK)
    draw.line([(32, 23), (36, 20)], fill=C_INK)
    draw.line([(33, 23), (36, 26)], fill=C_INK)
    draw.line([(39, 20), (39, 26)], fill=C_INK)
    draw.line([(39, 20), (43, 20)], fill=C_INK)
    draw.line([(39, 23), (42, 23)], fill=C_INK)
    draw.line([(39, 26), (43, 26)], fill=C_INK)
    draw.line([(46, 20), (46, 26)], fill=C_INK)
    draw.line([(46, 20), (50, 20)], fill=C_INK)
    draw.line([(50, 20), (51, 21), (51, 23), (50, 23), (46, 23)], fill=C_INK)
    draw.line([(48, 23), (51, 26)], fill=C_INK)
    
    # Doodled Jimbo
    draw.polygon([(29, 43), (35, 29), (41, 43)], outline=C_INK)
    draw.ellipse([33, 27, 37, 31], outline=C_INK, fill=C_INK_MED)
    draw.polygon([(30, 43), (17, 34), (19, 44), (28, 46)], outline=C_INK)
    draw.ellipse([16, 42, 20, 46], outline=C_INK, fill=C_INK_MED)
    draw.polygon([(40, 43), (53, 34), (51, 44), (42, 46)], outline=C_INK)
    draw.ellipse([50, 42, 54, 46], outline=C_INK, fill=C_INK_MED)
    
    draw.arc([24, 40, 46, 47], start=180, end=360, fill=C_INK, width=1)
    draw.ellipse([24, 43, 46, 63], outline=C_INK)
    
    draw.line([(27, 48), (32, 48)], fill=C_INK)
    draw.ellipse([28, 50, 31, 53], fill=C_INK)
    draw.line([(38, 48), (43, 48)], fill=C_INK)
    draw.ellipse([39, 50, 42, 53], fill=C_INK)
    
    draw.ellipse([33, 53, 37, 56], outline=C_INK)
    draw.arc([28, 52, 42, 61], start=10, end=170, fill=C_INK, width=2)
    draw.line([(27, 55), (28, 58)], fill=C_INK)
    draw.line([(43, 55), (42, 58)], fill=C_INK)
    
    ruffles = [
        [(21, 64), (27, 72), (32, 64)],
        [(30, 64), (35, 75), (40, 64)],
        [(38, 64), (43, 72), (49, 64)],
        [(16, 63), (21, 69), (25, 63)],
        [(45, 63), (49, 69), (54, 63)]
    ]
    for r_poly in ruffles:
        draw.polygon(r_poly, outline=C_INK)
        draw.line([r_poly[1], (r_poly[1][0], r_poly[1][1]-3)], fill=C_INK_MED)
        
    export_sprite(img, "j_sticky_note.png")

def generate_suit_swirl_background(stops):
    """Crops the uploaded swirl texture, resizes to 69x93 px, and maps to suit color ramp."""
    scratch_dir = os.path.join(BASE_DIR, "tools", "scratch")
    swirl_path = os.path.join(scratch_dir, "swirl_texture.png")
    swirl_raw = Image.open(swirl_path).convert("RGB")
    crop = swirl_raw.crop((70, 0, 484, 554))
    small = crop.resize((69, 93), Image.Resampling.LANCZOS)
    gray_arr = np.array(small.convert("L"), dtype=float)
    
    h, w = gray_arr.shape
    out = np.zeros((h, w, 4), dtype=np.uint8)
    for i in range(len(stops) - 1):
        v0, c0 = stops[i]
        v1, c1 = stops[i+1]
        mask = (gray_arr >= v0) & (gray_arr <= v1)
        t = (gray_arr[mask] - v0) / max(1e-5, (v1 - v0))
        for ch in range(3):
            out[mask, ch] = np.clip(c0[ch] + t * (c1[ch] - c0[ch]), 0, 255)
        out[mask, 3] = 255
    return Image.fromarray(out, "RGBA")

def create_adjective_card_base(swirl_stops):
    """
    Creates a 71x95 card with ZERO white outline:
    - Swirl background fills 69x93 at (1, 1) edge-to-edge
    - Standard Balatro outer dark outline (30, 37, 40)
    - Authentic vertical JOKER text
    """
    card = Image.new("RGBA", (71, 95), (0, 0, 0, 0))
    swirl = generate_suit_swirl_background(swirl_stops)
    card.paste(swirl, (1, 1))
    
    border_color = PALETTE["DEEP_OUTLINE"]
    draw = ImageDraw.Draw(card)
    draw.line([(3, 0), (67, 0)], fill=border_color)
    draw.line([(3, 94), (67, 94)], fill=border_color)
    draw.line([(0, 3), (0, 91)], fill=border_color)
    draw.line([(70, 3), (70, 91)], fill=border_color)
    corner_pixels = [
        ((1, 2), border_color), ((2, 1), border_color),
        ((69, 2), border_color), ((68, 1), border_color),
        ((1, 92), border_color), ((2, 93), border_color),
        ((69, 92), border_color), ((68, 93), border_color),
    ]
    for pt, col in corner_pixels:
        draw.point(pt, fill=col)
    for pt in [(0, 0), (1, 0), (0, 1), (70, 0), (69, 0), (70, 1), (0, 94), (1, 94), (0, 93), (70, 94), (69, 94), (70, 93), (1, 1), (69, 1), (1, 93), (69, 93)]:
        card.putpixel(pt, (0, 0, 0, 0))
        
    draw_vertical_joker_text(card, (255, 255, 255, 255))
    return card

def get_canonical_jimbo_bust():
    """Returns the authentic canonical Jimbo bust isolated with alpha transparency."""
    scratch_dir = os.path.join(BASE_DIR, "tools", "scratch")
    bust_path = os.path.join(scratch_dir, "perfect_jimbo_bust.png")
    bust = Image.open(bust_path).convert("RGBA")
    # Clean any hanging white-gray pixels under the chin/beard (y >= 53)
    for y in range(53, bust.height):
        for x in range(bust.width):
            p = bust.getpixel((x, y))
            if p[3] > 0 and (p[:3] in [(220, 220, 220), (255, 255, 255), (192, 192, 192)]):
                bust.putpixel((x, y), (0, 0, 0, 0))
    return bust

def build_j_frugal_joker():
    """
    Builds Frugal Joker (Diamonds):
    - Warm golden amber / honey swirl texture with zero white outline
    - Authentic Jimbo bust in golden amber hat & collar, gold bells
    - Sly calculating wink & gold tooth gleam
    """
    stops = [
        (0,   (80, 35, 10)),
        (65,  (175, 75, 15)),
        (135, (235, 140, 30)),
        (205, (255, 205, 80)),
        (255, (255, 245, 195))
    ]
    card = create_adjective_card_base(stops)
    bust = get_canonical_jimbo_bust()
    
    C_OUT = PALETTE["MID_SLATE"]
    C_WHITE = PALETTE["CARD_WHITE"]
    C_GOLD_TOOTH = (255, 215, 0, 255)
    
    for y in range(95):
        for x in range(71):
            p = bust.getpixel((x, y))
            if p[3] == 0: continue
            if p[:3] == (253, 95, 85) and y < 40:
                bust.putpixel((x, y), (235, 150, 40, 255))
            elif p[:3] == (253, 162, 0) and (x < 32 or x > 38 or y < 43):
                bust.putpixel((x, y), (255, 215, 60, 255))
            elif p[:3] == (223, 242, 253): bust.putpixel((x, y), (255, 238, 160, 255))
            elif p[:3] == (129, 206, 253): bust.putpixel((x, y), (250, 195, 80, 255))
            elif p[:3] == (0, 156, 253):   bust.putpixel((x, y), (225, 145, 30, 255))
            elif p[:3] == (0, 139, 227):   bust.putpixel((x, y), (165, 95, 15, 255))
            
    # Sly greedy wink on right eye & gold tooth
    bust.putpixel((38, 40), C_WHITE)
    bust.putpixel((39, 40), C_OUT)
    bust.putpixel((40, 40), C_OUT)
    bust.putpixel((41, 40), C_WHITE)
    bust.putpixel((38, 41), C_OUT)
    bust.putpixel((39, 41), C_WHITE)
    bust.putpixel((40, 41), C_WHITE)
    bust.putpixel((41, 41), C_OUT)
    bust.putpixel((33, 48), C_GOLD_TOOTH)
    bust.putpixel((34, 48), C_GOLD_TOOTH)
    
    card.alpha_composite(bust)
    export_sprite(card, "j_frugal_joker.png")

def build_j_fickle_joker():
    """
    Builds Fickle Joker (Hearts):
    - Candy rose / vivid ruby crimson swirl texture with zero white outline
    - Authentic Jimbo bust in ruby crimson hat & rose pink collar
    - Playful winking eye & blushing rosy cheeks
    """
    stops = [
        (0,   (90, 15, 25)),
        (65,  (185, 30, 50)),
        (135, (245, 75, 100)),
        (205, (255, 155, 175)),
        (255, (255, 235, 240))
    ]
    card = create_adjective_card_base(stops)
    bust = get_canonical_jimbo_bust()
    
    C_OUT = PALETTE["MID_SLATE"]
    C_WHITE = PALETTE["CARD_WHITE"]
    
    for y in range(95):
        for x in range(71):
            p = bust.getpixel((x, y))
            if p[3] == 0: continue
            if p[:3] == (253, 95, 85) and y < 40:
                bust.putpixel((x, y), (230, 40, 50, 255))
            elif p[:3] == (253, 162, 0) and (x < 32 or x > 38 or y < 43):
                bust.putpixel((x, y), (255, 120, 160, 255))
            elif p[:3] == (223, 242, 253): bust.putpixel((x, y), (255, 195, 215, 255))
            elif p[:3] == (129, 206, 253): bust.putpixel((x, y), (255, 130, 165, 255))
            elif p[:3] == (0, 156, 253):   bust.putpixel((x, y), (230, 45, 65, 255))
            elif p[:3] == (0, 139, 227):   bust.putpixel((x, y), (160, 20, 40, 255))
            elif p[:3] == (253, 162, 0) and y >= 40:
                bust.putpixel((x, y), (255, 110, 140, 255))
                
    # Playful wink on right eye
    bust.putpixel((38, 41), C_OUT)
    bust.putpixel((39, 41), C_OUT)
    bust.putpixel((40, 41), C_OUT)
    bust.putpixel((41, 41), C_OUT)
    bust.putpixel((39, 42), C_WHITE)
    bust.putpixel((40, 42), C_WHITE)
    
    card.alpha_composite(bust)
    export_sprite(card, "j_fickle_joker.png")

def build_j_stoic_joker():
    """
    Builds Stoic Joker (Spades):
    - Royal midnight navy / deep slate swirl texture with zero white outline
    - Authentic Jimbo bust in midnight navy hat & steel slate collar
    - Calm, resolute stoic straight mouth line & level steady brows
    """
    stops = [
        (0,   (20, 25, 55)),
        (65,  (50, 65, 115)),
        (135, (85, 115, 175)),
        (205, (160, 195, 240)),
        (255, (235, 245, 255))
    ]
    card = create_adjective_card_base(stops)
    bust = get_canonical_jimbo_bust()
    
    C_OUT = PALETTE["MID_SLATE"]
    C_WHITE = PALETTE["CARD_WHITE"]
    C_GREY = (220, 220, 220, 255)
    
    for y in range(95):
        for x in range(71):
            p = bust.getpixel((x, y))
            if p[3] == 0: continue
            if p[:3] == (253, 95, 85) and y < 40:
                bust.putpixel((x, y), (45, 65, 135, 255))
            elif p[:3] == (253, 162, 0) and (x < 32 or x > 38 or y < 43):
                bust.putpixel((x, y), (175, 195, 215, 255))
            elif p[:3] == (223, 242, 253): bust.putpixel((x, y), (200, 220, 240, 255))
            elif p[:3] == (129, 206, 253): bust.putpixel((x, y), (120, 150, 195, 255))
            elif p[:3] == (0, 156, 253):   bust.putpixel((x, y), (60, 85, 140, 255))
            elif p[:3] == (0, 139, 227):   bust.putpixel((x, y), (30, 45, 85, 255))
            
    # Calm level brows above eyes
    for bx in range(29, 33): bust.putpixel((bx, 39), C_OUT)
    for bx in range(38, 42): bust.putpixel((bx, 39), C_OUT)
    
    # Firm stoic straight mouth line
    for my in range(46, 52):
        for mx in range(28, 43):
            if bust.getpixel((mx, my))[3] > 0 and bust.getpixel((mx, my))[:3] != C_OUT:
                bust.putpixel((mx, my), C_WHITE)
    for mx in range(30, 41): bust.putpixel((mx, 48), C_OUT)
    bust.putpixel((29, 48), C_GREY)
    bust.putpixel((41, 48), C_GREY)
    bust.putpixel((35, 51), C_GREY)
    
    card.alpha_composite(bust)
    export_sprite(card, "j_stoic_joker.png")

def build_j_stubborn_joker():
    """
    Builds Stubborn Joker (Clubs):
    - Emerald jade / deep forest green swirl texture with zero white outline
    - Authentic Jimbo bust in deep forest green hat & moss collar, antique bronze bells
    - Tough furrowed brows & stubborn clenched teeth grin
    """
    stops = [
        (0,   (15, 55, 30)),
        (65,  (30, 105, 60)),
        (135, (55, 160, 100)),
        (205, (140, 220, 165)),
        (255, (230, 255, 240))
    ]
    card = create_adjective_card_base(stops)
    bust = get_canonical_jimbo_bust()
    
    C_OUT = PALETTE["MID_SLATE"]
    
    for y in range(95):
        for x in range(71):
            p = bust.getpixel((x, y))
            if p[3] == 0: continue
            if p[:3] == (253, 95, 85) and y < 40:
                bust.putpixel((x, y), (30, 125, 65, 255))
            elif p[:3] == (253, 162, 0) and (x < 32 or x > 38 or y < 43):
                bust.putpixel((x, y), (205, 160, 60, 255))
            elif p[:3] == (223, 242, 253): bust.putpixel((x, y), (165, 235, 180, 255))
            elif p[:3] == (129, 206, 253): bust.putpixel((x, y), (75, 180, 115, 255))
            elif p[:3] == (0, 156, 253):   bust.putpixel((x, y), (35, 130, 70, 255))
            elif p[:3] == (0, 139, 227):   bust.putpixel((x, y), (15, 75, 35, 255))
            
    # Furrowed brows
    bust.putpixel((29, 39), C_OUT)
    bust.putpixel((30, 39), C_OUT)
    bust.putpixel((31, 40), C_OUT)
    bust.putpixel((32, 40), C_OUT)
    bust.putpixel((38, 40), C_OUT)
    bust.putpixel((39, 40), C_OUT)
    bust.putpixel((40, 39), C_OUT)
    bust.putpixel((41, 39), C_OUT)
    
    # Clenched teeth
    for tx in [31, 33, 35, 37, 39]: bust.putpixel((tx, 48), C_OUT)
    
    card.alpha_composite(bust)
    export_sprite(card, "j_stubborn_joker.png")

def create_velvet_card(stops, seed=42):
    """
    Creates a 71x95 card with rich, plush undulating velvet drape background:
    - Zero white outline (fills 69x93 at (1, 1))
    - Authentic vertical 'JOKER' text
    - Outer Balatro dark border
    """
    w, h = 69, 93
    np.random.seed(seed)
    y, x = np.mgrid[0:h, 0:w].astype(float)
    ang1 = 0.65
    d1 = x * np.cos(ang1) + y * np.sin(ang1)
    wave1 = np.sin(d1 * 0.12)
    ang2 = -0.45
    d2 = x * np.cos(ang2) + y * np.sin(ang2)
    wave2 = np.sin(d2 * 0.16 + 1.2) * 0.55
    d3 = np.sqrt((x - 35)**2 + (y - 47)**2)
    wave3 = np.cos(d3 * 0.075) * 0.35
    folds = wave1 + wave2 + wave3
    folds = (folds - folds.min()) / (folds.max() - folds.min())
    velvet = folds ** 1.6
    noise = np.random.normal(0, 0.025, (h, w))
    velvet = np.clip(velvet + noise, 0, 1)
    
    val = velvet * 255.0
    out = np.zeros((h, w, 4), dtype=np.uint8)
    for i in range(len(stops) - 1):
        v0, c0 = stops[i]
        v1, c1 = stops[i+1]
        mask = (val >= v0) & (val <= v1)
        t = (val[mask] - v0) / max(1e-5, (v1 - v0))
        for ch in range(3):
            out[mask, ch] = np.clip(c0[ch] + t * (c1[ch] - c0[ch]), 0, 255)
        out[mask, 3] = 255
    velvet_img = Image.fromarray(out, "RGBA")
    
    card = Image.new("RGBA", (71, 95), (0, 0, 0, 0))
    card.paste(velvet_img, (1, 1))
    
    border_color = PALETTE["DEEP_OUTLINE"]
    draw = ImageDraw.Draw(card)
    draw.line([(3, 0), (67, 0)], fill=border_color)
    draw.line([(3, 94), (67, 94)], fill=border_color)
    draw.line([(0, 3), (0, 91)], fill=border_color)
    draw.line([(70, 3), (70, 91)], fill=border_color)
    corner_pixels = [
        ((1, 2), border_color), ((2, 1), border_color),
        ((69, 2), border_color), ((68, 1), border_color),
        ((1, 92), border_color), ((2, 93), border_color),
        ((69, 92), border_color), ((68, 93), border_color),
    ]
    for pt, col in corner_pixels:
        draw.point(pt, fill=col)
    for pt in [(0, 0), (1, 0), (0, 1), (70, 0), (69, 0), (70, 1), (0, 94), (1, 94), (0, 93), (70, 94), (69, 94), (70, 93), (1, 1), (69, 1), (1, 93), (69, 93)]:
        card.putpixel(pt, (0, 0, 0, 0))
        
    draw_vertical_joker_text(card, (255, 255, 255, 255))
    return card

def draw_gem_sparkle(draw, cx, cy, size=2, color=(255, 255, 255, 255)):
    draw.point((cx, cy), fill=color)
    for d in range(1, size + 1):
        draw.point((cx - d, cy), fill=color)
        draw.point((cx + d, cy), fill=color)
        draw.point((cx, cy - d), fill=color)
        draw.point((cx, cy + d), fill=color)

def build_j_ruby_heart():
    """
    Builds Ruby Heart (Hearts):
    - Royal burgundy / crimson plush velvet drape background
    - Brilliantly faceted heart-cut ruby gemstone with vivid crimson core,
      bright scarlet reflections, and sparkling white facet gleams
    """
    stops = [
        (0,   (60, 10, 20)),
        (70,  (135, 20, 35)),
        (145, (215, 35, 55)),
        (210, (255, 105, 125)),
        (255, (255, 205, 215))
    ]
    card = create_velvet_card(stops, seed=101)
    draw = ImageDraw.Draw(card)
    
    C_OUT = (40, 5, 10, 255)
    C_DARK = (120, 12, 25, 255)
    C_MID1 = (185, 20, 40, 255)
    C_MID2 = (225, 30, 55, 255)
    C_BRIGHT = (255, 55, 85, 255)
    C_HL = (255, 140, 160, 255)
    C_WHITE = (255, 255, 255, 255)
    
    # Outer drop shadow for dimensional gemstone depth
    shadow_poly = [(35, 31), (25, 26), (17, 34), (16, 44), (21, 56), (35, 71), (49, 56), (54, 44), (53, 34), (45, 26)]
    draw.polygon(shadow_poly, fill=(30, 5, 10, 190))
    
    # Upper left lobe facets
    draw.polygon([(35, 33), (26, 28), (35, 41)], fill=C_MID2, outline=C_OUT)
    draw.polygon([(26, 28), (18, 36), (28, 48), (35, 41)], fill=C_BRIGHT, outline=C_OUT)
    draw.polygon([(18, 36), (17, 44), (28, 48)], fill=C_MID1, outline=C_OUT)
    
    # Upper right lobe facets
    draw.polygon([(35, 33), (44, 28), (35, 41)], fill=C_MID1, outline=C_OUT)
    draw.polygon([(44, 28), (52, 36), (42, 48), (35, 41)], fill=C_DARK, outline=C_OUT)
    draw.polygon([(52, 36), (53, 44), (42, 48)], fill=C_MID1, outline=C_OUT)
    
    # Center Table facet (Large radiant heart kite)
    draw.polygon([(35, 41), (42, 48), (35, 59), (28, 48)], fill=C_BRIGHT, outline=C_OUT)
    draw.polygon([(32, 45), (38, 45), (35, 54)], fill=C_HL)
    draw.line([(31, 46), (37, 52)], fill=C_WHITE, width=1)
    
    # Lower pavilion facets
    draw.polygon([(28, 48), (17, 44), (21, 56), (28, 62)], fill=C_MID1, outline=C_OUT)
    draw.polygon([(28, 48), (28, 62), (35, 69), (35, 59)], fill=C_BRIGHT, outline=C_OUT)
    draw.polygon([(42, 48), (35, 59), (35, 69), (42, 62)], fill=C_DARK, outline=C_OUT)
    draw.polygon([(42, 48), (42, 62), (49, 56), (53, 44)], fill=C_MID2, outline=C_OUT)
    
    # Specular vertex and edge gleams
    draw.line([(26, 28), (35, 41)], fill=C_HL, width=1)
    draw.line([(28, 48), (35, 59)], fill=C_WHITE, width=1)
    draw.point((35, 33), fill=C_WHITE)
    draw.point((26, 28), fill=C_WHITE)
    draw.point((44, 28), fill=C_HL)
    draw.point((28, 48), fill=C_WHITE)
    draw.point((42, 48), fill=C_WHITE)
    draw.point((35, 69), fill=C_WHITE)
    
    # Sparkle stars
    draw_gem_sparkle(draw, 14, 27, size=2, color=C_WHITE)
    draw_gem_sparkle(draw, 56, 61, size=2, color=C_HL)
    
    export_sprite(card, "j_ruby_heart.png")

def build_j_black_diamond():
    """
    Builds Black Diamond (Spades):
    - Deep midnight obsidian / charcoal plush velvet drape background
    - Faceted Black Diamond with mirror jet-black table facet,
      brilliant steel-silver triangular crown reflections, and sharp white gleams
    """
    stops = [
        (0,   (15, 18, 24)),
        (70,  (38, 45, 58)),
        (145, (70, 82, 105)),
        (210, (135, 155, 185)),
        (255, (215, 228, 245))
    ]
    card = create_velvet_card(stops, seed=202)
    draw = ImageDraw.Draw(card)
    
    C_OUT = (10, 12, 15, 255)
    C_JET = (18, 21, 26, 255)
    C_DARK = (40, 46, 56, 255)
    C_STEEL = (75, 88, 105, 255)
    C_SILVER = (145, 162, 182, 255)
    C_LIGHT = (210, 225, 242, 255)
    C_WHITE = (255, 255, 255, 255)
    
    # Outer drop shadow
    shadow_poly = [(35, 23), (25, 34), (16, 46), (19, 57), (29, 60), (31, 71), (39, 71), (41, 60), (51, 57), (54, 46), (45, 34)]
    draw.polygon(shadow_poly, fill=(5, 8, 12, 190))
    
    # Crown Apex facets
    draw.polygon([(35, 25), (26, 36), (35, 35)], fill=C_LIGHT, outline=C_OUT)
    draw.polygon([(35, 25), (44, 36), (35, 35)], fill=C_STEEL, outline=C_OUT)
    draw.line([(35, 25), (35, 35)], fill=C_WHITE)
    
    # Shoulder facets
    draw.polygon([(26, 36), (18, 47), (28, 44), (35, 35)], fill=C_SILVER, outline=C_OUT)
    draw.polygon([(44, 36), (52, 47), (42, 44), (35, 35)], fill=C_DARK, outline=C_OUT)
    
    # Central Table Facet (Obsidian jet-black mirror)
    draw.polygon([(35, 35), (42, 44), (42, 53), (35, 57), (28, 53), (28, 44)], fill=C_JET, outline=C_OUT)
    draw.polygon([(30, 45), (37, 43), (34, 49)], fill=C_STEEL)
    draw.line([(30, 45), (36, 49)], fill=C_LIGHT, width=1)
    draw.point((32, 47), fill=C_WHITE)
    
    # Lower flank facets
    draw.polygon([(28, 44), (18, 47), (20, 56), (28, 53)], fill=C_STEEL, outline=C_OUT)
    draw.polygon([(42, 44), (52, 47), (50, 56), (42, 53)], fill=C_LIGHT, outline=C_OUT)
    
    # Inward cleft and spade stem facets
    draw.polygon([(28, 53), (20, 56), (29, 60), (35, 57)], fill=C_DARK, outline=C_OUT)
    draw.polygon([(42, 53), (50, 56), (41, 60), (35, 57)], fill=C_SILVER, outline=C_OUT)
    draw.polygon([(35, 57), (29, 60), (31, 70), (35, 66)], fill=C_SILVER, outline=C_OUT)
    draw.polygon([(35, 57), (41, 60), (39, 70), (35, 66)], fill=C_DARK, outline=C_OUT)
    draw.polygon([(31, 70), (39, 70), (35, 66)], fill=C_LIGHT, outline=C_OUT)
    
    # Vertex gleams
    draw.point((35, 25), fill=C_WHITE)
    draw.point((18, 47), fill=C_WHITE)
    draw.point((52, 47), fill=C_WHITE)
    draw.point((28, 44), fill=C_WHITE)
    draw.point((42, 44), fill=C_WHITE)
    draw.point((35, 57), fill=C_WHITE)
    draw.line([(42, 44), (52, 47)], fill=C_WHITE, width=1)
    
    # Sparkle stars
    draw_gem_sparkle(draw, 14, 30, size=2, color=C_WHITE)
    draw_gem_sparkle(draw, 56, 61, size=2, color=C_LIGHT)
    
    export_sprite(card, "j_black_diamond.png")

def build_j_linarite():
    """
    Builds Linarite (Clubs):
    - Royal azure / electric cyan plush velvet drape background
    - Radiant Trillion-cut Trefoil crystal in intense cerulean, cobalt,
      and vibrant electric cyan with internal prism rays and white gleams
    """
    stops = [
        (0,   (10, 30, 60)),
        (70,  (18, 75, 130)),
        (145, (28, 135, 195)),
        (210, (75, 205, 245)),
        (255, (200, 245, 255))
    ]
    card = create_velvet_card(stops, seed=303)
    draw = ImageDraw.Draw(card)
    
    C_OUT = (5, 20, 45, 255)
    C_NAVY = (15, 45, 95, 255)
    C_DEEP = (0, 85, 160, 255)
    C_MID = (0, 140, 215, 255)
    C_BRIGHT = (0, 190, 250, 255)
    C_CYAN = (90, 225, 255, 255)
    C_WHITE = (255, 255, 255, 255)
    
    # Top trillion lobe (cx=35, cy=33)
    draw.polygon([(35, 24), (25, 37), (45, 37)], fill=C_NAVY, outline=C_OUT)
    draw.polygon([(35, 24), (29, 36), (35, 35)], fill=C_CYAN, outline=C_OUT)
    draw.polygon([(35, 24), (41, 36), (35, 35)], fill=C_MID, outline=C_OUT)
    draw.polygon([(29, 36), (41, 36), (35, 35)], fill=C_BRIGHT, outline=C_OUT)
    draw.polygon([(25, 37), (29, 36), (35, 43), (35, 37)], fill=C_DEEP, outline=C_OUT)
    draw.polygon([(45, 37), (41, 36), (35, 43), (35, 37)], fill=C_MID, outline=C_OUT)
    
    # Left trillion lobe (cx=24, cy=48)
    draw.polygon([(14, 48), (28, 40), (28, 56)], fill=C_NAVY, outline=C_OUT)
    draw.polygon([(14, 48), (24, 43), (25, 48)], fill=C_CYAN, outline=C_OUT)
    draw.polygon([(14, 48), (24, 53), (25, 48)], fill=C_BRIGHT, outline=C_OUT)
    draw.polygon([(24, 43), (24, 53), (25, 48)], fill=C_WHITE, outline=C_OUT)
    draw.polygon([(28, 40), (24, 43), (35, 47)], fill=C_MID, outline=C_OUT)
    draw.polygon([(28, 56), (24, 53), (35, 47)], fill=C_DEEP, outline=C_OUT)
    
    # Right trillion lobe (cx=46, cy=48)
    draw.polygon([(56, 48), (42, 40), (42, 56)], fill=C_NAVY, outline=C_OUT)
    draw.polygon([(56, 48), (46, 43), (45, 48)], fill=C_DEEP, outline=C_OUT)
    draw.polygon([(56, 48), (46, 53), (45, 48)], fill=C_NAVY, outline=C_OUT)
    draw.polygon([(46, 43), (46, 53), (45, 48)], fill=C_MID, outline=C_OUT)
    draw.polygon([(42, 40), (46, 43), (35, 47)], fill=C_BRIGHT, outline=C_OUT)
    draw.polygon([(42, 56), (46, 53), (35, 47)], fill=C_DEEP, outline=C_OUT)
    
    # Central crystal knot
    draw.polygon([(35, 41), (41, 47), (35, 53), (29, 47)], fill=C_CYAN, outline=C_OUT)
    draw.polygon([(35, 43), (39, 47), (35, 51), (31, 47)], fill=C_WHITE)
    
    # Faceted crystal stem
    draw.polygon([(35, 53), (29, 58), (31, 68), (35, 65)], fill=C_MID, outline=C_OUT)
    draw.polygon([(35, 53), (41, 58), (39, 68), (35, 65)], fill=C_DEEP, outline=C_OUT)
    draw.polygon([(31, 68), (39, 68), (35, 65)], fill=C_CYAN, outline=C_OUT)
    
    # Vertex gleams
    draw.point((35, 24), fill=C_WHITE)
    draw.point((14, 48), fill=C_WHITE)
    draw.point((56, 48), fill=C_CYAN)
    draw.point((35, 41), fill=C_WHITE)
    draw.line([(14, 48), (24, 43)], fill=C_WHITE)
    draw.line([(35, 24), (29, 36)], fill=C_WHITE)
    
    # Sparkle stars
    draw_gem_sparkle(draw, 14, 33, size=2, color=C_CYAN)
    draw_gem_sparkle(draw, 56, 33, size=2, color=C_WHITE)
    
    export_sprite(card, "j_linarite.png")

def build_j_emerald():
    """
    Builds Emerald (Clubs):
    - Deep emerald green plush velvet drape background
    - Brilliant faceted 3-lobed Club gemstone in deep radiant emerald,
      mint facet reflections, central crystal knot, and white sparkle glints
    """
    stops = [
        (0,   (8, 38, 20)),
        (70,  (18, 85, 45)),
        (145, (30, 145, 75)),
        (210, (75, 215, 130)),
        (255, (195, 255, 220))
    ]
    card = create_velvet_card(stops, seed=505)
    draw = ImageDraw.Draw(card)
    
    C_OUT = (5, 25, 12, 255)
    C_DEEP = (10, 65, 32, 255)
    C_DARK = (20, 110, 55, 255)
    C_MID = (35, 165, 85, 255)
    C_BRIGHT = (65, 220, 120, 255)
    C_MINT = (150, 250, 190, 255)
    C_WHITE = (255, 255, 255, 255)
    
    # Drop shadow
    shadow_poly = [(35, 21), (23, 35), (13, 47), (20, 58), (29, 61), (31, 71), (39, 71), (41, 61), (50, 58), (57, 47), (47, 35)]
    draw.polygon(shadow_poly, fill=(5, 20, 10, 190))
    
    # 3-lobed Faceted Club Emerald
    # Top lobe (cx=35, cy=33)
    draw.polygon([(35, 24), (25, 37), (45, 37)], fill=C_DEEP, outline=C_OUT)
    draw.polygon([(35, 24), (29, 36), (35, 35)], fill=C_MINT, outline=C_OUT)
    draw.polygon([(35, 24), (41, 36), (35, 35)], fill=C_MID, outline=C_OUT)
    draw.polygon([(29, 36), (41, 36), (35, 35)], fill=C_BRIGHT, outline=C_OUT)
    draw.polygon([(25, 37), (29, 36), (35, 43), (35, 37)], fill=C_DARK, outline=C_OUT)
    draw.polygon([(45, 37), (41, 36), (35, 43), (35, 37)], fill=C_MID, outline=C_OUT)
    
    # Left lobe (cx=24, cy=48)
    draw.polygon([(14, 48), (28, 40), (28, 56)], fill=C_DEEP, outline=C_OUT)
    draw.polygon([(14, 48), (24, 43), (25, 48)], fill=C_MINT, outline=C_OUT)
    draw.polygon([(14, 48), (24, 53), (25, 48)], fill=C_BRIGHT, outline=C_OUT)
    draw.polygon([(24, 43), (24, 53), (25, 48)], fill=C_WHITE, outline=C_OUT)
    draw.polygon([(28, 40), (24, 43), (35, 47)], fill=C_MID, outline=C_OUT)
    draw.polygon([(28, 56), (24, 53), (35, 47)], fill=C_DARK, outline=C_OUT)
    
    # Right lobe (cx=46, cy=48)
    draw.polygon([(56, 48), (42, 40), (42, 56)], fill=C_DEEP, outline=C_OUT)
    draw.polygon([(56, 48), (46, 43), (45, 48)], fill=C_DARK, outline=C_OUT)
    draw.polygon([(56, 48), (46, 53), (45, 48)], fill=C_DEEP, outline=C_OUT)
    draw.polygon([(46, 43), (46, 53), (45, 48)], fill=C_MID, outline=C_OUT)
    draw.polygon([(42, 40), (46, 43), (35, 47)], fill=C_BRIGHT, outline=C_OUT)
    draw.polygon([(42, 56), (46, 53), (35, 47)], fill=C_DARK, outline=C_OUT)
    
    # Central crystal knot
    draw.polygon([(35, 41), (41, 47), (35, 53), (29, 47)], fill=C_MINT, outline=C_OUT)
    draw.polygon([(35, 43), (39, 47), (35, 51), (31, 47)], fill=C_WHITE)
    
    # Faceted crystal stem
    draw.polygon([(35, 53), (29, 58), (31, 68), (35, 65)], fill=C_MID, outline=C_OUT)
    draw.polygon([(35, 53), (41, 58), (39, 68), (35, 65)], fill=C_DARK, outline=C_OUT)
    draw.polygon([(31, 68), (39, 68), (35, 65)], fill=C_MINT, outline=C_OUT)
    
    # Vertex gleams
    draw.point((35, 24), fill=C_WHITE)
    draw.point((14, 48), fill=C_WHITE)
    draw.point((56, 48), fill=C_MINT)
    draw.point((35, 41), fill=C_WHITE)
    draw.line([(14, 48), (24, 43)], fill=C_WHITE)
    draw.line([(35, 24), (29, 36)], fill=C_WHITE)
    
    # Sparkle stars
    draw_gem_sparkle(draw, 14, 33, size=2, color=C_MINT)
    draw_gem_sparkle(draw, 56, 33, size=2, color=C_WHITE)
    
    export_sprite(card, "j_emerald.png")

def build_j_sphene():
    """
    Builds Sphene (Diamonds):
    - Warm golden amber / honey plush velvet drape background
    - Brilliant-cut Rhombus fire gemstone with glowing amber core,
      dazzling golden facets, signature yellow-green fire dispersion, and white gleams
    """
    stops = [
        (0,   (75, 35, 10)),
        (70,  (165, 90, 20)),
        (145, (225, 145, 35)),
        (210, (255, 205, 80)),
        (255, (255, 245, 185))
    ]
    card = create_velvet_card(stops, seed=404)
    draw = ImageDraw.Draw(card)
    
    C_OUT = (45, 20, 5, 255)
    C_AMBER_DARK = (130, 55, 10, 255)
    C_AMBER = (195, 95, 15, 255)
    C_GOLD = (245, 165, 25, 255)
    C_FIRE_LIME = (205, 230, 45, 255)
    C_YELLOW = (255, 215, 55, 255)
    C_HL = (255, 245, 150, 255)
    C_WHITE = (255, 255, 255, 255)
    
    # Drop shadow
    shadow_poly = [(35, 21), (15, 47), (35, 73), (55, 47)]
    draw.polygon(shadow_poly, fill=(35, 15, 5, 190))
    
    # Central diamond table facet
    draw.polygon([(35, 36), (44, 47), (35, 58), (26, 47)], fill=C_GOLD, outline=C_OUT)
    draw.polygon([(35, 39), (41, 47), (35, 55), (29, 47)], fill=C_YELLOW)
    draw.polygon([(35, 41), (39, 47), (35, 53), (31, 47)], fill=C_FIRE_LIME)
    draw.line([(31, 47), (39, 47)], fill=C_WHITE, width=1)
    draw.line([(35, 41), (35, 53)], fill=C_WHITE, width=1)
    
    # Top kite and bezel facets
    draw.polygon([(35, 23), (29, 35), (35, 36)], fill=C_FIRE_LIME, outline=C_OUT)
    draw.polygon([(35, 23), (41, 35), (35, 36)], fill=C_GOLD, outline=C_OUT)
    draw.polygon([(35, 23), (17, 47), (26, 47), (29, 35)], fill=C_YELLOW, outline=C_OUT)
    draw.polygon([(35, 23), (53, 47), (44, 47), (41, 35)], fill=C_AMBER, outline=C_OUT)
    
    # Bottom kite and bezel facets
    draw.polygon([(35, 71), (29, 59), (35, 58)], fill=C_GOLD, outline=C_OUT)
    draw.polygon([(35, 71), (41, 59), (35, 58)], fill=C_AMBER_DARK, outline=C_OUT)
    draw.polygon([(35, 71), (17, 47), (26, 47), (29, 59)], fill=C_AMBER, outline=C_OUT)
    draw.polygon([(35, 71), (53, 47), (44, 47), (41, 59)], fill=C_AMBER_DARK, outline=C_OUT)
    
    # Vertex and facet gleams
    draw.point((35, 23), fill=C_WHITE)
    draw.point((17, 47), fill=C_WHITE)
    draw.point((53, 47), fill=C_WHITE)
    draw.point((35, 71), fill=C_WHITE)
    draw.point((35, 36), fill=C_WHITE)
    draw.line([(35, 23), (29, 35)], fill=C_WHITE, width=1)
    draw.line([(17, 47), (26, 47)], fill=C_HL, width=1)
    
    # Sparkle stars
    draw_gem_sparkle(draw, 14, 31, size=2, color=C_WHITE)
    draw_gem_sparkle(draw, 56, 61, size=2, color=C_HL)
    
    export_sprite(card, "j_sphene.png")

def build_j_camera():
    """
    Builds Camera Joker (Polaroid Now+):
    - Matte black/charcoal plastic body with rounded silhouette and top-right viewfinder hump
    - Flash unit on top-left with frosted horizontal silver ribs
    - Bold circular red shutter button on middle-left
    - Giant center autofocus lens with stepped rings, cyan anti-reflective reflection arc, and white glint
    - Iconic 5-stripe Polaroid rainbow (Red, Orange, Yellow, Green, Blue) centered under lens
    - Viewfinder window and cyan plus feature button on right
    - Horizontal film ejection slot on bottom chin
    - Soft ground drop shadow beneath camera
    """
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from camera_sprite_builder import create_camera_1x
    img = create_camera_1x()
    export_sprite(img, "j_camera.png")

if __name__ == "__main__":
    print("Building all VanillaModedWorld assets...")
    build_mod_icon()
    build_j_espresso()
    build_c_the_mirror()
    build_c_the_weakness()
    build_c_swaper()
    build_c_phantasm()
    build_c_pact()
    build_j_wrong_schematics()
    build_j_magifect()
    build_j_stanczyk()
    build_j_doubler()
    build_b_echo()
    build_j_burnt_offering()
    build_j_jackpot()
    build_j_double_espresso()
    build_j_the_bell()
    build_sleeve_echo()
    build_j_lucky_clover()
    build_j_multifaces()
    build_j_bonus_stage()
    build_j_overdrive()
    build_j_kaleidoscope()
    build_j_glassblower()
    build_j_the_anvil()
    build_j_monolith()
    build_j_bullion()
    build_j_golden_horseshoe()
    build_j_fortune_cookie()
    build_j_hot_pepper()
    build_j_the_scythe()
    build_j_antivirus()
    build_j_sommers()
    build_v_market()
    build_v_supermarket()
    build_j_taxi_driver()
    build_j_river()
    build_j_stone_tablet()
    build_j_overkill()
    build_j_spotlight()
    build_j_short_circuit()
    build_j_ricochet()
    build_j_rebound()
    build_j_backlash()
    build_j_aftershock()
    build_j_sticky_note()
    build_j_frugal_joker()
    build_j_fickle_joker()
    build_j_stoic_joker()
    build_j_stubborn_joker()
    build_j_sphene()
    build_j_ruby_heart()
    build_j_black_diamond()
    build_j_linarite()
    build_j_emerald()
    build_j_camera()
