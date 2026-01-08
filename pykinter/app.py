import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from quiz.quiz_engine import QuizEngine
from assets.asset_manager import AssetManager

# --- CONSTANTS & STYLES ---
WINDOW_WIDTH = 450
WINDOW_HEIGHT = 850
BG_COLOR = "#FFF8E1" # Cream
PRIMARY_COLOR = "#FFB74D" # Orange
ACCENT_COLOR = "#FDD835" # Yellow
TEXT_COLOR = "#1a1a1a"

class CheeseApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("What Cheese Are You?")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)
        self.configure(bg=BG_COLOR)

        # Managers
        self.asset_manager = AssetManager()
        self.quiz_engine = QuizEngine()
        self.quiz_engine.load_data()

        # Styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background=BG_COLOR)
        self.style.configure('TLabel', background=BG_COLOR, foreground=TEXT_COLOR, font=('Helvetica', 14))
        self.style.configure('Title.TLabel', font=('Helvetica', 28, 'bold'), foreground=PRIMARY_COLOR)
        
        # Primary Button (Matches "Sticker" look)
        self.style.configure('Primary.TButton', 
            font=('Helvetica', 16, 'bold'), 
            background=PRIMARY_COLOR, 
            foreground=TEXT_COLOR, 
            borderwidth=3,
            relief="raised",
            padding=10
        )
        self.style.map('Primary.TButton',
            background=[('active', '#FFA726')],
            relief=[('pressed', 'sunken')]
        )

        # Option Button
        self.style.configure('Option.TButton', 
            font=('Helvetica', 12), 
            background=BG_COLOR, 
            foreground=TEXT_COLOR, 
            borderwidth=2,
            relief="solid",
            padding=10,
            width=30
        )
        
        # State
        self.current_frame = None

        # Start
        self.show_welcome_screen()

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
    
    def load_image(self, relative_path, size=None):
        full_path = os.path.abspath(relative_path)
        if not os.path.exists(full_path):
            return None  
        try:
            pil_img = Image.open(full_path)
            if size:
                pil_img = pil_img.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(pil_img)
        except Exception as e:
            print(f"Error loading image: {e}")
            return None

    # --- SCREENS ---

    def show_welcome_screen(self):
        self.clear_frame()
        self.current_frame = ttk.Frame(self)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        title_label = ttk.Label(self.current_frame, text="What Cheese\nAre You?", style="Title.TLabel", justify="center")
        title_label.pack(pady=(50, 20))

        mouse_img = self.load_image("assets/mouse.png", (200, 200))
        if mouse_img:
            lbl = ttk.Label(self.current_frame, image=mouse_img)
            lbl.image = mouse_img
            lbl.pack(pady=20)
        else:
            ttk.Label(self.current_frame, text="🧀", font=("System", 100)).pack(pady=20)

        desc_label = ttk.Label(self.current_frame, text="An existentially terrifying\npersonality quiz.", justify="center")
        desc_label.pack(pady=20)

        start_btn = ttk.Button(self.current_frame, text="Start The Roast", style="Primary.TButton", command=self.start_game)
        start_btn.pack(side=tk.BOTTOM, pady=50)

    def start_game(self):
        self.quiz_engine.start_new_game()
        self.show_question_screen()

    def show_question_screen(self):
        self.clear_frame()
        q = self.quiz_engine.get_next_question()
        
        if not q:
            self.show_result_screen()
            return

        self.current_frame = ttk.Frame(self)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Question Countdown
        count_label = ttk.Label(self.current_frame, text=f"Question {self.quiz_engine.question_index + 1}", font=("Helvetica", 10, 'bold'))
        count_label.pack(pady=(10, 5))

        # Question Card
        q_frame = tk.Frame(self.current_frame, bg="#FFF8E1", bd=3, relief="solid")
        q_frame.pack(pady=20, fill=tk.X, ipady=20)
        
        q_text = tk.Label(q_frame, text=q['text'], bg="#FFF8E1", fg=TEXT_COLOR, font=("Helvetica", 16, "bold"), wraplength=350)
        q_text.pack(padx=10, pady=10)

        # Content Area (Options or Slider)
        content_frame = ttk.Frame(self.current_frame)
        content_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        if q['type'] == 'scale':
            self.render_slider(content_frame, q)
        else:
            self.render_choices(content_frame, q)

    def render_choices(self, parent, question):
        for opt in question.get('options', []):
            btn = ttk.Button(parent, text=opt['label'], style="Option.TButton", 
                             command=lambda val=opt['value']: self.handle_answer(val))
            btn.pack(pady=5, fill=tk.X)

    def render_slider(self, parent, question):
        # Min/Max Labels
        labels_frame = ttk.Frame(parent)
        labels_frame.pack(fill=tk.X, pady=(0, 10))
        
        min_lbl = ttk.Label(labels_frame, text=question.get('min_label', '0'), font=("Helvetica", 10, 'italic'), wraplength=150)
        min_lbl.pack(side=tk.LEFT, anchor='w')
        
        max_lbl = ttk.Label(labels_frame, text=question.get('max_label', '100'), font=("Helvetica", 10, 'italic'), wraplength=150, justify='right')
        max_lbl.pack(side=tk.RIGHT, anchor='e')

        # Slider Widget
        # Range 0-100, no ticks, custom appearance
        self.slider_var = tk.DoubleVar(value=50) # Middle default
        
        scale = tk.Scale(parent, from_=0, to=100, orient=tk.HORIZONTAL, 
                         variable=self.slider_var, 
                         bg=BG_COLOR, fg=TEXT_COLOR, highlightthickness=0,
                         bd=0, activebackground=PRIMARY_COLOR, length=300,
                         resolution=1,
                         sliderlength=25, # Makes the handle squarish
                         width=25, # Thicker track
                         showvalue=0, # Hide value number
                         troughcolor="#E0E0E0",
                         sliderrelief="flat" # Cleaner look
                         )
        
        # Click to jump binding
        scale.bind("<Button-1>", lambda event: self.move_scale(event, scale))
                         
        scale.pack(pady=20, fill=tk.X)

        # Removed the self.value_label update logic as requested

        # Submit Button
        # Normalization: value (0-100) / 10 -> rounded -> (0-10)
        submit_btn = ttk.Button(parent, text="Confirm Choice", style="Primary.TButton", 
                                command=lambda: self.handle_answer(round(self.slider_var.get() / 10)))
        submit_btn.pack(pady=20)

    def move_scale(self, event, scale_widget):
        # Calculate value based on x position
        x = event.x
        width = scale_widget.winfo_width()
        
        if width > 0:
            pct = x / width
            # Clamp
            pct = max(0, min(1, pct))
            new_val = pct * 100
            scale_widget.set(new_val)

    def handle_answer(self, value):
        self.quiz_engine.submit_answer(value)
        self.show_question_screen()

    def show_result_screen(self):
        self.clear_frame()
        result = self.quiz_engine.calculate_result()
        
        if not result:
            messagebox.showerror("Error", "Could not calculate result.")
            self.show_welcome_screen()
            return

        self.current_frame = ttk.Frame(self)
        self.current_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        ttk.Label(self.current_frame, text="You are...", font=("Helvetica", 18)).pack(pady=(30, 10))
        
        name_label = ttk.Label(self.current_frame, text=result['name'], font=("Helvetica", 22, "bold"), wraplength=400, justify="center")
        name_label.pack(pady=10)

        img_path = os.path.join("assets", result['image'])
        cheese_img = self.load_image(img_path, (300, 300))
        
        if cheese_img:
            lbl = ttk.Label(self.current_frame, image=cheese_img)
            lbl.image = cheese_img
            lbl.pack(pady=10)
        else:
            ttk.Label(self.current_frame, text="(Image Missing)", foreground="red").pack(pady=20)

        desc_frame = tk.Frame(self.current_frame, bg="white", bd=2, relief="solid")
        desc_frame.pack(pady=10, fill=tk.X, ipadx=10, ipady=10)
        
        desc_label = tk.Label(desc_frame, text=result['description'], bg="white", fg=TEXT_COLOR, font=("Helvetica", 12), wraplength=380, justify="center")
        desc_label.pack()

        retry_btn = ttk.Button(self.current_frame, text="Roast Again", style="Primary.TButton", command=self.show_welcome_screen)
        retry_btn.pack(side=tk.BOTTOM, pady=30)


if __name__ == "__main__":
    app = CheeseApp()
    app.mainloop()
