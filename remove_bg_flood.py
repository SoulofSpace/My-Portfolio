import os
from PIL import Image

def flood_fill_background(image_path, output_path):
    print(f"Loading user portrait: {image_path}")
    img = Image.open(image_path).convert("RGBA")
    width, height = img.size
    
    # We want to perform a flood fill from the borders to detect the background.
    # We'll use a queue-based flood fill.
    pixels = img.load()
    visited = set()
    bg_pixels = set()
    
    # Threshold for color distance from black (0, 0, 0)
    # The background is extremely dark, but not always exactly (0,0,0) due to compression
    threshold = 30
    
    def get_neighbors(x, y):
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                neighbors.append((nx, ny))
        return neighbors

    # Start seeds from all border pixels
    seeds = []
    for x in range(width):
        seeds.append((x, 0))
        seeds.append((x, height - 1))
    for y in range(1, height - 1):
        seeds.append((0, y))
        seeds.append((width - 1, y))
        
    queue = []
    for x, y in seeds:
        r, g, b, a = pixels[x, y]
        # Check if the border pixel is dark enough to be background
        if r < threshold and g < threshold and b < threshold:
            queue.append((x, y))
            visited.add((x, y))
            bg_pixels.add((x, y))
            
    # Run flood fill
    while queue:
        cx, cy = queue.pop(0)
        for nx, ny in get_neighbors(cx, cy):
            if (nx, ny) not in visited:
                r, g, b, a = pixels[nx, ny]
                # If neighbor is close to black, it is part of the background
                if r < threshold and g < threshold and b < threshold:
                    visited.add((nx, ny))
                    bg_pixels.add((nx, ny))
                    queue.append((nx, ny))
                    
    # Update image data: make background transparent, keep everything else solid
    new_data = []
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if (x, y) in bg_pixels:
                new_data.append((r, g, b, 0))
            else:
                new_data.append((r, g, b, 255))
                
    img.putdata(new_data)
    img.save(output_path, "PNG")
    print(f"Successfully removed background using flood fill! Saved to {output_path}")

if __name__ == "__main__":
    src = "media__1782271915373.jpg"
    dest = "editor_portrait.png"
    
    # The source is in the brain folder, let's copy it or load it directly
    brain_src = "C:\\Users\\space\\.gemini\\antigravity\\brain\\0d1ed549-1d46-401b-9d68-aff03b1bf5b5\\media__1782271915373.jpg"
    if os.path.exists(brain_src):
        flood_fill_background(brain_src, dest)
    else:
        print(f"Error: {brain_src} not found!")
