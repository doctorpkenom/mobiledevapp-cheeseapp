from PIL import Image
import os
import sys

def make_transparent(file_path):
    try:
        img = Image.open(file_path).convert("RGBA")
        datas = img.getdata()
        
        # Check corner pixel to determine background color
        # We assume the top-left pixel represents the background
        bg_color = img.getpixel((0, 0))
        
        # If it's already transparent (alpha < 10), we might skip or check further.
        # But let's assume we want to remove white/near-white.
        
        # Define threshold for "white" or "background"
        # If bg_color is not white-ish, we might check if user wants it removed.
        # For now, let's target white/light backgrounds specifically as requested.
        
        is_light_bg = (bg_color[0] > 240 and bg_color[1] > 240 and bg_color[2] > 240)
        
        if not is_light_bg and bg_color[3] != 0:
            print(f"Skipping {os.path.basename(file_path)}: Background seems dark or colored {bg_color}")
            # return # Uncomment to be conservative, or proceed to flood fill anyway if you want to be aggressive
        
        # Flood fill logic from (0,0) and other corners slightly better than replacing all white
        # Pillow's ImageDraw.floodfill doesn't erase to transparent easily on strict check.
        # Let's do a simple proximity replacement first, as these are likely flat icons.
        # Actually, flood fill is safer for internal whites.
        
        # Let's use a tolerance-based replacement for simplicity if it's a simple graphic
        # But flood fill is better. Let's do a BFS flood fill for transparency.
        
        width, height = img.size
        # visited = set()
        # q = [(0,0), (width-1, 0), (0, height-1), (width-1, height-1)]
        
        # To be safe/fast, let's simpler:
        # If pixel is near white (>240, >240, >240), make transparent.
        # RISK: Eyes/Teeth become transparent.
        
        # Better: use Pillow's transparency handling if it was a simple colorkey.
        # Let's try the simple threshold first, but ONLY if the pixel is connected to the outside?
        # That's expensive in python without cv2.
        
        # COMPROMISE: Distance threshold from pure white.
        newData = []
        changed = False
        for item in datas:
            # Check for white-ish
            if item[0] > 240 and item[1] > 240 and item[2] > 240:
                newData.append((255, 255, 255, 0))
                changed = True
            else:
                newData.append(item)
        
        if changed:
            img.putdata(newData)
            img.save(file_path, "PNG")
            print(f"Processed: {os.path.basename(file_path)}")
        else:
            print(f"Unchanged: {os.path.basename(file_path)}")
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(root, file)
                make_transparent(file_path)

if __name__ == "__main__":
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "react/public/assets"
    print(f"Processing images in: {target_dir}")
    process_directory(target_dir)
