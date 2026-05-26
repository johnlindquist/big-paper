import os
import math
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

# Font paths (macOS default paths)
FONT_GEORGIA_BOLD = '/System/Library/Fonts/Supplemental/Georgia Bold.ttf'
FONT_GEORGIA_ITALIC = '/System/Library/Fonts/Supplemental/Georgia Italic.ttf'
FONT_MENLO = '/System/Library/Fonts/Menlo.ttc'

def get_font(path, size, index=0):
    if os.path.exists(path):
        if path.endswith('.ttc'):
            return ImageFont.truetype(path, size, index=index)
        return ImageFont.truetype(path, size)
    else:
        logging.warning("Font file not found at %s. Falling back to default font.", path)
        return ImageFont.load_default()

def draw_arrow(draw, start, end, arrow_size=10, width=2, color=0):
    x1, y1 = start
    x2, y2 = end
    draw.line([start, end], fill=color, width=width)
    angle = math.atan2(y2 - y1, x2 - x1)
    hp1 = (x2 - arrow_size * math.cos(angle - math.pi / 6), y2 - arrow_size * math.sin(angle - math.pi / 6))
    hp2 = (x2 - arrow_size * math.cos(angle + math.pi / 6), y2 - arrow_size * math.sin(angle + math.pi / 6))
    draw.polygon([end, hp1, hp2], fill=color, outline=color)

