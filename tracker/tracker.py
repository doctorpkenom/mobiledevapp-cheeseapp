import json
import os
from datetime import datetime

class Tracker:
    def __init__(self, history_file="tracker/history.json"):
        self.history_file = history_file
        self.history = []
        self.load_history()

    def load_history(self):
        """Loads history from JSON file."""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    self.history = json.load(f)
            except json.JSONDecodeError:
                self.history = []
        else:
            self.history = []

    def save_result(self, cheese_name, score):
        """Saves a new result to history."""
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cheese": cheese_name,
            "score": score
        }
        self.history.append(entry)
        self._write_to_file()

    def _write_to_file(self):
        """Writes current history to JSON file."""
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=4)

    def get_last_result(self):
        """Returns the most recent result or None."""
        if self.history:
            return self.history[-1]
        return None

    def get_all_history(self):
        return self.history
