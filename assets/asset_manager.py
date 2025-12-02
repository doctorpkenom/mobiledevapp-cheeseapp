import os

class AssetManager:
    def __init__(self, assets_dir="assets"):
        self.assets_dir = assets_dir

    def get_image_path(self, image_name):
        """Returns the full path to an image file. Returns None if not found."""
        full_path = os.path.join(self.assets_dir, image_name)
        if os.path.exists(full_path):
            return full_path
        
        # Fallback for development (if image doesn't exist yet)
        print(f"Warning: Asset not found: {full_path}")
        return None

    def list_assets(self):
        """Returns a list of all files in the assets directory."""
        if os.path.exists(self.assets_dir):
            return os.listdir(self.assets_dir)
        return []