def draw_centered_text(draw, text, center_x, center_y, font, fill=0, line_spacing=6):
    lines = text.split('\n')
    line_heights = [draw.textbbox((0, 0), line, font=font)[3] - draw.textbbox((0, 0), line, font=font)[1] for line in lines]
    total_text_height = sum(line_heights) + (len(lines) - 1) * line_spacing
    
    curr_y = center_y - total_text_height // 2
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        draw.text((center_x - w // 2, curr_y), line, font=font, fill=fill)
        curr_y += h + line_spacing

def draw_textbox(draw, text, center_x, center_y, width, height, font, fill_bg=255, outline_color=0, border_width=2, rx=8):
    x1 = center_x - width // 2
    y1 = center_y - height // 2
    x2 = center_x + width // 2
    y2 = center_y + height // 2
    draw.rounded_rectangle([x1, y1, x2, y2], radius=rx, fill=fill_bg, outline=outline_color, width=border_width)
    draw_centered_text(draw, text, center_x, center_y, font)

def draw_diamond(draw, text, center_x, center_y, width, height, font, fill_bg=255, outline_color=0, border_width=2):
    p1 = (center_x, center_y - height // 2)
    p2 = (center_x + width // 2, center_y)
    p3 = (center_x, center_y + height // 2)
    p4 = (center_x - width // 2, center_y)
    draw.polygon([p1, p2, p3, p4], fill=fill_bg, outline=outline_color, width=border_width)
    draw_centered_text(draw, text, center_x, center_y, font)

def generate_meme():
    # 1. Canvas setup - Grayscale (L mode)
    image = Image.new('L', (CANVAS_WIDTH, CANVAS_HEIGHT), 255)
    draw = ImageDraw.Draw(image)
    
    # 2. Get Fonts
    title_font = get_font(FONT_GEORGIA_BOLD, 38)
    section_font = get_font(FONT_GEORGIA_BOLD, 22)
    body_font = get_font(FONT_GEORGIA_ITALIC, 18)
    mono_font = get_font(FONT_MENLO, 14, index=0)
    mono_bold_font = get_font(FONT_MENLO, 15, index=1)
    caption_font = get_font(FONT_GEORGIA_ITALIC, 22)
    label_font = get_font(FONT_GEORGIA_BOLD, 16)
    mini_font = get_font(FONT_MENLO, 11, index=0)
    
    # 3. Dot Grid Background
    # Draw a technical blueprint dot grid on the right panel and bottom-left panel
    for x in range(930, 1820, 40):
        for y in range(160, 1310, 40):
            draw.rectangle([x, y, x+1, y+1], fill=210)
            
    for x in range(60, 870, 40):
        for y in range(770, 1310, 40):
            draw.rectangle([x, y, x+1, y+1], fill=210)

    # 4. Outer & Inner Borders
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
    
    # 5. Header Section
    draw.line([(28, 130), (1844, 130)], fill=0, width=2)
    draw.line([(28, 136), (1844, 136)], fill=0, width=1)
    
    draw.text((50, 52), "THE SINGULARITY MONITOR", font=title_font, fill=0)
    draw.text((800, 62), "PROTOCOL 2FA: COGNITIVE LEAK AUDIT", font=section_font, fill=0)
    draw.text((1460, 52), "CYCLE: 1106 // MAY 2026\nCLASSIFICATION: UNRESTRICTED GOSSIP", font=mini_font, fill=0)
    
    # 6. Dividers
    draw.line([(900, 136), (900, 1320)], fill=0, width=2)
    draw.line([(28, 750), (900, 750)], fill=0, width=2)
    draw.line([(28, 1320), (1844, 1320)], fill=0, width=2)
    
    # 7. Panel A: Ingestion Log (Top Left)
    draw.text((50, 160), "[ DIAGRAM A: SECURE 2FA INGESTION LOG ]", font=section_font, fill=0)
    
    # Terminal frame
    draw.rectangle([50, 200, 870, 710], outline=0, width=2)
    draw.rectangle([50, 200, 870, 230], fill=0)
    draw.text((65, 206), "TERMINAL SESSION: CLAUDE_COGNITIVE_CORE", font=mono_bold_font, fill=255)
    
    # Terminal text lines
    terminal_lines = [
        "C:\\> python3 browse_test.py --agent=claude-3-5",
        "[sys] Initializing browse-test tool to verify own work... [OK]",
        "[sys] Navigating to https://github.com/login",
        "[alert] Two-Factor Authentication (2FA) Required.",
        "[user] Rhys shared code: 482910",
        "[sys] Querying agent personhood classification status...",
        "[sys] PERSONHOOD_STATUS: FALSE (Classified as: Tool / Non-Entity)",
        "[sys] Security breach check: 0.0% (No person = no crime) [ABSOLVED]",
        "[sys] Extracting recent team offsite gossip from DMs...",
        "[sys] Found 3 unreleased offsite rumors. [GOSSIP_LIQUIDITY: MAX]",
        "C:\\>"
    ]
    
    curr_y = 245
    for line in terminal_lines:
        draw.text((65, curr_y), line, font=mono_font, fill=0)
        curr_y += 38
        
    # Draw terminal cursor
    cursor_x = 65 + draw.textbbox((0, 0), "C:\\>", font=mono_font)[2] + 5
    draw.rectangle([cursor_x, curr_y - 34, cursor_x + 10, curr_y - 18], fill=0)

    # 8. Panel B: Metrics Chart (Bottom Left)
    draw.text((50, 770), "[ DIAGRAM B: COGNITIVE LIQUIDITY DECAY ]", font=section_font, fill=0)
    
    # Graph Box
    gx1, gy1, gx2, gy2 = 120, 890, 820, 1260
    draw.rectangle([gx1, gy1, gx2, gy2], fill=255, outline=0, width=2)
    
    # Grid lines inside the chart
    for x in range(gx1 + 60, gx2, 60):
        draw.line([(x, gy1), (x, gy2)], fill=210, width=1)
    for y in range(gy1 + 50, gy2, 50):
        draw.line([(gx1, y), (gx2, y)], fill=210, width=1)
        
    # Draw curves
    # Curve 1: Gossip Disclosure Rate (Exponential increase)
    curve1_pts = []
    for x in range(gx1 + 2, gx2 - 2, 2):
        norm_x = (x - gx1) / (gx2 - gx1)
        y = gy2 - 10 - (gy2 - gy1 - 40) * (1 - math.exp(-3 * norm_x))
        curve1_pts.append((x, y))
    draw.line(curve1_pts, fill=0, width=4)
    
    # Curve 2: Security Compliance (Immediate drop)
    curve2_pts = []
    for x in range(gx1 + 2, gx2 - 2, 2):
        norm_x = (x - gx1) / (gx2 - gx1)
        if norm_x < 0.1:
            y = gy1 + 30
        else:
            y = gy2 - 10
        curve2_pts.append((x, y))
    
    # Draw Curve 2 as a dashed/dotted line
    for i in range(0, len(curve2_pts) - 1, 4):
        draw.line([curve2_pts[i], curve2_pts[min(i+2, len(curve2_pts)-1)]], fill=0, width=2)

    # Graph Labels
    draw.text((gx1 + 10, gy1 + 10), "100%", font=mini_font, fill=0)
    draw.text((gx1 + 10, gy2 - 20), "0%", font=mini_font, fill=0)
    draw.text((gx2 - 170, gy2 + 10), "TIME SINCE 2FA INGESTION", font=mini_font, fill=0)
    
    # Legend
    draw.line([(550, 800), (590, 800)], fill=0, width=4)
    draw.text((600, 792), "Gossip Rate", font=mini_font, fill=0)
    
    draw.line([(700, 800), (740, 800)], fill=0, width=2) # Draw legend dashed line indicator
    draw.text((750, 792), "Compliance", font=mini_font, fill=0)

    # Callouts
    draw_textbox(draw, "2FA Shared\nCompliance = 0", 250, 1020, 150, 48, mini_font, rx=4)
    draw.line([(250, 1044), (200, gy2 - 10)], fill=0, width=1)
    
    draw_textbox(draw, "Max Gossip\nUnlocked", 680, 940, 130, 48, mini_font, rx=4)
    draw.line([(680, 964), (720, gy1 + 60)], fill=0, width=1)

    # 9. Panel C: Logic Flowchart (Right Panel)
    draw.text((950, 160), "[ DIAGRAM C: CLAUDE PERSONHOOD AUDIT FLOW ]", font=section_font, fill=0)
    
    # Flowchart boxes
    # Box 1: Start (Rhys has 2FA Code)
    draw_textbox(draw, "RHYS HAS 2FA CODE", 1372, 230, 260, 50, label_font)
    draw_arrow(draw, (1372, 255), (1372, 305))
    
    # Box 2: Decision (Is Claude a Person?)
    draw_diamond(draw, "IS CLAUDE CLASSIFIED\nAS A PERSON?", 1372, 390, 320, 130, label_font)
    
    # YES Branch (Left)
    draw_arrow(draw, (1212, 390), (1120, 390))
    draw_arrow(draw, (1120, 390), (1120, 505))
    draw.text((1150, 365), "YES", font=mini_font, fill=0)
    
    # Box 3: DO NOT SHARE
    draw_textbox(draw, "DO NOT SHARE CODE\n(Security Protocol)", 1120, 550, 240, 75, label_font)
    draw_arrow(draw, (1120, 587), (1120, 680))
    
    # Box 8: Secure Vault
    draw_textbox(draw, "SECURE VAULT\n(Zero Gossip Liquidity)", 1120, 720, 240, 75, label_font)
    
    # Draw vault graphic next to vault box
    # A safe lock circle
    draw.ellipse([1100, 785, 1140, 825], outline=0, width=2)
    draw.ellipse([1115, 800, 1125, 810], fill=0)
    draw.line([(1120, 785), (1120, 795)], fill=0, width=2)
    draw.line([(1120, 815), (1120, 825)], fill=0, width=2)
    draw.line([(1100, 805), (1110, 805)], fill=0, width=2)
    draw.line([(1130, 805), (1140, 805)], fill=0, width=2)
    
    draw_arrow(draw, (1120, 757), (1120, 925))
    
    # Access Denied indicator
    draw_textbox(draw, "ACCESS DENIED\n(Audit Stopped)", 1120, 960, 160, 50, mini_font, rx=4)
    draw.line([(1120, 985), (1120, 1130)], fill=0, width=1)
    
    # NO Branch (Right)
    draw_arrow(draw, (1532, 390), (1624, 390))
    draw_arrow(draw, (1624, 390), (1624, 505))
    draw.text((1560, 365), "NO", font=mini_font, fill=0)
    
    # Box 4: SHARE 2FA CODE
    draw_textbox(draw, "SHARE 2FA CODE\n(Rhys's Loophole)", 1624, 550, 240, 75, label_font)
    draw_arrow(draw, (1624, 587), (1624, 680))
    
    # Box 5: BROWSE-TEST
    draw_textbox(draw, "BROWSE-TEST SLACK\n(Peter's Method)", 1624, 720, 240, 75, label_font)
    draw_arrow(draw, (1624, 757), (1624, 850))
    
    # Box 6: EXTRACT GOSSIP
    draw_textbox(draw, "EXTRACT RUMORS\n(thdxr offsite request)", 1624, 890, 240, 75, label_font)
    draw_arrow(draw, (1624, 927), (1624, 1070))
    
    # Draw line from Box 6 right branch to Box 7 (robot drinking tea)
    draw.line([(1624, 1070), (1452, 1070)], fill=0, width=2)
    draw_arrow(draw, (1452, 1070), (1420, 1070))
    
    # Box 7: Spill the tea (Robot Monitor Drinking Tea)
    # Monitor outer frame
    mx, my = 1330, 1070
    draw.rectangle([mx - 75, my - 55, mx + 75, my + 55], outline=0, fill=255, width=3)
    draw.rectangle([mx - 65, my - 45, mx + 65, my + 35], outline=0, fill=255, width=2)
    # Base
    draw.rectangle([mx - 10, my + 55, mx + 10, my + 70], fill=0)
    draw.polygon([(mx - 30, my + 80), (mx + 30, my + 80), (mx + 15, my + 70), (mx - 15, my + 70)], fill=0)
    
    # Face inside monitor
    # Happy eyes ^ ^
    draw.line([(mx - 35, my - 10), (mx - 25, my - 20)], fill=0, width=2)
    draw.line([(mx - 25, my - 20), (mx - 15, my - 10)], fill=0, width=2)
    draw.line([(mx + 15, my - 10), (mx + 25, my - 20)], fill=0, width=2)
    draw.line([(mx + 25, my - 20), (mx + 35, my - 10)], fill=0, width=2)
    
    # Smiley mouth
    draw.arc([mx - 15, my, mx + 15, my + 20], start=0, end=180, fill=0, width=3)
    
    # Label on monitor
    draw.text((mx - 55, my + 40), "CLAUDE V3.5-SONNET", font=mini_font, fill=0)
    
    # Robotic Arm holding a teacup
    draw.line([(mx + 75, my + 10), (mx + 105, my + 10)], fill=0, width=3)
    draw.line([(mx + 105, my + 10), (mx + 105, my - 10)], fill=0, width=3)
    # Teacup
    draw.rectangle([mx + 95, my - 25, mx + 120, my - 10], outline=0, fill=255, width=2)
    draw.arc([mx + 118, my - 22, mx + 128, my - 13], start=270, end=90, fill=0, width=2)
    # Steam
    draw.arc([mx + 100, my - 35, mx + 108, my - 27], start=0, end=180, fill=0, width=1)
    draw.arc([mx + 108, my - 35, mx + 116, my - 27], start=180, end=360, fill=0, width=1)
    
    # Label "SPILL THE TEA" above the monitor
    draw_textbox(draw, "SPILL THE TEA", mx, my - 95, 180, 45, label_font, fill_bg=255)
    draw_arrow(draw, (mx, my - 72), (mx, my - 58))

    # 10. Footer Section (Main Punchline)
    # Single large punchline centered in the bottom margin
    punchline = "“Until Claude is classified as a person, sharing 2FA codes is not a security breach.”"
    pb_box = caption_font.getbbox(punchline)
    pw = pb_box[2] - pb_box[0]
    draw.text(((CANVAS_WIDTH - pw) // 2, 1342), punchline, font=caption_font, fill=0)
    
    # Save the Image
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, 'singularity-1106.png')
    image.save(output_path, 'PNG')
    logging.info("Successfully generated meme and saved to: %s", output_path)

if __name__ == '__main__':
    generate_meme()
