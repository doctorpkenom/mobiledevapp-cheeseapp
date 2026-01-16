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
            "bg": "assets/background.png",
            "rope": "assets/rope_progrss_bar.png",
            "mouse": "assets/mouse.png",
            "hook": "assets/gen_assets/rope_hook.png",
            "slider_knob": "assets/gen_assets/slider_knob.png",
            "slider_track": "assets/gen_assets/slider_track.png"
        }
        for key, path in assets_to_load.items():
            full_path = os.path.abspath(path)
            if os.path.exists(full_path):
                self.raw_images[key] = Image.open(full_path)
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

    # --- SCREENS ---
    
    def transition_to_welcome(self):
        self.current_screen = 'welcome'
        self.refresh_layout()

    def draw_welcome_screen(self, w, h):
        self.clear_ui()
        min_dim = min(w, h)

        # 1. Dialog Panel (Procedural)
        tw, th = int(w * 0.5), int(h * 0.25)
        if tw < 350: tw = 350
        
        # Generate Panel
        panel_img = self.ui_renderer.create_panel(tw, th, texture_key="texture_wood")
        panel_photo = ImageTk.PhotoImage(panel_img)
        self.images_cache["welcome_panel"] = panel_photo
        
        cx, cy = w/2, h * 0.25
        self.main_canvas.create_image(cx, cy, image=panel_photo, tags="ui")

        title_size = int(min_dim * 0.05)
        self.main_canvas.create_text(cx, cy, text="What Cheese\nAre You?", font=(self.default_font, title_size, 'bold'), 
                                     fill="#E65100", justify="center", tags="ui")

        # 2. Mascot
        ms = int(min_dim * 0.5)
        mphoto = self.resize_asset("mouse", ms, ms, "welcome_mouse")
        if mphoto:
            self.main_canvas.create_image(w*0.2, h*0.6, image=mphoto, tags="ui")

        # 3. Start Button (Procedural)
        bw, bh = 220, 70
        btn_img = self.ui_renderer.create_button(bw, bh, color="#FFB74D")
        btn_photo = ImageTk.PhotoImage(btn_img)
        self.images_cache["start_btn"] = btn_photo
        
        bx, by = w/2, h * 0.75
        bid = self.main_canvas.create_image(bx, by, image=btn_photo, tags="ui")
        tid = self.main_canvas.create_text(bx, by, text="Start The Roast", font=(self.default_font, 18, 'bold'), fill="white", tags="ui")
        
        cb = lambda e: self.start_game()
        self.main_canvas.tag_bind(bid, "<Button-1>", cb)
        self.main_canvas.tag_bind(tid, "<Button-1>", cb)

        self.main_canvas.create_text(w/2, by + 60, text="An existentially terrifying\npersonality quiz.", 
                                     font=(self.default_font, 12, 'italic'), fill="#333", justify="center", tags="ui")

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
        
        # 1. Rope & Hook
        rope_w, rope_h = int(w*0.8), 40
        rphoto = self.resize_asset("rope", rope_w, rope_h, "q_rope")
        if rphoto: self.main_canvas.create_image(w/2, 20, image=rphoto, anchor="n", tags="ui")
        
        # Hook
        hx, hy = w/2, 40
        hphoto = self.resize_asset("hook", 50, 50, "q_hook")
        if hphoto: self.main_canvas.create_image(hx, hy, image=hphoto, anchor="n", tags="ui")
        
        # 2. Paper Card (Question)
        qw, qh = int(w * 0.6), int(h * 0.3)
        qx, qy = w/2, hy + 40
        
        # Generate Paper
        paper_img = self.ui_renderer.create_paper_card(qw, qh)
        paper_photo = ImageTk.PhotoImage(paper_img)
        self.images_cache["q_paper"] = paper_photo
        
        self.main_canvas.create_image(qx, qy, image=paper_photo, anchor="n", tags="ui")
        
        # Text
        self.main_canvas.create_text(qx, qy + qh/2, text=q['text'], width=qw-60, 
                                     font=(self.default_font, int(min(w,h)*0.03), 'bold'), fill="#3E2723", justify="center", tags="ui")

        # 3. Inputs
        start_y = qy + qh + 20
        avail_h = h - start_y - 20
        if q['type'] == 'scale':
            self.draw_slider(start_y, q, w)
        else:
            self.draw_choices(start_y, q, w, avail_h)

    def draw_choices(self, start_y, question, w, area_h):
        opts = question.get('options', [])
        count = len(opts)
        spacing = 10
        btn_h = int((area_h - (spacing*count)) / count)
        if btn_h > 70: btn_h = 70
        if btn_h < 40: btn_h = 40
        
        btn_w = int(w*0.6)
        if btn_w < 300: btn_w = 300
        
        # Generate generic Texture Button/Tape
        # We can recycle one image if size is const, but size might change per resize.
        # We generate one per frame ideally, or cache by size.
        # For simplicity, generate new per frame (it's fast enough for <10 items).
        
        for i, opt in enumerate(opts):
            cy = start_y + i*(btn_h+spacing) + btn_h/2
            
            # Procedural Tape/Button
            # Let's use create_panel with 'tape' texture
            tape_img = self.ui_renderer.create_panel(btn_w, btn_h, radius=10, texture_key="texture_tape", border_color="#D7CCC8", border_width=1)
            tape_photo = ImageTk.PhotoImage(tape_img)
            self.images_cache[f"tape_{i}"] = tape_photo
            
            bid = self.main_canvas.create_image(w/2, cy, image=tape_photo, tags="ui")
            tid = self.main_canvas.create_text(w/2, cy, text=opt['label'], font=(self.default_font, 12, 'bold'), fill="#333", tags="ui")
            
            cb = lambda e, val=opt['value']: self.handle_answer(val)
            self.main_canvas.tag_bind(bid, "<Button-1>", cb)
            self.main_canvas.tag_bind(tid, "<Button-1>", cb)

    def draw_slider(self, start_y, question, w):
        # Track
        track_w, track_h = int(w*0.6), 40
        cx, cy = w/2, start_y + 40
        tphoto = self.resize_asset("slider_track", track_w, track_h, "sl_track")
        if tphoto: self.main_canvas.create_image(cx, cy, image=tphoto, tags="ui")
        
        # Knob
        kphoto = self.resize_asset("slider_knob", 50, 50, "sl_knob")
        self.knob_photo = kphoto # Ref
        
        min_x = cx - track_w/2 + 25
        max_x = cx + track_w/2 - 25
        self.slider_bounds = (min_x, max_x)
        self.slider_val = 0.5
        
        kx = min_x + (max_x - min_x) * 0.5
        self.knob_id = self.main_canvas.create_image(kx, cy, image=kphoto, tags="ui")
        
        # Bind
        self.main_canvas.tag_bind(self.knob_id, "<B1-Motion>", self.on_drag)
        
        # Labels
        self.main_canvas.create_text(min_x, cy-30, text=question['min_label'], anchor="w", font=(self.default_font, 10), tags="ui")
        self.main_canvas.create_text(max_x, cy-30, text=question['max_label'], anchor="e", font=(self.default_font, 10), tags="ui")

        # Confirm
        btn_w, btn_h = 160, 50
        btn_img = self.ui_renderer.create_button(btn_w, btn_h)
        bphoto = ImageTk.PhotoImage(btn_img)
        self.images_cache["cnf_btn"] = bphoto
        
        bx, by = w/2, cy + 70
        bid = self.main_canvas.create_image(bx, by, image=bphoto, tags="ui")
        tid = self.main_canvas.create_text(bx, by, text="Confirm", font=(self.default_font, 14, 'bold'), fill="white", tags="ui")
        
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
            
        cw, ch = int(w*0.7), int(h*0.7)
        cx, cy = w/2, h/2
        
        # Big Wood Panel
        bg_img = self.ui_renderer.create_panel(cw, ch, texture_key="texture_wood")
        bg_photo = ImageTk.PhotoImage(bg_img)
        self.images_cache["res_bg"] = bg_photo
        self.main_canvas.create_image(cx, cy, image=bg_photo, tags="ui")
        
        self.main_canvas.create_text(cx, cy - ch*0.4, text="You are...", font=(self.default_font, 18), fill="#3E2723", tags="ui")
        self.main_canvas.create_text(cx, cy - ch*0.3, text=res['name'], font=(self.default_font, 28, 'bold'), fill="#E65100", width=cw-40, justify="center", tags="ui")

        # Cheese
        img_path = os.path.join("assets", res['image'])
        if not os.path.isabs(img_path): img_path = os.path.abspath(img_path)
        if os.path.exists(img_path):
            pil_i = Image.open(img_path)
            isz = int(min(cw, ch) * 0.35)
            pil_i = pil_i.resize((isz, isz), Image.Resampling.LANCZOS)
            iphoto = ImageTk.PhotoImage(pil_i)
            self.images_cache["res_cheese"] = iphoto
            self.main_canvas.create_image(cx, cy, image=iphoto, tags="ui")

        self.main_canvas.create_text(cx, cy + ch*0.25, text=res['description'], width=cw-60, font=(self.default_font, 12), fill="#3E2723", justify="center", tags="ui")
        
        # Retry
        btn_w, btn_h = 180, 60
        btn_img = self.ui_renderer.create_button(btn_w, btn_h)
        bphoto = ImageTk.PhotoImage(btn_img)
        self.images_cache["retry_btn"] = bphoto
        
        by = cy + ch*0.4
        bid = self.main_canvas.create_image(cx, by, image=bphoto, tags="ui")
        tid = self.main_canvas.create_text(cx, by, text="Roast Again", font=(self.default_font, 16, 'bold'), fill="white", tags="ui")
        
        cb = lambda e: self.transition_to_welcome()
        self.main_canvas.tag_bind(bid, "<Button-1>", cb)
        self.main_canvas.tag_bind(tid, "<Button-1>", cb)

if __name__ == "__main__":
    app = CheeseApp()
    app.mainloop()
