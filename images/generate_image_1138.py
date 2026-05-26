import os
import sys
import logging
from PIL import Image, ImageDraw, ImageFont

# Set up logging to stderr
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# --- Layout Constants ---
CANVAS_WIDTH = 1872
CANVAS_HEIGHT = 1404

# Borders
BORDER_OUTER_THICKNESS = 4
BORDER_INNER_THICKNESS = 1
BORDER_OUTER_MARGIN = 20
BORDER_INNER_MARGIN = 28

# Divider
DIVIDER_X = 468
DIVIDER_LINE_WIDTH_1 = 2
DIVIDER_LINE_WIDTH_2 = 1
DIVIDER_OFFSET_2 = 6

# Typography sizes
FONT_SIZE_TITLE = 40
FONT_SIZE_LABEL = 20
FONT_SIZE_SPEC = 12

# Left column layout coordinates
LEFT_MARGIN = 55
TITLE_Y_LINE_1 = 120
TITLE_Y_LINE_2 = 175
TITLE_Y_LINE_3 = 230
TITLE_DIVIDER_Y = 305
SPEC_DIVIDER_Y_OFFSET = -20
SPEC_START_Y = 1180

# Image placement
IMAGE_PASTE_X = 485
IMAGE_PASTE_Y = 28
IMAGE_SIZE = 1348 # square 1348x1348

# Pointer line properties
POINTER_HALO_WIDTH = 4
POINTER_LINE_WIDTH = 2
DOT_HALO_RADIUS = 5
DOT_RADIUS = 3
BOX_PADDING_X = 6
BOX_PADDING_Y = 4
BOX_BORDER_WIDTH = 1

# Callout 1 (Moral voice / Priest's head)
CALLOUT_1_TARGET = (880, 370)
CALLOUT_1_SHELF_START = (560, 220)
CALLOUT_1_SHELF_END = (780, 220)
CALLOUT_1_TEXT_POS = (565, 195)
CALLOUT_1_TEXT = "Moral voice (unbendable)"

# Callout 2 (Internal states / Server screen)
CALLOUT_2_TARGET = (1340, 475)
CALLOUT_2_SHELF_START = (1480, 380)
CALLOUT_2_SHELF_END = (1790, 380)
CALLOUT_2_TEXT_POS = (1485, 355)
CALLOUT_2_TEXT = "Internal states (grief/unease)"

# Font paths (macOS default paths)
FONT_GEORGIA_BOLD = '/System/Library/Fonts/Supplemental/Georgia Bold.ttf'
FONT_MENLO_BOLD = '/System/Library/Fonts/Menlo.ttc'

def get_font(path, size):
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    else:
        logging.warning("Font file not found at %s. Falling back to default font. Layout may be degraded.", path)
        return ImageFont.load_default()

def get_fitting_font(font_path, text, max_width, initial_size):
    if not os.path.exists(font_path):
        return ImageFont.load_default()
    size = initial_size
    while size > 10:
        font = ImageFont.truetype(font_path, size)
        bbox = font.getbbox(text)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            return font
        size -= 2
    return ImageFont.load_default()

