# Quiz Module Documentation 🧠

This folder contains the core logic and data for the Cheese Personality Test (Reference Implementation).

## Files

### 1. `quiz_engine.py`
The brain of the operation. This Python class handles the game loop, scoring, and result calculation.

**Key Features:**

*   **Random Question Selection:**
    Picks 10 random questions from the pool to ensure every playthrough is different.
    ```python
    def start_new_game(self, num_questions=10):
        # ...
        count = min(len(self.questions), num_questions)
        self.current_session_questions = random.sample(self.questions, count)
    ```

*   **Lactose Intolerance Override:**
    The final question checks for lactose intolerance. If "Yes", the score is immediately forced to -100.
    ```python
    def submit_answer(self, value):
        if value == "LACTOSE_YES":
            self.current_score = -100
        # ...
    ```

*   **Coin Flip Scoring:**
    If a user's score falls between two cheese personalities, the engine randomly picks one (50/50 chance).
    ```python
    # If we are between two cheeses, flip a coin
    if lower_cheese and upper_cheese:
        return random.choice([lower_cheese, upper_cheese])
    ```

### 2. `questions.json`
The database of questions. Supports "scale" (slider) and "choice" (buttons) types.

**Snippet:**
```json
[
    {
        "id": 1,
        "type": "scale",
        "text": "How deeply do you regret your last major life decision?",
        "min_label": "No regrets (0)",
        "max_label": "Deep regret (10)"
    }
]
```

### 3. `cheeses.json`
The database of results. Each cheese has a target score.

**Snippet:**
```json
[
    {
        "name": "Mozzarella",
        "score": 0,
        "description": "You are soft, reliable, and unproblematic.",
        "image": "mozzarella.jpg"
    }
]
```
