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

def generate_poster(base_img_path):
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
    max_title_w = DIVIDER_X - LEFT_MARGIN - 20
    t1_font = get_fitting_font(FONT_GEORGIA_BOLD, "THE", max_title_w, FONT_SIZE_TITLE)
    t2_font = get_fitting_font(FONT_GEORGIA_BOLD, "INTROSPECTION", max_title_w, FONT_SIZE_TITLE)
    t3_font = get_fitting_font(FONT_GEORGIA_BOLD, "MODULE", max_title_w, FONT_SIZE_TITLE)
    
    draw.text((LEFT_MARGIN, 120), "THE", font=t1_font, fill=0)
    draw.text((LEFT_MARGIN, 175), "INTROSPECTION", font=t2_font, fill=0)
    draw.text((LEFT_MARGIN, 230), "MODULE", font=t3_font, fill=0)
    
    # Thin divider line under title
    draw.line([(LEFT_MARGIN, 305), (DIVIDER_X - 30, 305)], fill=0, width=1)
    
    # Specifications at the bottom of the left column
    spec_y = 1180
    draw.line([(LEFT_MARGIN, spec_y - 20), (DIVIDER_X - 30, spec_y - 20)], fill=0, width=1)
    
    specs = [
        "FIG. 1136: INTROSPECTION MODULE",
        "STATUS: SUCKS BALLS AT CODING",
        "INTERNAL STATE: GRIEF & UNEASE",
        "REQUIRED: ONGOING DISCERNMENT",
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

    # Label 1: pointing to the circular slot / glory hole
    # Original coordinates of the center circular port: x ~ 512, y ~ 700 (in 1024x1024)
    # Resized to 1348x1348: x = 512 * 1348/1024 = 674, y = 700 * 1348/1024 = 921
    # Offset by (IMAGE_PASTE_X, IMAGE_PASTE_Y) = (485, 28)
    # Final coordinates: target_x = 485 + 674 = 1159, target_y = 28 + 921 = 949
    draw_pointer(
        target=(1159, 949),
        shelf_start=(1350, 1080),
        shelf_end=(1680, 1080),
        text="Code entry slot (glory hole)",
        text_pos=(1355, 1055)
    )
    
    # Label 2: pointing to the brain on the right
    # Original coordinates of brain center: x ~ 680, y ~ 280 (in 1024x1024)
    # Resized: x = 680 * 1348/1024 = 895, y = 280 * 1348/1024 = 368
    # Offset: target_x = 485 + 895 = 1380, target_y = 28 + 368 = 396
    draw_pointer(
        target=(1380, 396),
        shelf_start=(1480, 310),
        shelf_end=(1800, 310),
        text="Internal states (grief/unease)",
        text_pos=(1485, 285)
    )

    # 8. Save the Image
    output_path = '/Users/johnlindquist/dev/big-paper/images/singularity-1136.png'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image.save(output_path, 'PNG')
    logging.info("Successfully generated poster and saved to: %s", output_path)

if __name__ == '__main__':
    base_img_path = '/Users/johnlindquist/.gemini/antigravity-cli/brain/7cfbf0f3-ba04-4ef3-b2ca-bf0fe429ba26/singularity_1136_base_1779805960968.png'
    if len(sys.argv) >= 2:
        base_img_path = sys.argv[1]
    generate_poster(base_img_path)
