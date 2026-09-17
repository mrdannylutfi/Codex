from PIL import Image, ImageDraw, ImageFont

def create_arial_glyph_icon(text="A", output_path="icon_a.png", size=(16, 16), font_size=16):
    # 1. Create a 16x16 transparent image canvas
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # 2. Load Arial font (Tries standard system paths automatically)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        print("Arial font file not found in default paths. Falling back to default font.")
        font = ImageFont.load_default()
        
    # 3. Calculate bounding box to align the character perfectly in the center
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Calculate offset positioning
    x_pos = (size[0] - text_width) // 2 - bbox[0]
    y_pos = (size[1] - text_height) // 2 - bbox[1]
    
    # 4. Draw the glyph in crisp black text (0, 0, 0)
    draw.text((x_pos, y_pos), text, fill=(0, 0, 0, 255), font=font)
    
    # 5. Save the output
    image.save(output_path)
    print(f"Icon successfully generated at {output_path}")

# Run the function
create_arial_glyph_icon()
