import os
from PIL import Image

def remove_background(image_path, output_path):
    print(f"Opening image: {image_path}")
    img = Image.open(image_path).convert("RGBA")
    datas = img.getdata()

    new_data = []
    # Threshold for black background
    threshold = 20
    
    for item in datas:
        r, g, b, a = item
        # Calculate brightness/intensity
        # If it's very dark, make it transparent
        if r < threshold and g < threshold and b < threshold:
            # We can also do a smooth falloff to avoid harsh edges
            # For pixels extremely close to black, set alpha to 0
            new_data.append((r, g, b, 0))
        else:
            new_data.append((r, g, b, 255))

    img.putdata(new_data)
    img.save(output_path, "PNG")
    print(f"Saved transparent image to: {output_path}")

if __name__ == "__main__":
    src = "editor_portrait.jpg"
    dest = "editor_portrait.png"
    if os.path.exists(src):
        remove_background(src, dest)
    else:
        print(f"Error: {src} not found!")