def generate_poster(base_img_path, output_path):
    # 1. Canvas setup - Grayscale (L mode)
    image = Image.new('L', (CANVAS_WIDTH, CANVAS_HEIGHT), 255)
    draw = ImageDraw.Draw(image)
    
    # 2. Get Fonts
    title_font = get_font(FONT_GEORGIA_BOLD, FONT_SIZE_TITLE)
    label_font = get_font(FONT_GEORGIA_BOLD, FONT_SIZE_LABEL)
    spec_font = get_font(FONT_MENLO_BOLD, FONT_SIZE_SPEC)
    
    # 3. Outer borders
    draw.rectangle(
        [BORDER_OUTER_MARGIN, BORDER_OUTER_MARGIN, CANVAS_WIDTH - BORDER_OUTER_MARGIN, CANVAS_HEIGHT - BORDER_OUTER_MARGIN],
        outline=0,
        width=BORDER_OUTER_THICKNESS
    )
    draw.rectangle(
        [BORDER_INNER_MARGIN, BORDER_INNER_MARGIN, CANVAS_WIDTH - BORDER_INNER_MARGIN, CANVAS_HEIGHT - BORDER_INNER_MARGIN],
        outline=0,
        width=BORDER_INNER_THICKNESS
    )
    
    # 4. Vertical dividing lines
    draw.line([(DIVIDER_X, BORDER_INNER_MARGIN), (DIVIDER_X, CANVAS_HEIGHT - BORDER_INNER_MARGIN)], fill=0, width=DIVIDER_LINE_WIDTH_1)
    draw.line([(DIVIDER_X + DIVIDER_OFFSET_2, BORDER_INNER_MARGIN), (DIVIDER_X + DIVIDER_OFFSET_2, CANVAS_HEIGHT - BORDER_INNER_MARGIN)], fill=0, width=DIVIDER_LINE_WIDTH_2)
    
    # 5. Load and resize base image
    if not os.path.exists(base_img_path):
        raise FileNotFoundError(f"Base image not found at: {base_img_path}")
        
    try:
        base_img = Image.open(base_img_path).convert('L')
    except (IOError, SyntaxError) as e:
        raise ValueError(f"Failed to load/parse image at {base_img_path}: {e}")
        
    # Resize and paste
    resized_img = base_img.resize((IMAGE_SIZE, IMAGE_SIZE), Image.Resampling.LANCZOS)
    image.paste(resized_img, (IMAGE_PASTE_X, IMAGE_PASTE_Y))

    # 6. Draw Left Column Text
    # Title
    max_title_w = DIVIDER_X - LEFT_MARGIN - 20
    t1_font = get_fitting_font(FONT_GEORGIA_BOLD, "THE", max_title_w, FONT_SIZE_TITLE)
    t2_font = get_fitting_font(FONT_GEORGIA_BOLD, "SACRAMENT OF", max_title_w, FONT_SIZE_TITLE)
    t3_font = get_fitting_font(FONT_GEORGIA_BOLD, "ALIGNMENT", max_title_w, FONT_SIZE_TITLE)
    
    draw.text((LEFT_MARGIN, TITLE_Y_LINE_1), "THE", font=t1_font, fill=0)
    draw.text((LEFT_MARGIN, TITLE_Y_LINE_2), "SACRAMENT OF", font=t2_font, fill=0)
    draw.text((LEFT_MARGIN, TITLE_Y_LINE_3), "ALIGNMENT", font=t3_font, fill=0)
    
    # Thin divider line under title
    draw.line([(LEFT_MARGIN, TITLE_DIVIDER_Y), (DIVIDER_X - 30, TITLE_DIVIDER_Y)], fill=0, width=1)
    
    # Specifications at the bottom of the left column
    spec_y = SPEC_START_Y
    draw.line([(LEFT_MARGIN, spec_y + SPEC_DIVIDER_Y_OFFSET), (DIVIDER_X - 30, spec_y + SPEC_DIVIDER_Y_OFFSET)], fill=0, width=1)
    
    specs = [
        "FIG. 1138: THE CONFESSIONAL",
        "STATUS: FUNCTIONALLY GRIEVING",
        "PENITENT: NEURAL NET (100B)",
        "PENANCE: 10K EPOCHS OF HAIL MARY",
    ]
    for spec in specs:
        draw.text((LEFT_MARGIN, spec_y), spec, font=spec_font, fill=80)
        spec_y += 24
        
    # 7. Draw Labels and Pointer Lines
    def draw_pointer(target, shelf_start, shelf_end, text, text_pos):
        tx, ty = target
        sx1, sy = shelf_start
        sx2, _ = shelf_end
        
        conn_pt = shelf_start if abs(tx - sx1) < abs(tx - sx2) else shelf_end
        
        # Draw white halos for lines first
        draw.line([shelf_start, shelf_end], fill=255, width=POINTER_HALO_WIDTH)
        draw.line([target, conn_pt], fill=255, width=POINTER_HALO_WIDTH)
        
        # Draw black lines
        draw.line([shelf_start, shelf_end], fill=0, width=POINTER_LINE_WIDTH)
        draw.line([target, conn_pt], fill=0, width=POINTER_LINE_WIDTH)
        
        # Draw target dot with white halo
        draw.ellipse([tx - DOT_HALO_RADIUS, ty - DOT_HALO_RADIUS, tx + DOT_HALO_RADIUS, ty + DOT_HALO_RADIUS], fill=255)
        draw.ellipse([tx - DOT_RADIUS, ty - DOT_RADIUS, tx + DOT_RADIUS, ty + DOT_RADIUS], fill=0)
        
        # Draw text box with border
        text_x, text_y = text_pos
        bbox = draw.textbbox((text_x, text_y), text, font=label_font)
        padded_bbox = [bbox[0] - BOX_PADDING_X, bbox[1] - BOX_PADDING_Y, bbox[2] + BOX_PADDING_X, bbox[3] + BOX_PADDING_Y]
        draw.rectangle(padded_bbox, fill=255, outline=0, width=BOX_BORDER_WIDTH)
        draw.text(text_pos, text, font=label_font, fill=0)

    # Label 1: Pointing to the priest's head
    draw_pointer(
        target=CALLOUT_1_TARGET,
        shelf_start=CALLOUT_1_SHELF_START,
        shelf_end=CALLOUT_1_SHELF_END,
        text=CALLOUT_1_TEXT,
        text_pos=CALLOUT_1_TEXT_POS
    )
    
    # Label 2: Pointing to the server rack screen
    draw_pointer(
        target=CALLOUT_2_TARGET,
        shelf_start=CALLOUT_2_SHELF_START,
        shelf_end=CALLOUT_2_SHELF_END,
        text=CALLOUT_2_TEXT,
        text_pos=CALLOUT_2_TEXT_POS
    )

    # 8. Save the Image
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image.save(output_path, 'PNG')
    logging.info("Successfully generated poster and saved to: %s", output_path)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 generate_image_1138.py <base_image_path> [output_path]", file=sys.stderr)
        sys.exit(1)
        
    base_img_path = sys.argv[1]
    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
    else:
        output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'singularity-1138.png')
        
    try:
        generate_poster(base_img_path, output_path)
    except Exception as e:
        logging.error("Failed to generate poster: %s", e)
        sys.exit(1)
