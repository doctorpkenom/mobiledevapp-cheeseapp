import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk, ImageDraw
import os
import json
import math
import random

# --- CONFIG ---
COLORS = {
    "bg": "#FFF9C4",      # Light Cream
    "card": "#FFFFFF",    # White
    "accent": "#FFB74D",  # Orange
    "accent_dark": "#F57C00", # Dark Orange
    "text": "#3E2723",    # Dark Brown
    "border": "#3E2723"   # Dark Brown
}
FONTS = {
    "title": ("Comic Sans MS", 32, "bold"),
    "header": ("Comic Sans MS", 20, "bold"),
    "body": ("Arial", 14),
    "button": ("Comic Sans MS", 16, "bold")
}

# --- ENGINE ---
class QuizEngine:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.questions = []
        self.cheeses = []
        self.score = 0
        self.q_index = 0
        self.session_qs = []
        
    def load(self):
        try:
            with open(os.path.join(self.data_dir, "questions.json"), 'r') as f:
                self.questions = json.load(f)
            with open(os.path.join(self.data_dir, "cheeses.json"), 'r') as f:
                self.cheeses = json.load(f)
        except Exception as e:
            print(f"Data Error: {e}")
            
    def new_game(self):
        self.score = 0
        self.q_index = 0
        self.session_qs = random.sample(self.questions, min(10, len(self.questions)))
        
    def get_current_question(self):
        if self.q_index < len(self.session_qs):
            return self.session_qs[self.q_index]
        return None
        
    def answer(self, val):
        if isinstance(val, int):
            self.score += val
        self.q_index += 1
        
    def get_result(self):
        # Simple closest match
        best_cheese = None
        min_diff = 999
        for c in self.cheeses:
            diff = abs(c['score'] - self.score)
            if diff < min_diff:
                min_diff = diff
                best_cheese = c
        return best_cheese

