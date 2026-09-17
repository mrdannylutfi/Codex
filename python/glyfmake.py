from PIL import Image, ImageDraw, ImageFont

def parse_color(color_input):
    """Converts hex strings or RGB tuples into a standard RGBA tuple."""
    if isinstance(color_input, str):
        color_input = color_input.lstrip('#')
        rgb = tuple(int(color_input[i:i+2], 16) for i in (0, 2, 4))
        return rgb + (255,)
    elif isinstance(color_input, tuple):
        if len(color_input) == 3:
            return color_input + (255,)
        return color_input
    return (0, 0, 0, 255)

def create_advanced_glyph_icon(
    text="A", 
    output_path="custom_icon.png", 
    size=(16, 16), 
    shape="badge", 
    bg_color="#FF5733",      # Supports Hex
    text_color=(255, 255, 255) # Supports RGB
):
    # 1. Supersampling: Render at 4x size then downscale for smooth edges (anti-aliasing)
    scale = 4
    render_size = (size[0] * scale, size[1] * scale)
    image = Image.new("RGBA", render_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # 2. Parse colors
    fill_bg = parse_color(bg_color)
    fill_text = parse_color(text_color)
    
    # 3. Draw advanced custom shapes
    w, h = render_size[0], render_size[1]
    
    if shape.lower() == "triangle":
        # Coordinates for an upright triangle
        points = [(w // 2, 0), (0, h - 1), (w - 1, h - 1)]
        draw.polygon(points, fill=fill_bg)
        
    elif shape.lower() == "badge":
        # Shield/Badge style: Straight top, curved/pointed bottom
        points = [
            (0, 0),                       # Top-left
            (w - 1, 0),                   # Top-right
            (w - 1, int(h * 0.6)),        # Right mid
            (w // 2, h - 1),              # Bottom tip
            (0, int(h * 0.6))             # Left mid
        ]
        draw.polygon(points, fill=fill_bg)
    
    else:
        # Default fallback to a simple rectangle box if shape mismatch
        draw.rectangle([0, 0, w - 1, h - 1], fill=fill_bg)
        
    # 4. Handle Font and scaling
    # Adjust font scale depending on the shape container limits
    font_scale = 0.55 if shape.lower() == "triangle" else 0.65
    font_size = int(w * font_scale)
    
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
        
    # 5. Perfect centering calculations
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x_pos = (w - text_width) // 2 - bbox[0]
    y_pos = (h - text_height) // 2 - bbox[1]
    
    # Push text down slightly for triangles since the base is heavier
    if shape.lower() == "triangle":
        y_pos += int(h * 0.1)
        
    draw.text((x_pos, y_pos), text, fill=fill_text, font=font)
    
    # 6. Downsample back to the original target size using high-quality Resampling
    final_image = image.resize(size, Image.Resampling.LANCZOS)
    final_image.save(output_path)
    print(f"Icon generated: {shape} style saved to {output_path}")

# --- Test Palette Run ---
# 1. Pastel Orange Badge with White Text
create_advanced_glyph_icon(shape="badge", bg_color="#FFB347", text_color="#FFFFFF", output_path="orange_badge.png")

# 2. Forest Green Triangle with Light Gray Text using RGB
create_advanced_glyph_icon(shape="triangle", bg_color=(34, 139, 34), text_color=(240, 240, 240), output_path="green_triangle.png")
