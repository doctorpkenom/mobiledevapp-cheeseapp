from PIL import Image, ImageDraw, ImageOps, ImageFilter
import os
import random

class UIRenderer:
    def __init__(self, asset_dir):
        self.asset_dir = asset_dir
        self.textures = {}
        self.load_textures()

    def load_textures(self):
        # Load base textures if available
        # Added texture_paper to list
        for name in ["texture_wood", "texture_tape", "texture_paper", "card_paper_bg"]:
            path = os.path.join(self.asset_dir, "gen_assets", f"{name}.png")
            if os.path.exists(path):
                self.textures[name] = Image.open(path).convert("RGBA")
            else:
                pass # Silent fail for now, fallback logic handles it

    def create_rounded_rect_mask(self, w, h, radius):
        mask = Image.new("L", (w, h), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, w, h), radius=radius, fill=255)
        return mask

    def create_panel(self, width, height, radius=20, border_color="#5D4037", border_width=4, texture_key="texture_wood"):
        """Creates a wood panel with border and internal texture."""
        img = Image.new("RGBA", (width, height), (0,0,0,0))
        
        if texture_key in self.textures:
            tex = self.textures[texture_key]
            tex = tex.resize((width, height), Image.Resampling.LANCZOS)
            mask = self.create_rounded_rect_mask(width, height, radius)
            img.paste(tex, (0,0), mask)
        else:
            draw = ImageDraw.Draw(img)
            draw.rounded_rectangle((0,0,width,height), radius=radius, fill="#D7CCC8")

        overlay = Image.new("RGBA", (width, height), (0,0,0,0))
        draw = ImageDraw.Draw(overlay)
        draw.rounded_rectangle((0,0,width-1,height-1), radius=radius, outline=border_color, width=border_width)
        
        img = Image.alpha_composite(img, overlay)
        return self.add_drop_shadow(img, radius=radius)

    def create_torn_edge_mask(self, w, h, jaggedness=2):
        """Creates a mask with slightly jagged edges."""
        mask = Image.new("L", (w, h), 0)
        draw = ImageDraw.Draw(mask)
        
        # Simple jagged rect
        points = []
        # Top
        for x in range(0, w, 5):
            points.append((x, 0 + random.randint(0, jaggedness)))
        points.append((w, 0))
        # Right
        for y in range(0, h, 5):
            points.append((w - random.randint(0, jaggedness), y))
        points.append((w, h))
        # Bottom
        for x in range(w, 0, -5):
            points.append((x, h - random.randint(0, jaggedness)))
        points.append((0, h))
        # Left
        for y in range(h, 0, -5):
            points.append((0 + random.randint(0, jaggedness), y))
            
        draw.polygon(points, fill=255)
        return mask

    def create_paper_card(self, width, height):
        """Creates a torn paper card using texture_paper."""
        # Use generated torn card background if available and matching ratio, 
        # But for dynamic size, tiling texture_paper is better.
        
        img = Image.new("RGBA", (width, height), (0,0,0,0))
        
        tex_key = "texture_paper"
        if tex_key in self.textures:
            tex = self.textures[tex_key]
            # Resize texture to cover
            tex = tex.resize((width, height), Image.Resampling.LANCZOS)
            
            # Create a jagged mask
            mask = self.create_torn_edge_mask(width, height, jaggedness=3)
            img.paste(tex, (0,0), mask)
            
            # Add a subtle inner shadow/burnt edge?
            # Creating a border logic for torn paper is complex procedurally.
            # Sticking to the texture + shadow.
        else:
             # Fallback
             draw = ImageDraw.Draw(img)
             draw.rectangle((0,0,width,height), fill="#FFF8E1") # Cream > White

        return self.add_drop_shadow(img, offset=(3,3), shadow_blur=5)

    def create_button(self, width, height, color="#FFB74D", radius=15):
        """Creates a glossy 3D button procedurally."""
        img = Image.new("RGBA", (width, height), (0,0,0,0))
        draw = ImageDraw.Draw(img)
        
        draw.rounded_rectangle((0,0,width,height), radius=radius, fill=color)
        
        # Highlight
        highlight = Image.new("RGBA", (width, height), (0,0,0,0))
        h_draw = ImageDraw.Draw(highlight)
        h_draw.rounded_rectangle((2, 2, width-2, height//2), radius=radius, fill=(255,255,255,80))
        img = Image.alpha_composite(img, highlight)
        
        # Shadow
        shadow_overlay = Image.new("RGBA", (width, height), (0,0,0,0))
        s_draw = ImageDraw.Draw(shadow_overlay)
        s_draw.rounded_rectangle((0, height-10, width, height), radius=radius, fill=(0,0,0,40))
        img = Image.alpha_composite(img, shadow_overlay)
        
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle((0,0,width-1,height-1), radius=radius, outline="#E65100", width=2)
        
        return self.add_drop_shadow(img, radius=radius)

    def add_drop_shadow(self, image, offset=(4,4), shadow_color=(0,0,0,100), shadow_blur=6, radius=0):
        w, h = image.size
        total_w = w + abs(offset[0]) + 2*shadow_blur
        total_h = h + abs(offset[1]) + 2*shadow_blur
        
        base = Image.new("RGBA", (total_w, total_h), (0,0,0,0))
        alpha = image.split()[3]
        
        shadow = Image.new("RGBA", (w, h), shadow_color)
        shadow.putalpha(alpha)
        
        shadow_layer = Image.new("RGBA", (total_w, total_h), (0,0,0,0))
        shadow_layer.paste(shadow, (shadow_blur + offset[0], shadow_blur + offset[1]))
        shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(shadow_blur * 0.5))
        
        shadow_layer.paste(image, (shadow_blur, shadow_blur), image)
        return shadow_layer
