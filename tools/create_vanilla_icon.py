"""
Generate a high-polish Balatro-style icon for Vanilla Moded World featuring a vanilla bean and orchid flower.
Outputs:
  - icon.png (32x32)
  - assets/1x/icon.png (32x32)
  - assets/2x/icon.png (64x64)
"""

from PIL import Image, ImageDraw

def create_vanilla_icon_32():
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Palette
    BORDER = (24, 30, 36, 255)         # Dark Balatro contour
    BG_OUTER = (34, 66, 58, 255)       # Rich deep pine/teal background
    BG_INNER = (44, 92, 80, 255)       # Lighter center gradient
    TEAL_ACCENT = (75, 194, 146, 255)  # Mod signature badge teal (#4BC292)
    
    # Vanilla Pods (dark chocolate / mahogany)
    POD_OUTLINE = (20, 12, 8, 255)
    POD_DARK = (45, 26, 16, 255)
    POD_MID = (75, 44, 28, 255)
    POD_LIGHT = (115, 68, 42, 255)
    POD_HILIGHT = (185, 130, 75, 255)
    POD_SEED = (15, 9, 6, 255)

    # Orchid Flower (creamy vanilla white & golden throat)
    PETAL_SHADOW = (180, 160, 125, 255)
    PETAL_MID = (225, 215, 185, 255)
    PETAL_LIGHT = (255, 250, 235, 255)
    PETAL_PURE = (255, 255, 255, 255)
    
    THROAT_DARK = (200, 120, 20, 255)
    THROAT_MID = (245, 175, 30, 255)
    THROAT_LIGHT = (255, 220, 80, 255)
    
    SPARKLE = (255, 240, 150, 255)
    SPARKLE_CORE = (255, 255, 255, 255)

    # 1. Base Tile with rounded corners
    # Outer dark border
    draw.rounded_rectangle([1, 1, 30, 30], radius=5, fill=BORDER)
    # Teal accent rim
    draw.rounded_rectangle([2, 2, 29, 29], radius=4, fill=TEAL_ACCENT)
    # Deep teal background
    draw.rounded_rectangle([3, 3, 28, 28], radius=3, fill=BG_OUTER)
    # Subtle radial/center highlight
    for y in range(8, 24):
        for x in range(8, 24):
            dx = x - 16
            dy = y - 16
            if dx*dx + dy*dy <= 45:
                img.putpixel((x, y), BG_INNER)

    # 2. Draw Two Crossing Vanilla Beans (slender curved pods)
    # Bean 1: sweeping from bottom-left (5, 26) up to top-right (26, 7)
    # Bean 2: sweeping from bottom-right (26, 25) up to top-left (7, 8)
    
    # Path for Bean 1 (Bottom-left to top-right)
    bean1_pts = [
        (5, 26), (6, 25), (7, 24), (8, 23), (9, 22), (10, 20), (11, 19), 
        (12, 17), (13, 16), (14, 15), (15, 14), (16, 13), (17, 12), (18, 11),
        (19, 10), (20, 9), (21, 8), (22, 7), (23, 7), (24, 7), (25, 8)
    ]
    # Draw bean 1 body with outline and shading
    for pt in bean1_pts:
        x, y = pt
        # Outline
        for ox in (-1, 0, 1):
            for oy in (-1, 0, 1):
                if 2 <= x+ox <= 29 and 2 <= y+oy <= 29:
                    curr = img.getpixel((x+ox, y+oy))
                    if curr in (BG_OUTER, BG_INNER, TEAL_ACCENT):
                        img.putpixel((x+ox, y+oy), POD_OUTLINE)

    for pt in bean1_pts:
        x, y = pt
        img.putpixel((x, y), POD_MID)
        if x+1 <= 29:
            img.putpixel((x+1, y), POD_DARK)
        if y-1 >= 2 and (x % 3 != 0):
            img.putpixel((x, y-1), POD_LIGHT)

    # Path for Bean 2 (Bottom-right to top-left with curved tip)
    bean2_pts = [
        (26, 26), (25, 25), (24, 24), (23, 23), (22, 21), (21, 20), (20, 18),
        (19, 17), (18, 16), (17, 15), (16, 14), (15, 13), (14, 12), (13, 11),
        (12, 10), (11, 9), (10, 8), (9, 7), (8, 7), (7, 8), (6, 9)
    ]
    for pt in bean2_pts:
        x, y = pt
        for ox in (-1, 0, 1):
            for oy in (-1, 0, 1):
                if 2 <= x+ox <= 29 and 2 <= y+oy <= 29:
                    curr = img.getpixel((x+ox, y+oy))
                    if curr in (BG_OUTER, BG_INNER, TEAL_ACCENT):
                        img.putpixel((x+ox, y+oy), POD_OUTLINE)

    for pt in bean2_pts:
        x, y = pt
        img.putpixel((x, y), POD_LIGHT)
        if x+1 <= 29 and y+1 <= 29:
            img.putpixel((x+1, y+1), POD_DARK)
        if x-1 >= 2:
            img.putpixel((x-1, y), POD_MID)

    # Bean highlight ridges
    for pt in [(11, 9), (13, 11), (15, 13), (18, 16), (21, 20), (23, 23)]:
        img.putpixel(pt, POD_HILIGHT)

    # Hooked tips on beans
    img.putpixel((5, 27), POD_OUTLINE)
    img.putpixel((6, 27), POD_MID)
    img.putpixel((26, 27), POD_OUTLINE)
    img.putpixel((25, 27), POD_MID)

    # 3. Vanilla Orchid Flower in the center (center at x=16, y=16)
    # The orchid has 5 distinct petals:
    # - Top dorsal sepal: extends up (x=16, y=10..13)
    # - Left upper petal: extends up-left (x=10..14, y=12..15)
    # - Right upper petal: extends up-right (x=18..22, y=12..15)
    # - Left lower sepal: extends down-left (x=11..14, y=17..20)
    # - Right lower sepal: extends down-right (x=18..21, y=17..20)
    # - Center labellum (throat/lip): golden trumpet (x=15..17, y=15..18)

    flower_pixels = {
        # Top sepal
        (16, 9): PETAL_SHADOW,
        (15, 10): PETAL_SHADOW, (16, 10): PETAL_PURE, (17, 10): PETAL_SHADOW,
        (15, 11): PETAL_MID,    (16, 11): PETAL_PURE, (17, 11): PETAL_LIGHT,
        (15, 12): PETAL_MID,    (16, 12): PETAL_LIGHT, (17, 12): PETAL_LIGHT,

        # Left petal
        (10, 13): PETAL_SHADOW,
        (11, 12): PETAL_SHADOW, (11, 13): PETAL_PURE, (11, 14): PETAL_SHADOW,
        (12, 12): PETAL_LIGHT,  (12, 13): PETAL_PURE, (12, 14): PETAL_MID,
        (13, 13): PETAL_LIGHT,  (13, 14): PETAL_MID,

        # Right petal
        (22, 13): PETAL_SHADOW,
        (21, 12): PETAL_SHADOW, (21, 13): PETAL_PURE, (21, 14): PETAL_SHADOW,
        (20, 12): PETAL_LIGHT,  (20, 13): PETAL_PURE, (20, 14): PETAL_MID,
        (19, 13): PETAL_LIGHT,  (19, 14): PETAL_MID,

        # Left bottom sepal
        (11, 19): PETAL_SHADOW,
        (12, 18): PETAL_SHADOW, (12, 19): PETAL_LIGHT, (12, 20): PETAL_SHADOW,
        (13, 17): PETAL_MID,    (13, 18): PETAL_LIGHT, (13, 19): PETAL_MID,
        (14, 17): PETAL_MID,    (14, 18): PETAL_LIGHT,

        # Right bottom sepal
        (21, 19): PETAL_SHADOW,
        (20, 18): PETAL_SHADOW, (20, 19): PETAL_LIGHT, (20, 20): PETAL_SHADOW,
        (19, 17): PETAL_MID,    (19, 18): PETAL_LIGHT, (19, 19): PETAL_MID,
        (18, 17): PETAL_MID,    (18, 18): PETAL_LIGHT,

        # Center golden throat / labellum (orchid trumpet)
        (15, 14): THROAT_MID,   (16, 14): THROAT_LIGHT, (17, 14): THROAT_MID,
        (15, 15): THROAT_MID,   (16, 15): THROAT_LIGHT, (17, 15): THROAT_MID,
        (15, 16): THROAT_DARK,  (16, 16): THROAT_LIGHT, (17, 16): THROAT_DARK,
        (16, 17): THROAT_DARK,
        # Tiny white pistil glint in throat
        (16, 15): (255, 255, 255, 255),
    }

    # Add dark drop outline around flower petals for crisp pop
    for (fx, fy) in flower_pixels:
        for ox in (-1, 0, 1):
            for oy in (-1, 0, 1):
                pos = (fx + ox, fy + oy)
                if pos not in flower_pixels and 2 <= pos[0] <= 29 and 2 <= pos[1] <= 29:
                    c = img.getpixel(pos)
                    if c not in (BORDER, TEAL_ACCENT, POD_OUTLINE, POD_DARK):
                        img.putpixel(pos, (18, 22, 20, 255))

    # Apply flower pixels
    for (fx, fy), col in flower_pixels.items():
        img.putpixel((fx, fy), col)

    # 4. Magical Balatro Sparkles
    # Top-right sparkle (diamond 4-point star)
    sp1 = [(25, 5), (24, 6), (25, 6), (26, 6), (25, 7)]
    for pt in sp1:
        img.putpixel(pt, SPARKLE)
    img.putpixel((25, 6), SPARKLE_CORE)

    # Bottom-left mini sparkle
    sp2 = [(6, 16), (7, 16), (6, 17)]
    for pt in sp2:
        img.putpixel(pt, SPARKLE)
    img.putpixel((6, 16), SPARKLE_CORE)

    return img

if __name__ == "__main__":
    icon_32 = create_vanilla_icon_32()
    # 2x nearest-neighbor scale for 64x64
    icon_64 = icon_32.resize((64, 64), Image.Resampling.NEAREST)

    icon_32.save("icon.png")
    icon_32.save("assets/1x/icon.png")
    icon_64.save("assets/2x/icon.png")
    print("Vanilla bean icon generated successfully!")
