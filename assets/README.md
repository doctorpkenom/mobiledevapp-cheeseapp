# Assets Module Documentation 🎨

This folder manages the static resources (images, icons, etc.) for the application.

## Files

### 1. `asset_manager.py`
The librarian for file paths. It abstracts the file system so the rest of the app doesn't need to know exactly where images are stored.

**Key Features:**

*   **Safe Path Resolution:**
    Takes a filename and returns the full absolute path. If the file is missing, it returns `None` (and prints a warning) instead of crashing the app.
    ```python
    def get_image_path(self, image_name):
        full_path = os.path.join(self.assets_dir, image_name)
        if os.path.exists(full_path):
            return full_path
        
        print(f"Warning: Asset not found: {full_path}")
        return None
    ```

*   **Listing Assets:**
    Can return a list of all available files in the assets directory, useful for debugging or pre-loading.
    ```python
    def list_assets(self):
        return os.listdir(self.assets_dir)
    ```

### 2. Image Assets
- `background.png`: Main app background.
- `cheeses/`: Directory containing cheese result images.
- `icon_*.png`: UI icons.
