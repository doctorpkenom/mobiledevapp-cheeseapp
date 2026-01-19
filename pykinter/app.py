import tkinter as tk
from tkinter import ttk, messagebox, font, Frame
from PIL import Image, ImageTk
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from quiz.quiz_engine import QuizEngine
from assets.asset_manager import AssetManager
from pykinter.ui_renderer import UIRenderer

class CheeseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("What Cheese Are You?")
        self.geometry("900x600")
        self.minsize(600, 400)
        
        # Managers
        self.asset_manager = AssetManager()
        self.quiz_engine = QuizEngine()
        self.quiz_engine.load_data()
        
        # Renderer
        self.ui_renderer = UIRenderer(os.path.abspath("assets"))
        
        # State
        self.current_screen = None 
        self.resize_timer = None
        self.images_cache = {} 
        self.raw_images = {}
        self.default_font = "Comic Sans MS"
        
        # Canvas
        self.main_canvas = tk.Canvas(self, highlightthickness=0, bg="#D7CCC8")
        self.main_canvas.pack(fill="both", expand=True)

        self.load_raw_assets()
        self.bind("<Configure>", self.on_resize)
        self.transition_to_welcome()

    def load_raw_assets(self):
        """Loads static assets (mascot, background). UI elements are generated."""
        assets_to_load = {
            "bg": "assets/bg_pattern.png",
            "rope": "assets/rope_knotted.png",
            "character_group": "assets/character_group.png",
            "logo": "assets/logo_main.png",
            "hook": "assets/rope_hook.png",
            "slider_knob": "assets/slider_knob_cheese.png",
            "slider_track": "assets/slider_track.png",
            "back_arrow": "assets/icon_back_arrow.png",
            "tape": "assets/texture_tape_strip.png"
        }
        for key, path in assets_to_load.items():
            full_path = os.path.abspath(path)
            if os.path.exists(full_path):
                img = Image.open(full_path)
                # Apply transparency to everything except the background pattern
                if key != "bg":
                    img = self.ui_renderer.make_white_transparent(img)
                self.raw_images[key] = img
            else:
                print(f"Warning: Missing asset {path}")

    def on_resize(self, event):
        if event.widget == self:
            if self.resize_timer:
                self.after_cancel(self.resize_timer)
            self.resize_timer = self.after(50, self.refresh_layout)

    def refresh_layout(self):
        w = self.winfo_width()
        h = self.winfo_height()
        if w <= 1 or h <= 1: return

        self.draw_background(w, h)
        if self.current_screen == 'welcome': self.draw_welcome_screen(w, h)
        elif self.current_screen == 'question': self.draw_question_screen(w, h)
        elif self.current_screen == 'result': self.draw_result_screen(w, h)

    def draw_background(self, w, h):
        self.main_canvas.delete("bg_layer")
        if "bg" in self.raw_images:
            img = self.raw_images["bg"].resize((w, h), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.images_cache["bg_resized"] = photo
            self.main_canvas.create_image(0, 0, image=photo, anchor="nw", tags="bg_layer")
            self.main_canvas.tag_lower("bg_layer")

    def resize_asset(self, key, w, h, cache_key):
        if key not in self.raw_images: return None
        img = self.raw_images[key].resize((int(w), int(h)), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        self.images_cache[cache_key] = photo
        return photo

    def clear_ui(self):
        self.main_canvas.delete("ui")
        for child in self.main_canvas.winfo_children():
            child.destroy()

    def draw_outlined_text(self, x, y, text, font_spec, fill, outline="white", width=0, justify="center", anchor="center"):
        """Simulates outlined text by drawing stroke layers."""
        if outline:
            # Draw offsets
            offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1)] # Simple 1px stroke
            for ox, oy in offsets:
                 self.main_canvas.create_text(x+ox, y+oy, text=text, font=font_spec, fill=outline, width=width, justify=justify, anchor=anchor, tags="ui")
        
        # Main text
        tid = self.main_canvas.create_text(x, y, text=text, font=font_spec, fill=fill, width=width, justify=justify, anchor=anchor, tags="ui")
        return tid

    # --- SCREENS ---
    
    def transition_to_welcome(self):
        self.current_screen = 'welcome'
        self.refresh_layout()

    def draw_welcome_screen(self, w, h):
        self.clear_ui()
        min_dim = min(w, h)

        # 1. Logo (Center Top) - pushed higher
        logo_w, logo_h = int(w * 0.5), int(h * 0.2)
        lphoto = self.resize_asset("logo", logo_w, logo_h, "welcome_logo")
        if lphoto:
            self.main_canvas.create_image(w/2, h*0.12, image=lphoto, tags="ui")

        # 2. Characters (Below Logo) - scaled down slightly
        cw = int(min_dim * 0.6) 
        cphoto = self.resize_asset("character_group", cw, cw*0.6, "welcome_chars") 
        if cphoto:
             self.main_canvas.create_image(w/2, h*0.38, image=cphoto, tags="ui")

        # 3. Dialog Panel (Yellow, Hand Drawn)
        tw, th = int(w * 0.8), int(h * 0.25) # Slightly taller for text
        panel_img = self.ui_renderer.create_panel(tw, th, texture_key="panel_yellow_large")
        panel_photo = ImageTk.PhotoImage(panel_img)
        self.images_cache["welcome_panel"] = panel_photo
        
        px, py = w/2, h * 0.68
        self.main_canvas.create_image(px, py, image=panel_photo, tags="ui")

        # Text with Outline Helper would be nice, but for now simple offsets
        self.draw_outlined_text(px, py-20, "WHO IS YOUR INNER DAIRY?", (self.default_font, int(min_dim*0.04), 'bold'), "black", "white")
        self.draw_outlined_text(px, py+25, "Discover if you are mild, spicy, or a biohazard.", (self.default_font, 12, 'italic'), "#333", None)

        # 4. Start Button (Orange)
        bw, bh = 280, 80
        # Check if we have the texture, else use renderer fallback
        # Assuming renderer.create_button can use texture or we draw via panel hack?
        # Let's use create_panel logic since it's just an image now? 
        # Actually UIRenderer.create_button generates shapes. We want the asset 'button_orange_large'.
        # We can implement a new draw_image_button in renderer or just load it here.
        # Let's load it here for simplicity.
        
        # Load asset directly via renderer helper (reusing create_panel logic which handles resizing)
        btn_img = self.ui_renderer.create_panel(bw, bh, texture_key="button_orange_large")
        btn_photo = ImageTk.PhotoImage(btn_img)
        self.images_cache["start_btn"] = btn_photo
        
        bx, by = w/2, h * 0.85
        bid = self.main_canvas.create_image(bx, by, image=btn_photo, tags="ui")
        tid = self.main_canvas.create_text(bx, by, text="START THE ROAST", font=(self.default_font, 18, 'bold'), fill="black", tags="ui")
        
        cb = lambda e: self.start_game()
        self.main_canvas.tag_bind(bid, "<Button-1>", cb)
        self.main_canvas.tag_bind(tid, "<Button-1>", cb)

    def start_game(self):
        self.quiz_engine.start_new_game()
        self.transition_to_question()

    def transition_to_question(self):
        self.current_screen = 'question'
        self.refresh_layout()

    def draw_question_screen(self, w, h):
        self.clear_ui()
        q = self.quiz_engine.get_next_question()
        if not q:
            self.transition_to_result()
            return
            
        # 1. Header & Back
        pad = 20
        # Back Arrow Icon
        bi_w, bi_h = 40, 40
        bphoto = self.resize_asset("back_arrow", bi_w, bi_h, "back_icon")
        if bphoto:
            self.main_canvas.create_image(pad+20, pad+20, image=bphoto, tags="ui")
        self.draw_outlined_text(pad+50, pad+20, "Back", (self.default_font, 12, 'bold'), "black", "white", anchor="w")
        
        q_idx = self.quiz_engine.question_index + 1
        total = 10 # approximate
        self.main_canvas.create_text(w/2, 40, text=f"Question {q_idx}/{total}", font=(self.default_font, 18, 'bold'), fill="#FDD835", tags="ui") # Simple fill, outline removed

        # 2. Progress Rope & Hook
        rope_w = int(w*0.8)
        rphoto = self.resize_asset("rope", rope_w, 40, "q_rope_h")
        if rphoto: self.main_canvas.create_image(w/2, 70, image=rphoto, tags="ui")
        
        # Hook (Center Top of rope)
        hphoto = self.resize_asset("hook", 40, 40, "q_hook")
        if hphoto: self.main_canvas.create_image(w/2, 50, image=hphoto, tags="ui")

        # 3. Question Panel (Cream) - Adding a solid white reading area on top
        qw, qh = int(w * 0.85), int(h * 0.25)
        qx, qy = w/2, h * 0.3
        
        panel_img = self.ui_renderer.create_panel(qw, qh, texture_key="panel_cream_large")
        panel_photo = ImageTk.PhotoImage(panel_img)
        self.images_cache["q_panel"] = panel_photo
        self.main_canvas.create_image(qx, qy, image=panel_photo, tags="ui")
        
        # Inner text box (translucent white)
        margin = 30
        tw, th = qw - margin*2, qh - margin*2
        # Center of panel is qx, qy
        # Top-left of text box
        tx1, ty1 = qx - tw/2, qy - th/2
        tx2, ty2 = qx + tw/2, qy + th/2
        
        # Draw rounded rect for text background
        # self.main_canvas.create_rectangle(tx1, ty1, tx2, ty2, fill="#FFFFFF", outline="", stipple="gray50", tags="ui") # Tkinter transparency is hard with stipple
        # Better: Solid cream/white overlay
        self.main_canvas.create_rectangle(tx1, ty1, tx2, ty2, fill="#FFF9C4", outline="#5D4037", width=2, tags="ui")
        
        self.main_canvas.create_text(qx, qy, text=q['text'], width=tw-20, font=(self.default_font, 13, 'bold'), fill="black", justify="center", tags="ui")

        # 4. Options
        start_y = qy + qh/2 + 20
        avail_h = h - start_y - 20
        
        if q['type'] == 'scale':
            self.draw_slider(start_y, q, w)
        else:
            self.draw_choices_grid(start_y, q, w, avail_h)

    def draw_choices_grid(self, start_y, question, w, avail_h):
        opts = question.get('options', [])
        cols = 2
        
        margin_x = w * 0.1
        btn_w = (w - 2*margin_x - 20) / 2
        btn_h = 70
        
        for i, opt in enumerate(opts):
            r = i // cols
            c = i % cols
            
            cx = margin_x + c*(btn_w+20) + btn_w/2
            cy = start_y + r*(btn_h+20) + btn_h/2
            
            # Button Background: "button_cream_strip" texture as base? 
            # User wants "simple solid colur backgrounds".
            # Let's use a solid beige/yellow rect with border
            
            # Shadow
            self.main_canvas.create_rectangle(cx-btn_w/2+4, cy-btn_h/2+4, cx+btn_w/2+4, cy+btn_h/2+4, fill="#3E2723", tags="ui")
            
            # Button Body
            bid = self.main_canvas.create_rectangle(cx-btn_w/2, cy-btn_h/2, cx+btn_w/2, cy+btn_h/2, fill="#FFECB3", outline="black", width=2, tags="ui")
            
            # Text
            tid = self.main_canvas.create_text(cx, cy, text=opt['label'], width=btn_w-10, font=(self.default_font, 10, 'bold'), fill="black", justify="center", tags="ui")
            
            cb = lambda e, val=opt['value']: self.handle_answer(val)
            self.main_canvas.tag_bind(bid, "<Button-1>", cb)
            self.main_canvas.tag_bind(tid, "<Button-1>", cb)

    def draw_slider(self, start_y, question, w):
        # Track
        track_w, track_h = int(w*0.6), 60 # bit taller for wobbly feel
        cx, cy = w/2, start_y + 40
        tphoto = self.resize_asset("slider_track", track_w, track_h, "sl_track")
        if tphoto: self.main_canvas.create_image(cx, cy, image=tphoto, tags="ui")
        
        # Knob (Cheese Wheel)
        kphoto = self.resize_asset("slider_knob", 60, 60, "sl_knob") 
        self.knob_photo = kphoto 
        
        min_x = cx - track_w/2 + 25
        max_x = cx + track_w/2 - 25
        self.slider_bounds = (min_x, max_x)
        self.slider_val = 0.5
        
        kx = min_x + (max_x - min_x) * 0.5
        self.knob_id = self.main_canvas.create_image(kx, cy, image=kphoto, tags="ui")
        
        # Bind
        self.main_canvas.tag_bind(self.knob_id, "<B1-Motion>", self.on_drag)
        
        # Labels
        self.draw_outlined_text(min_x, cy-40, question['min_label'], (self.default_font, 10, 'bold'), "black", "white", anchor="w")
        self.draw_outlined_text(max_x, cy-40, question['max_label'], (self.default_font, 10, 'bold'), "black", "white", anchor="e")

        # Confirm Button (Orange Large)
        btn_w, btn_h = 200, 65
        btn_img = self.ui_renderer.create_panel(btn_w, btn_h, texture_key="button_orange_large")
        bphoto = ImageTk.PhotoImage(btn_img)
        self.images_cache["cnf_btn"] = bphoto
        
        bx, by = w/2, cy + 80
        bid = self.main_canvas.create_image(bx, by, image=bphoto, tags="ui")
        tid = self.draw_outlined_text(bx, by, "LOCK IT IN!", (self.default_font, 14, 'bold'), "black", "white")
        
        cb = lambda e: self.confirm_slider()
        self.main_canvas.tag_bind(bid, "<Button-1>", cb)
        self.main_canvas.tag_bind(tid, "<Button-1>", cb)

    def on_drag(self, event):
        min_x, max_x = self.slider_bounds
        x = min(max(event.x, min_x), max_x)
        y = self.main_canvas.coords(self.knob_id)[1]
        self.main_canvas.coords(self.knob_id, x, y)
        self.slider_val = (x - min_x) / (max_x - min_x)

    def confirm_slider(self):
        val = round(self.slider_val * 10)
        self.handle_answer(val)

    def handle_answer(self, val):
        self.quiz_engine.submit_answer(val)
        self.transition_to_question()

    def transition_to_result(self):
        self.current_screen = 'result'
        self.refresh_layout()

    def draw_result_screen(self, w, h):
        self.clear_ui()
        res = self.quiz_engine.calculate_result()
        if not res: 
            self.transition_to_welcome()
            return
            
        cx, cy = w/2, h/2
        
        # 1. Header
        self.main_canvas.create_text(cx, h*0.1, text="The Universe has spoken...", font=(self.default_font, 20, 'bold'), fill="#FDD835", tags="ui")

        # 2. Polaroid Result
        pw, ph = 300, 360 # Frame size
        
        # Load Frame Asset
        frame_asset_path = os.path.join("assets", "frame_polaroid.png")
        if os.path.exists(frame_asset_path):
             frame_img = Image.open(frame_asset_path).convert("RGBA").resize((pw, ph), Image.Resampling.LANCZOS)
             frame_img = self.ui_renderer.make_white_transparent(frame_img) # Just in case
             
             # Locate Cheese Image
             img_path = os.path.join("assets", res['image'])
             if not os.path.isabs(img_path): img_path = os.path.abspath(img_path)
             
             if os.path.exists(img_path):
                 cheese_img = Image.open(img_path).convert("RGBA")
                 # Scale cheese to fit inside frame window (approx 80% width, top offset)
                 cw_sz = int(pw * 0.75)
                 cheese_img = cheese_img.resize((cw_sz, cw_sz), Image.Resampling.LANCZOS)
                 
                 # Create composite
                 final_polaroid = Image.new("RGBA", (pw, ph), (0,0,0,0))
                 # Paste cheese first
                 final_polaroid.paste(cheese_img, (int((pw-cw_sz)/2), 50), cheese_img)
                 # Paste frame on top
                 final_polaroid.paste(frame_img, (0,0), frame_img)
                 
                 frame_photo = ImageTk.PhotoImage(final_polaroid)
                 self.images_cache["res_polaroid"] = frame_photo
                 self.main_canvas.create_image(cx, h*0.4, image=frame_photo, tags="ui")

        # 3. Label & Desc
        self.main_canvas.create_text(cx, h*0.62, text=res['name'].upper(), font=(self.default_font, 24, 'bold'), fill="black", tags="ui")
        
        # Desc Panel (Cream Small)
        dw, dh = int(w*0.8), int(h*0.15)
        d_panel_img = self.ui_renderer.create_panel(dw, dh, texture_key="panel_cream_small")
        d_photo = ImageTk.PhotoImage(d_panel_img)
        self.images_cache["res_desc_panel"] = d_photo
        self.main_canvas.create_image(cx, h*0.75, image=d_photo, tags="ui")
        
        self.main_canvas.create_text(cx, h*0.75, text=res['description'], width=dw-40, font=(self.default_font, 12), fill="black", justify="center", tags="ui")

        # 4. Buttons
        btn_w, btn_h = 240, 60
        btn_img = self.ui_renderer.create_panel(btn_w, btn_h, texture_key="button_orange_large")
        bphoto = ImageTk.PhotoImage(btn_img)
        self.images_cache["share_btn"] = bphoto
        
        by = h * 0.88
        bid = self.main_canvas.create_image(cx, by, image=bphoto, tags="ui")
        tid = self.main_canvas.create_text(cx, by, text="SHARE DISASTER", font=(self.default_font, 16, 'bold'), fill="black", tags="ui")
        
        # Retake Link
        rtid = self.main_canvas.create_text(cx, by + 40, text="Retake Quiz", font=(self.default_font, 12, 'underline'), fill="#333", tags="ui")
        
        cb = lambda e: self.transition_to_welcome()
        self.main_canvas.tag_bind(rtid, "<Button-1>", cb)
        self.main_canvas.tag_bind(bid, "<Button-1>", cb)

if __name__ == "__main__":
    app = CheeseApp()
    app.mainloop()
