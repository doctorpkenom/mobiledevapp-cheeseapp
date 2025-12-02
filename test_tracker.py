from tracker.tracker import Tracker
import os

def test_tracker():
    # Clean up previous test file
    test_file = "tracker/test_history.json"
    if os.path.exists(test_file):
        os.remove(test_file)

    print("--- Testing Tracker ---")
    tracker = Tracker(history_file=test_file)
    
    print("Initial history:", tracker.get_all_history())
    
    print("Saving result: Cheddar (Score 50)")
    tracker.save_result("Cheddar", 50)
    
    print("Saving result: Brie (Score 10)")
    tracker.save_result("Brie", 10)
    
    last = tracker.get_last_result()
    print(f"Last result: {last['cheese']} at {last['date']}")
    
    # Reload to check persistence
    print("Reloading tracker...")
    tracker2 = Tracker(history_file=test_file)
    print(f"History count: {len(tracker2.get_all_history())}")
    
    if len(tracker2.get_all_history()) == 2:
        print("SUCCESS: History persisted.")
    else:
        print("FAILURE: History lost.")

    # Cleanup
    if os.path.exists(test_file):
        os.remove(test_file)

if __name__ == "__main__":
    test_tracker()
