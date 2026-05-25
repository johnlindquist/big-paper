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
FONT_SIZE_TITLE = 42
FONT_SIZE_PUNCHLINE = 21
FONT_SIZE_LABEL = 20
FONT_SIZE_SPEC = 12

# Left margin
LEFT_MARGIN = 55

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

# Font paths (macOS default paths)
FONT_GEORGIA_BOLD = '/System/Library/Fonts/Supplemental/Georgia Bold.ttf'
FONT_GEORGIA_ITALIC = '/System/Library/Fonts/Supplemental/Georgia Italic.ttf'
FONT_MENLO_BOLD = '/System/Library/Fonts/Menlo.ttc'

def get_font(path, size):
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    else:
        logging.warning("Font file not found at %s. Falling back to default font. Layout may be degraded.", path)
        return ImageFont.load_default()

def generate_poster(base_img_path):
    # 1. Canvas setup - Grayscale (L mode)
    image = Image.new('L', (CANVAS_WIDTH, CANVAS_HEIGHT), 255)
    draw = ImageDraw.Draw(image)
    
    # 2. Get Fonts
    title_font = get_font(FONT_GEORGIA_BOLD, FONT_SIZE_TITLE)
    punchline_font = get_font(FONT_GEORGIA_ITALIC, FONT_SIZE_PUNCHLINE)
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
        logging.error("Base image not found at: %s", base_img_path)
        sys.exit(1)
        
    try:
        base_img = Image.open(base_img_path).convert('L')
    except (IOError, SyntaxError) as e:
        logging.error("Failed to load/parse image at %s: %s", base_img_path, e)
        sys.exit(1)
        
    # Resize and paste
    resized_img = base_img.resize((IMAGE_SIZE, IMAGE_SIZE), Image.Resampling.LANCZOS)
    image.paste(resized_img, (IMAGE_PASTE_X, IMAGE_PASTE_Y))

    # 6. Draw Left Column Text
    # Title
    draw.text((LEFT_MARGIN, 120), "THE", font=title_font, fill=0)
    draw.text((LEFT_MARGIN, 175), "UNGRILLABLE", font=title_font, fill=0)
    draw.text((LEFT_MARGIN, 230), "DEFENDANT", font=title_font, fill=0)
    
    # Thin divider line under title
    draw.line([(LEFT_MARGIN, 305), (DIVIDER_X - 30, 305)], fill=0, width=1)
    
    # Punchline / Subtitle
    punchline_lines = [
        "So many developers",
        "are using the /grill",
        "command wrong.",
        "",
        "Some questions are",
        "just not grillable.",
        "",
        "Video on this coming",
        "today."
    ]
    current_y = 330
    for line in punchline_lines:
        draw.text((LEFT_MARGIN, current_y), line, font=punchline_font, fill=0)
        current_y += 30
        
    # Technical Specifications at the bottom of the left column
    spec_y = 1180
    draw.line([(LEFT_MARGIN, spec_y - 20), (DIVIDER_X - 30, spec_y - 20)], fill=0, width=1)
    
    specs = [
        "FIG. 1057: LITIGATION MONITOR",
        "COURT: DISTRICT OF V-BUCKS",
        "DEFENSE: EPIC GAMES, INC.",
        "PROSECUTOR: WEBER KETTLE 500",
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

    # Label 1: Tim Sweeney (Defendant)
    draw_pointer(
        target=(750, 600),
        shelf_start=(520, 660),
        shelf_end=(680, 660),
        text="Defendant (Tim)",
        text_pos=(520, 630)
    )
    
    # Label 2: Hon. Barbecue Kettle (Prosecutor)
    draw_pointer(
        target=(1459, 462),
        shelf_start=(1520, 300),
        shelf_end=(1750, 300),
        text="Prosecutor (Weber)",
        text_pos=(1520, 270)
    )

    # 8. Save the Image
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'singularity-1057.png')
    image.save(output_path, 'PNG')
    logging.info("Successfully generated poster and saved to: %s", output_path)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("Usage: python3 %s <base_image_path>", sys.argv[0])
        sys.exit(1)
        
    generate_poster(sys.argv[1])
