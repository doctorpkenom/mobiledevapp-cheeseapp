# Tracker Module Documentation 📝

This folder handles the "Memory" of the application, ensuring user progress is saved.

## Files

### 1. `tracker.py`
The persistence manager. It handles reading and writing to the JSON history file.

**Key Features:**

*   **Saving Results:**
    Appends a new entry with the current timestamp, cheese name, and score.
    ```python
    def save_result(self, cheese_name, score):
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cheese": cheese_name,
            "score": score
        }
        self.history.append(entry)
        self._write_to_file()
    ```

*   **Loading History:**
    Safely loads the JSON file, handling cases where the file might be missing or empty.
    ```python
    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                self.history = json.load(f)
    ```

### 2. `history.json`
*Note: This file is generated automatically when you run the app.*

It stores the user's past results in a simple JSON list.

**Example Content:**
```json
[
    {
        "date": "2023-10-27 14:30:00",
        "cheese": "Cheddar",
        "score": 45
    },
    {
        "date": "2023-10-28 09:15:00",
        "cheese": "Brie",
        "score": 12
    }
]
```