# --- UI APP ---
# --- UI APP ---
class CheeseApp(tk.Tk):
    def __init__(self, start_screen="HOME", test_data=None):
        super().__init__()
        self.title("Cheese Quest: Cute Edition")
        self.geometry("1000x700")
        self.config(bg=COLORS["bg"])
        
        # Paths
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        self.assets_dir = os.path.join(self.root_dir, "assets")
        self.quiz_dir = os.path.join(self.root_dir, "..", "quiz") 
        
        # Data
        self.engine = QuizEngine(self.quiz_dir)
        self.engine.load()
        
        # Test Data Injection
        if test_data:
            if 'q' in test_data:
                # Force specific question for testing
                self.engine.session_qs = [test_data['q']]
                self.engine.q_index = 0
            if 'res' in test_data:
                # Mock result engine
                self.engine.get_result = lambda: test_data['res']
        
        # Canvas
        self.canvas = Canvas(self, bg=COLORS["bg"], highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.width = 1000
        self.height = 700
        self.bind("<Configure>", self.on_resize)
        
        self.img_cache = {}
        self.anim_objects = []
        
        # Loop
        self.current_screen = start_screen # Configurable start
        if self.current_screen == "HOME":
            self.transition_to_home()
        elif self.current_screen == "QUIZ":
            self.transition_to_quiz()
        elif self.current_screen == "RESULT":
             self.transition_to_result()
             
        self.anim_loop()

    # ... (event handlers/helpers unchanged) ...
    def on_resize(self, event):
        if event.widget == self:
            self.width = event.width
            self.height = event.height
            self.redraw()
            
    def clear(self):
        self.canvas.delete("all")
        self.img_cache = {}
        
    def redraw(self):
        if self.current_screen == "HOME":
            self.draw_home()
        elif self.current_screen == "QUIZ":
            self.draw_quiz()
        elif self.current_screen == "RESULT":
            self.draw_result()

    # --- DRAWING HELPERS ---
    def draw_rounded_rect(self, x1, y1, x2, y2, r, fill, outline=None, width=1, tags=None):
        return self.draw_complex_rect(x1, y1, x2, y2, [r]*4, fill, outline, width, tags)

    def draw_fun_rect(self, x1, y1, x2, y2, fill, outline=None, width=1, tags=None):
        seed = int(x1 + y1)
        random.seed(seed)
        radii = [random.randint(15, 40) for _ in range(4)]
        return self.draw_complex_rect(x1, y1, x2, y2, radii, fill, outline, width, tags)

    def draw_complex_rect(self, x1, y1, x2, y2, radii, fill, outline, width, tags):
        r1, r2, r3, r4 = radii
        points = [
            x1+r1, y1, x2-r2, y1,
            x2, y1, x2, y1+r2,
            x2, y2-r3, x2, y2,
            x2-r3, y2, x1+r4, y2,
            x1, y2, x1, y2-r4,
            x1, y1+r1, x1, y1
        ]
        return self.canvas.create_polygon(points, smooth=True, fill=fill, outline=outline, width=width, tags=tags)
        
    def create_card_bg(self, text, y_offset=0):
        cw, ch = 800, 500
        cx, cy = self.width/2, self.height/2 + y_offset
        # Shadow (Fun)
        self.draw_fun_rect(cx-cw/2+10, cy-ch/2+10, cx+cw/2+10, cy+ch/2+10, "#D7CCC8")
        # Card (Fun)
        self.draw_fun_rect(cx-cw/2, cy-ch/2, cx+cw/2, cy+ch/2, COLORS["card"], COLORS["border"], 3)
        return cx, cy, cw, ch

    # --- SCREENS ---
    def transition_to_home(self):
        self.current_screen = "HOME"
        self.redraw()
        
    def draw_home(self):
        self.clear()
        cx, cy = self.width/2, self.height/2
        self.canvas.create_text(cx, cy-120, text="WHAT CHEESE\nARE YOU?", font=FONTS["title"], justify="center", fill=COLORS["text"])
        
        bx, by = cx, cy+100
        bw, bh = 220, 90
        
        self.draw_fun_rect(bx-bw/2+5, by-bh/2+5, bx+bw/2+5, by+bh/2+5, "#E65100")
        bid = self.draw_fun_rect(bx-bw/2, by-bh/2, bx+bw/2, by+bh/2, COLORS["accent"], COLORS["border"], 3)
        
        self.canvas.create_text(bx, by, text="LET'S GO!", font=FONTS["button"], fill="white")
        self.canvas.tag_bind(bid, "<Button-1>", lambda e: self.start_game())
        
    def start_game(self):
        self.engine.new_game()
        self.transition_to_quiz()
        
    def transition_to_quiz(self):
        self.current_screen = "QUIZ"
        self.redraw()
        
    def draw_quiz(self):
        self.clear()
        q = self.engine.get_current_question()
        if not q:
            self.transition_to_result()
            return

        cx, cy, cw, ch = self.create_card_bg(q['text'])
        
        self.canvas.create_text(cx, cy-120, text=q['text'], width=cw-80, font=FONTS["header"], justify="center", fill=COLORS["text"])
        
        opts = q.get('options', [])
        start_y = cy + 20
        
        if q['type'] == 'scale':
             self.draw_slider_component(cx, cy, start_y, q)
        else:
            cols = 2
            margin = 20
            bw = (cw - 100)/2
            bh = 70
            
            for i, opt in enumerate(opts):
                r = i // cols
                c = i % cols
                ox = (cx - cw/2 + 50) + c*(bw+margin) + bw/2
                oy = start_y + r*(bh+margin) + bh/2
                fill = COLORS["bg"]
                bid = self.draw_fun_rect(ox-bw/2, oy-bh/2, ox+bw/2, oy+bh/2, fill, COLORS["border"], 2)
                tid = self.canvas.create_text(ox, oy, text=opt['label'], width=bw-20, font=FONTS["body"], justify="center")
                cb = lambda e, v=opt['value']: self.answer(v)
                self.canvas.tag_bind(bid, "<Button-1>", cb)
                self.canvas.tag_bind(tid, "<Button-1>", cb)

    def draw_slider_component(self, cx, cy, start_y, q):
        min_x, max_x = cx - 250, cx + 250
        self.slider_bounds = (min_x, max_x)
        
        # Labels (Smaller and Wrap)
        # We put them slightly outside or allow wrapping and smaller font
        lbl_w = 120
        self.canvas.create_text(min_x - 10, start_y-40, text=q.get('min_label', 'No'), width=lbl_w, font=("Comic Sans MS", 10, "bold"), anchor="w", justify="left", fill=COLORS["text"])
        self.canvas.create_text(max_x + 10, start_y-40, text=q.get('max_label', 'Yes'), width=lbl_w, font=("Comic Sans MS", 10, "bold"), anchor="e", justify="right", fill=COLORS["text"])
        
        self.canvas.create_line(min_x, start_y, max_x, start_y, width=12, capstyle="round", fill=COLORS["accent_dark"])
        self.canvas.create_line(min_x, start_y, max_x, start_y, width=4, capstyle="round", fill="#FFF")
        
        if not hasattr(self, 'slider_val'): self.slider_val = 0.5
        kx = min_x + (max_x - min_x) * self.slider_val
        
        self.knob_id = self.canvas.create_oval(kx-20, start_y-20, kx+20, start_y+20, fill=COLORS["accent"], outline="black", width=2, tags="knob")
        self.canvas.create_oval(kx-10, start_y-10, kx-3, start_y-3, fill="#F57C00", outline="")
        
        self.canvas.tag_bind("knob", "<B1-Motion>", self.on_slider_drag)
        self.canvas.tag_bind("knob", "<Button-1>", self.on_slider_click)
        
        self.draw_fun_rect(cx-70, start_y+70, cx+70, start_y+120, COLORS["accent"], "black", 2, tags="btn")
        tid = self.canvas.create_text(cx, start_y+95, text="LOCK IT IN!", font=FONTS["button"], tags="btn_text")
        
        cb = lambda e: self.answer(int(self.slider_val * 10))
        self.canvas.tag_bind("btn", "<Button-1>", cb)
        self.canvas.tag_bind("btn_text", "<Button-1>", cb)

    def on_slider_click(self, event):
        pass

    def on_slider_drag(self, event):
        min_x, max_x = self.slider_bounds
        x = min(max(event.x, min_x), max_x)
        self.slider_val = (x - min_x) / (max_x - min_x)
        coords = self.canvas.coords(self.knob_id)
        cy = (coords[1] + coords[3]) / 2
        self.canvas.coords(self.knob_id, x-20, cy-20, x+20, cy+20) 

    def answer(self, val):
        self.engine.answer(val)
        if hasattr(self, 'slider_val'): del self.slider_val
        self.transition_to_quiz()
        
    def transition_to_result(self):
        self.current_screen = "RESULT"
        self.redraw()
        
    def draw_result(self):
        self.clear()
        res = self.engine.get_result()
        cx, cy, cw, ch = self.create_card_bg("")
        
        for i in range(0, 360, 30):
            rad = math.radians(i)
            rx = cx + math.cos(rad) * 400
            ry = cy + math.sin(rad) * 400
            self.canvas.create_line(cx, cy, rx, ry, width=20, fill="#FFF59D", tags="bg_deco")
        self.canvas.tag_lower("bg_deco")

        self.canvas.create_text(cx, cy-220, text="THE UNIVERSE SAYS...", font=FONTS["header"], fill=COLORS["text"])
        
        if res:
            try:
                img_name = os.path.basename(res['image'])
                path = os.path.join(self.assets_dir, img_name)
                
                if os.path.exists(path):
                    pil_img = Image.open(path)
                    pil_img.thumbnail((450, 450)) # Even larger max
                    pimg = ImageTk.PhotoImage(pil_img)
                    self.img_cache["res"] = pimg
                    # Scaled border
                    self.canvas.create_rectangle(cx-230, cy-85-35, cx+230, cy+110+35, fill="white", outline="#ccc", width=1)
                    self.canvas.create_image(cx, cy, image=pimg)
            except Exception as e:
                print(e)
                
            # Name (Wrapped tightly)
            self.canvas.create_text(cx, cy+180, text=res['name'].upper(), width=700, font=("Comic Sans MS", 24, "bold"), fill=COLORS["accent_dark"], justify="center")
            
            # Desc
            self.draw_fun_rect(cx-300, cy+230, cx+300, cy+320, COLORS["bg"], COLORS["border"], 1)
            self.canvas.create_text(cx, cy+275, text=res['description'], width=550, font=("Comic Sans MS", 12), justify="center")
            
        bx, by = cx, cy+360
        bid = self.draw_fun_rect(bx-120, by-35, bx+120, by+35, COLORS["accent"], "black", 2, tags="restart")
        tid = self.canvas.create_text(bx, by, text="ROAST ME AGAIN", font=FONTS["button"])
        
        cb = lambda e: self.transition_to_home()
        self.canvas.tag_bind("restart", "<Button-1>", cb)
        self.canvas.tag_bind(tid, "<Button-1>", cb)

    def anim_loop(self):
        self.after(20, self.anim_loop)

if __name__ == "__main__":
    app = CheeseApp()
    app.mainloop()
    def anim_loop(self):
        # Placeholder for polish 
        self.after(20, self.anim_loop)

if __name__ == "__main__":
    app = CheeseApp()
    app.mainloop()
