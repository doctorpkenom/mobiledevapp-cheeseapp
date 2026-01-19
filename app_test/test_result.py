from main import CheeseApp

RES_DATA = {
    'name': "Parmesan: The Hard-Core Traditionalist",
    'description': "You are solid, aged, and very, very loud when grated (stressed). You believe in doing things the 'right' way.",
    'image': "cheeses/parmesan.png" # Ensure this exists in test/assets/parmesan.png or adjust logic
}

if __name__ == "__main__":
    # main.py logic expects flat assets in assets_dir usually, let's see. 
    # Logic: os.path.basename(res['image']) -> parmesan.png
    app = CheeseApp(start_screen="RESULT", test_data={'res': RES_DATA})
    app.mainloop()
