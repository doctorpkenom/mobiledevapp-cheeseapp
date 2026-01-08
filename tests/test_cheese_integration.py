from assets.asset_manager import AssetManager
import json
import os

def test_integration():
    manager = AssetManager() # Default 'assets'
    
    with open('quiz/cheeses.json', 'r') as f:
        cheeses = json.load(f)
        
    print(f"Checking {len(cheeses)} cheeses...")
    all_good = True
    
    for c in cheeses:
        raw_path = c['image']
        # The AssetManager joins 'assets' + raw_path. 
        # If raw_path is 'assets/cheeses/foo.png', result is 'assets/assets/cheeses/foo.png' which is wrong.
        # Let's see what happens.
        resolved = manager.get_image_path(raw_path)
        
        if resolved:
            print(f"OK: {c['name']} -> {resolved}")
        else:
            print(f"FAILED: {c['name']} -> {raw_path}")
            # Try to debug why
            expected = os.path.join("assets", raw_path)
            print(f"   Looked at: {expected}")
            all_good = False

    if all_good:
        print("ALL ASSETS RESOLVED PERFECTLY")
    else:
        print("SOME ASSETS FAILED TO RESOLVE")

if __name__ == "__main__":
    test_integration()
