# Tests Module Documentation 🧪

This folder contains verification scripts to ensure the application works as expected. These scripts are crucial for maintaining code quality and preventing regressions.

## Files

### 1. `test_quiz.py`
Verifies the logic of the `QuizEngine`.

**Key Tests:**
*   **Normal Game Flow:** Simulates a standard 10-question run.
*   **Lactose Intolerance:** Verifies that answering "Yes" to the final question forces the score to -100.
*   **Coin Flip Logic:** Forces a score between two cheeses (e.g., 32) and runs it multiple times to ensure the result flips between the two neighbors.
    ```python
    # Test 3: Coin Flip Logic
    engine.current_score = 32
    # ...
    for _ in range(5):
        r = engine.calculate_result()
        # Should see a mix of "Gouda" and "Pepper Jack"
    ```

### 2. `test_tracker.py`
Verifies the `Tracker` module.

**Key Tests:**
*   **Persistence:** Saves a result, reloads the tracker from the file, and checks if the data is still there.
    ```python
    tracker.save_result("Cheddar", 50)
    # ...
    tracker2 = Tracker(history_file=test_file)
    if len(tracker2.get_all_history()) == 2:
        print("SUCCESS: History persisted.")
    ```

### 3. `test_assets.py`
Verifies the `AssetManager`.

**Key Tests:**
*   **Existence Check:** Confirms it can find a real file.
*   **Missing File Handling:** Confirms it returns `None` (instead of crashing) when asked for a non-existent file.

## How to Run Tests
From the root directory of the project, run:
```bash
python -m tests.test_quiz
python -m tests.test_tracker
python -m tests.test_assets
```
