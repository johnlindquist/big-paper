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
DIVIDER_X = 488
DIVIDER_LINE_WIDTH_1 = 2
DIVIDER_LINE_WIDTH_2 = 1
DIVIDER_OFFSET_2 = 6

# Left margin
LEFT_MARGIN = 55

# Image placement
IMAGE_PASTE_X = 496
IMAGE_PASTE_Y = 28
IMAGE_SIZE = 1348 # square 1348x1348

# Typography sizes
FONT_SIZE_TITLE = 42
FONT_SIZE_PUNCHLINE = 21
FONT_SIZE_LABEL = 20
FONT_SIZE_SPEC = 12

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
    
    # 5. Load and resize the generated base image
    if not os.path.exists(base_img_path):
        logging.error("Base image not found at: %s", base_img_path)
        sys.exit(1)
        
    try:
        base_img = Image.open(base_img_path).convert('L')
    except (IOError, SyntaxError) as e:
        logging.error("Failed to load/parse image at %s: %s", base_img_path, e)
        sys.exit(1)
        
    # Resize and paste flush with vertical divider and inner border
    resized_img = base_img.resize((IMAGE_SIZE, IMAGE_SIZE), Image.Resampling.LANCZOS)
    image.paste(resized_img, (IMAGE_PASTE_X, IMAGE_PASTE_Y))

    # 6. Draw Left Column Text (x: 28 to 488)
    # Title
    draw.text((LEFT_MARGIN, 120), "THE", font=title_font, fill=0)
    draw.text((LEFT_MARGIN, 175), "DELIVERY", font=title_font, fill=0)
    draw.text((LEFT_MARGIN, 230), "PARADOX", font=title_font, fill=0)
    
    # Thin divider line under title
    draw.line([(LEFT_MARGIN, 305), (DIVIDER_X - 30, 305)], fill=0, width=1)
    
    # Punchline / Subtitle
    punchline_lines = [
        "Sonnet 5 writes the",
        "entire app in seconds.",
        "",
        "App review approves",
        "the update in weeks.",
        "",
        "The open web remains",
        "instantly grateful."
    ]
    current_y = 330
    for line in punchline_lines:
        draw.text((LEFT_MARGIN, current_y), line, font=punchline_font, fill=0)
        current_y += 30
        
    # Technical Specifications at the bottom of the left column
    spec_y = 1180
    draw.line([(LEFT_MARGIN, spec_y - 20), (DIVIDER_X - 30, spec_y - 20)], fill=0, width=1)
    
    specs = [
        "FIG. 1087: DELIVERY PARADOX",
        "BUILD RATE: 100% DEPLOY SPEED",
        "REVIEW RATE: SNAIL VELOCITY",
        "PROTOCOL: FREEDOM OF THE WEB",
    ]
    for spec in specs:
        draw.text((LEFT_MARGIN, spec_y), spec, font=spec_font, fill=80)
        spec_y += 24
        
    # 7. Draw Labels and Pointer Lines
    def draw_pointer(target, shelf_start, shelf_end, text, text_pos):
        tx, ty = target
        # White halo for target dot
        draw.ellipse([tx - 6, ty - 6, tx + 6, ty + 6], fill=255)
        # Black target dot
        draw.ellipse([tx - 4, ty - 4, tx + 4, ty + 4], fill=0)
        
        sx1, sy = shelf_start
        sx2, _ = shelf_end
        
        # Draw white halos for lines first to mask the background image lines
        draw.line([shelf_start, shelf_end], fill=255, width=4)
        if abs(tx - sx1) < abs(tx - sx2):
            draw.line([target, shelf_start], fill=255, width=4)
        else:
            draw.line([target, shelf_end], fill=255, width=4)
            
        # Draw black lines
        draw.line([shelf_start, shelf_end], fill=0, width=2)
        if abs(tx - sx1) < abs(tx - sx2):
            draw.line([target, shelf_start], fill=0, width=2)
        else:
            draw.line([target, shelf_end], fill=0, width=2)
            
        # Draw text with a clean white background rectangle to mask out background lines
        text_x, text_y = text_pos
        bbox = draw.textbbox((text_x, text_y), text, font=label_font)
        padded_bbox = [bbox[0] - 8, bbox[1] - 6, bbox[2] + 8, bbox[3] + 6]
        draw.rectangle(padded_bbox, fill=255, outline=0, width=1)
        
        # Draw text
        draw.text(text_pos, text, font=label_font, fill=0)

    # Label 1: Awaiting Review (pointing to robot)
    # Robot's head is at x=270, y=480 in the 1024x1024 original.
    # In 1348x1348 pasted at (496, 28):
    # x = 496 + 270 * (1348/1024) = 496 + 355 = 851
    # y = 28 + 480 * (1348/1024) = 28 + 631 = 659
    draw_pointer(
        target=(851, 659),
        shelf_start=(550, 520),
        shelf_end=(750, 520),
        text="Awaiting Review",
        text_pos=(560, 490)
    )
    
    # Label 2: Instant Deploy (pointing to the Open Web doorway)
    # Open Web doorway is at x=780, y=500 in the 1024x1024 original.
    # In 1348x1348 pasted at (496, 28):
    # x = 496 + 780 * (1348/1024) = 496 + 1026 = 1522
    # y = 28 + 500 * (1348/1024) = 28 + 658 = 686
    draw_pointer(
        target=(1522, 686),
        shelf_start=(1580, 500),
        shelf_end=(1780, 500),
        text="Instant Deploy",
        text_pos=(1595, 470)
    )

    # 8. Save the Image relative to the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, 'singularity-1087.png')
    
    try:
        image.save(output_path, 'PNG')
        logging.info("Successfully generated poster and saved to: %s", output_path)
    except IOError as e:
        logging.error("Failed to save output image to %s: %s", output_path, e)
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("Usage: python3 %s <base_image_path>", sys.argv[0])
        sys.exit(1)
        
    generate_poster(sys.argv[1])
