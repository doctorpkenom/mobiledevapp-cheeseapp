from assets.asset_manager import AssetManager
import os

def test_assets():
    # Create a dummy asset for testing
    dummy_file = "assets/test_image.png"
    with open(dummy_file, 'w') as f:
        f.write("dummy content")

    print("--- Testing Asset Manager ---")
    manager = AssetManager()
    
    # Test finding an existing asset
    path = manager.get_image_path("test_image.png")
    print(f"Found asset: {path}")
    
    if path and os.path.exists(path):
        print("SUCCESS: Asset found.")
    else:
        print("FAILURE: Asset not found.")
        
    # Test missing asset
    missing = manager.get_image_path("ghost.png")
    if missing is None:
        print("SUCCESS: Missing asset handled correctly.")
    else:
        print(f"FAILURE: Found non-existent asset: {missing}")

    # Cleanup
    if os.path.exists(dummy_file):
        os.remove(dummy_file)

if __name__ == "__main__":
    test_assets()
