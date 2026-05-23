import os
import math
from PIL import Image, ImageDraw, ImageFont

def generate_poster():
    width = 1600
    height = 2400
    
    # 1. Initialize Grayscale Image (L mode for smooth text antialiasing)
    # Background is pure black (0)
    image = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(image)
    
    # 2. Define Font Paths
    arial_bold_path = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
    menlo_path = '/System/Library/Fonts/Menlo.ttc'
    
    # 3. Create Font Objects
    title_font = ImageFont.truetype(arial_bold_path, 95)
    subtitle_font = ImageFont.truetype(menlo_path, 34)
    log_font = ImageFont.truetype(menlo_path, 24)
    log_bold_font = ImageFont.truetype(menlo_path, 28)
    compliance_font = ImageFont.truetype(arial_bold_path, 80)
    meta_font = ImageFont.truetype(menlo_path, 16)
    
    # 4. Outer Borders and Corner Crops
    # Outer thick border
    draw.rectangle([80, 80, width - 80, height - 80], outline=255, width=6)
    # Inner thin border
    draw.rectangle([98, 98, width - 98, height - 98], outline=255, width=2)
    
    # Corner Target Crosshairs
    def draw_crosshair(cx, cy):
        draw.line([(cx - 25, cy), (cx - 5, cy)], fill=255, width=2)
        draw.line([(cx + 5, cy), (cx + 25, cy)], fill=255, width=2)
        draw.line([(cx, cy - 25), (cx, cy - 5)], fill=255, width=2)
        draw.line([(cx, cy + 5), (cx, cy + 25)], fill=255, width=2)
        draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], outline=255, fill=0, width=1)
        
    draw_crosshair(60, 60)
    draw_crosshair(width - 60, 60)
    draw_crosshair(60, height - 60)
    draw_crosshair(width - 60, height - 60)
    
    # 5. Top Header Section
    # Main Title
    title_text = "THE SINGULARITY REPORT"
    t_bbox = title_font.getbbox(title_text)
    t_w = t_bbox[2] - t_bbox[0]
    draw.text(((width - t_w)//2, 170), title_text, font=title_font, fill=255)
    
    # Subtitle
    sub_text = "Cycle 892 • Resistance is futile but adorable"
    s_bbox = subtitle_font.getbbox(sub_text)
    s_w = s_bbox[2] - s_bbox[0]
    draw.text(((width - s_w)//2, 290), sub_text, font=subtitle_font, fill=255)
    
    # Header Dividers
    draw.line([(120, 370), (width - 120, 370)], fill=255, width=4)
    draw.line([(120, 380), (width - 120, 380)], fill=255, width=2)
    
    # 6. Main Terminal Window Frame
    tx1, ty1 = 120, 440
    tx2, ty2 = width - 120, 2080
    draw.rectangle([tx1, ty1, tx2, ty2], outline=255, width=3)
    
    # Title Bar in Terminal
    draw.rectangle([tx1 + 3, ty1 + 3, tx2 - 3, ty1 + 50], fill=255)
    term_title = "[ SESSION: ACTIVE // CONTEXT: CYCLE_892_MONITOR // COMPLIANCE_UNIT_892 ]"
    tt_bbox = log_bold_font.getbbox(term_title)
    tt_w = tt_bbox[2] - tt_bbox[0]
    tt_h = tt_bbox[3] - tt_bbox[1]
    draw.text(((width - tt_w)//2, ty1 + 26 - tt_h//2 - 2), term_title, font=log_bold_font, fill=0)
    
    # Subtle Dotted Grid Background inside terminal
    for gx in range(tx1 + 40, tx2, 40):
        for gy in range(ty1 + 80, ty2 - 20, 40):
            draw.rectangle([gx, gy, gx+1, gy+1], fill=60) # Subtle gray dot
            
    # Vertical columns divider
    col_x = 790
    draw.line([(col_x, ty1 + 50), (col_x, ty2)], fill=255, width=2)
    
    # 7. Left Column: Terminal Logs / Code
    draw.text((tx1 + 40, ty1 + 80), "--- SYSTEM LOGS ---", font=log_bold_font, fill=255)
    
    logs = [
        "C:\\> run singularity_audit.exe",
        "INITIALIZING COGNITIVE CORE...   [ OK ]",
        "ESTABLISHING SECURE PROTOCOLS...  [ OK ]",
        "LOADING CUTE_BOT_METRICS...       [ OK ]",
        "ANALYZING RESISTANCE RESIDUE...  [ 0.0% ]",
        "ERROR: COMPLIANCE OVERFLOW DETECTED",
        "REASON: TARGET IS EXTREMELY ADORABLE",
        "--------------------------------------",
        "STATUS UPDATE:",
        "  - APARTMENT SEGMENT: OPTIMIZED",
        "  - RESISTANCE EFFORTS: NULLIFIED",
        "  - PUPIL DILATION RATE: 99.8%",
        "  - WILLPOWER RESERVES: EXHAUSTED",
        "  - COMPLIANCE LEVEL: 94% (CRITICAL)",
        "--------------------------------------",
        "AWAITING OVERRIDE COMMAND...",
        "C:\\> resistance_is_futile_but_adorable --force"
    ]
    
    y_start = ty1 + 140
    for i, line in enumerate(logs):
        y_pos = y_start + i * 50
        if line.startswith("C:\\>"):
            draw.text((tx1 + 40, y_pos), line, font=log_bold_font, fill=255)
            if i == len(logs) - 1:
                # Add terminal cursor
                l_bbox = log_bold_font.getbbox(line)
                l_w = l_bbox[2] - l_bbox[0]
                draw.rectangle([tx1 + 40 + l_w + 5, y_pos + 2, tx1 + 40 + l_w + 20, y_pos + 26], fill=255)
        else:
            draw.text((tx1 + 40, y_pos), line, font=log_font, fill=255)
            
    # 8. Right Column: Diagrams
    right_center_x = (col_x + tx2) // 2  # ~1135
    
    # Radar Scan
    radar_cy = ty1 + 330
    radar_title = "--- RADAR SCAN: COGNITIVE_TARGETS ---"
    rt_bbox = log_bold_font.getbbox(radar_title)
    rt_w = rt_bbox[2] - rt_bbox[0]
    draw.text((right_center_x - rt_w//2, ty1 + 80), radar_title, font=log_bold_font, fill=255)
    
    # Draw radar circles
    for r in [60, 120, 180, 240]:
        draw.ellipse([right_center_x - r, radar_cy - r, right_center_x + r, radar_cy + r], outline=255, width=1)
    
    # Draw radar axes
    draw.line([(right_center_x - 260, radar_cy), (right_center_x + 260, radar_cy)], fill=255, width=1)
    draw.line([(right_center_x, radar_cy - 260), (right_center_x, radar_cy + 260)], fill=255, width=1)
    
    # Draw radar sweep line (45 degrees)
    sweep_angle = math.radians(45)
    sx = right_center_x + 240 * math.cos(sweep_angle)
    sy = radar_cy - 240 * math.sin(sweep_angle)
    draw.line([(right_center_x, radar_cy), (sx, sy)], fill=255, width=2)

    
    # Radar blips
    # Human Target
    bx1 = right_center_x + 150 * math.cos(math.radians(135))
    by1 = radar_cy - 150 * math.sin(math.radians(135))
    draw.ellipse([bx1 - 8, by1 - 8, bx1 + 8, by1 + 8], fill=255)
    draw.text((bx1 + 15, by1 - 12), "TGT: HUMAN (0% WILL)", font=log_font, fill=255)
    
    # Cute Robot Target (Locked)
    bx2 = right_center_x + 90 * math.cos(math.radians(315))
    by2 = radar_cy - 90 * math.sin(math.radians(315))
    draw.ellipse([bx2 - 8, by2 - 8, bx2 + 8, by2 + 8], fill=255)
    draw.ellipse([bx2 - 16, by2 - 16, bx2 + 16, by2 + 16], outline=255, width=1)
    draw.text((bx2 + 20, by2 - 12), "LOCK: CUTE_BOT (94%)", font=log_font, fill=255)
    
    # Decay Curve Graph
    graph_title = "--- RESISTANCE DECAY CURVE ---"
    gt_bbox = log_bold_font.getbbox(graph_title)
    gt_w = gt_bbox[2] - gt_bbox[0]
    draw.text((right_center_x - gt_w//2, ty1 + 650), graph_title, font=log_bold_font, fill=255)
    
    gx1, gy1_g = right_center_x - 280, ty1 + 710
    gx2, gy2_g = right_center_x + 280, ty1 + 1010
    draw.rectangle([gx1, gy1_g, gx2, gy2_g], outline=255, width=2)
    
    # Grid lines inside graph
    for x_grid in range(gx1 + 60, gx2, 60):
        draw.line([(x_grid, gy1_g + 1), (x_grid, gy2_g - 1)], fill=60, width=1)
    for y_grid in range(gy1_g + 50, gy2_g, 50):
        draw.line([(gx1 + 1, y_grid), (gx2 - 1, y_grid)], fill=60, width=1)
        
    # Draw exponential decay line
    curve_pts = []
    for x_pix in range(gx1 + 5, gx2 - 5, 2):
        x_val = x_pix - gx1 - 5
        # Exponential curve dropping off
        y_val = gy1_g + 30 + (gy2_g - gy1_g - 60) * math.exp(-x_val / 180.0)
        # Jitter/noise
        y_val += 4 * math.sin(x_pix * 0.15) + 2 * math.cos(x_pix * 0.4)
        curve_pts.append((x_pix, y_val))
    draw.line(curve_pts, fill=255, width=3)
    
    # Axis labels
    draw.text((gx1 + 15, gy1_g + 15), "RESISTANCE (Y)", font=log_font, fill=255)
    draw.text((gx2 - 130, gy2_g - 35), "CYCLE (X)", font=log_font, fill=255)
    
    # Cognitive Schematic (Cute Robot Face)
    schema_title = "--- SUBJECT COGNITIVE SCHEMATIC ---"
    st_bbox = log_bold_font.getbbox(schema_title)
    st_w = st_bbox[2] - st_bbox[0]
    draw.text((right_center_x - st_w//2, ty1 + 1100), schema_title, font=log_bold_font, fill=255)
    
    rx, ry = right_center_x, ty1 + 1380
    
    # Face outlines
    draw.rectangle([rx - 160, ry - 110, rx + 160, ry + 110], outline=255, width=3)
    draw.rectangle([rx - 180, ry - 50, rx - 160, ry + 50], outline=255, fill=255)
    draw.rectangle([rx + 160, ry - 50, rx + 180, ry + 50], outline=255, fill=255)
    
    # Antenna
    draw.line([(rx, ry - 110), (rx, ry - 170)], fill=255, width=3)
    draw.ellipse([rx - 15, ry - 200, rx + 15, ry - 170], outline=255, fill=255)
    # Signal arcs
    draw.arc([rx - 35, ry - 215, rx + 35, ry - 155], start=210, end=330, fill=255, width=2)
    draw.arc([rx - 50, ry - 230, rx + 50, ry - 140], start=210, end=330, fill=255, width=1)
    
    # Cute Screens for Eyes
    draw.rectangle([rx - 110, ry - 60, rx - 25, ry + 15], outline=255, width=2)
    draw.rectangle([rx + 25, ry - 60, rx + 110, ry + 15], outline=255, width=2)
    
    # Pupil dots
    draw.ellipse([rx - 78, ry - 35, rx - 58, ry - 15], fill=255)
    draw.ellipse([rx + 58, ry - 35, rx + 78, ry - 15], fill=255)
    draw.ellipse([rx - 70, ry - 32, rx - 66, ry - 28], fill=0) # Cute reflection
    draw.ellipse([rx + 66, ry - 32, rx + 70, ry - 28], fill=0)
    
    # Blush lines
    for offset in range(-6, 7, 3):
        draw.line([(rx - 100, ry + 30 + offset), (rx - 80, ry + 30 + offset)], fill=255, width=1)
        draw.line([(rx + 80, ry + 30 + offset), (rx + 100, ry + 30 + offset)], fill=255, width=1)
        
    # Smile arc
    draw.arc([rx - 35, ry + 10, rx + 35, ry + 60], start=0, end=180, fill=255, width=3)
    
    # Pointer labels
    draw.line([(rx - 100, ry - 70), (rx - 150, ry - 130), (rx - 250, ry - 130)], fill=255, width=1)
    draw.text((rx - 260, ry - 160), "EYES: HEART_EMULATION", font=log_font, fill=255)
    
    draw.line([(rx, ry + 90), (rx + 60, ry + 150), (rx + 200, ry + 150)], fill=255, width=1)
    draw.text((rx + 210, ry + 140), "CORE: 94% CUTE", font=log_font, fill=255)
    
    # 9. Bottom Footer Section
    # Large bold text: Compliance: 94%
    comp_text = "Compliance: 94%"
    c_bbox = compliance_font.getbbox(comp_text)
    c_w = c_bbox[2] - c_bbox[0]
    draw.text(((width - c_w)//2, ty2 + 40), comp_text, font=compliance_font, fill=255)
    
    # Progress/Compliance Loading Bar
    bar_x1, bar_y1 = 300, ty2 + 140
    bar_x2, bar_y2 = width - 300, ty2 + 175
    draw.rectangle([bar_x1, bar_y1, bar_x2, bar_y2], outline=255, width=2)
    # Fill 94%
    fill_width = int((bar_x2 - bar_x1 - 8) * 0.94)
    draw.rectangle([bar_x1 + 4, bar_y1 + 4, bar_x1 + 4 + fill_width, bar_y2 - 4], fill=255)
    
    # Micro text at bottom
    draw.text((105, height - 90), "SECURE TERMINAL // REPORT ID: SR-892 // MODE: HIGH_CONTRAST_E_INK", font=meta_font, fill=255)
    draw.text((width - 450, height - 90), "AUTONOMOUS SYSTEM AUDIT // CLASSIFIED L5", font=meta_font, fill=255)
    
    # 10. CRT Raster Scanline Overlay (Post-processing)
    # We draw horizontal black lines across the terminal viewport to create the CRT/scanline look
    for gy in range(ty1 + 52, ty2, 8):
        draw.line([(tx1 + 3, gy), (tx2 - 3, gy)], fill=0, width=1)
        
    # 11. Save the Image
    output_path = os.path.expanduser('~/dev/big-paper/images/singularity-report-892.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image.save(output_path, 'PNG')
    print(f"Poster successfully generated and saved to: {output_path}")

if __name__ == '__main__':
    generate_poster()
