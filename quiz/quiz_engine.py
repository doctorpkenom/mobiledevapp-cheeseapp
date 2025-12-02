import json
import random

class QuizEngine:
    def __init__(self, questions_file="quiz/questions.json", cheeses_file="quiz/cheeses.json"):
        self.questions_file = questions_file
        self.cheeses_file = cheeses_file
        self.questions = []
        self.cheeses = []
        self.current_score = 0
        self.current_session_questions = []
        self.question_index = 0

    def load_data(self):
        """Loads questions and cheeses from JSON files."""
        try:
            with open(self.questions_file, 'r') as f:
                self.questions = json.load(f)
            with open(self.cheeses_file, 'r') as f:
                self.cheeses = json.load(f)
        except FileNotFoundError:
            print("Error: Data files not found.")
            self.questions = []
            self.cheeses = []

    def start_new_game(self, num_questions=10):
        """Resets score and picks random questions + mandatory lactose question."""
        self.current_score = 0
        self.question_index = 0
        
        # 1. Pick 10 random questions
        # Ensure we don't crash if we have fewer than num_questions
        count = min(len(self.questions), num_questions)
        self.current_session_questions = random.sample(self.questions, count)
        
        # 2. Add the mandatory Lactose Intolerant question
        lactose_question = {
            "id": 999,
            "type": "choice",
            "text": "Final Question: Are you lactose intolerant?",
            "options": [
                {"label": "Yes, sadly.", "value": "LACTOSE_YES"}, 
                {"label": "No, I am strong.", "value": 0}
            ]
        }
        self.current_session_questions.append(lactose_question)

    def get_next_question(self):
        """Returns the current question object or None if finished."""
        if self.question_index < len(self.current_session_questions):
            return self.current_session_questions[self.question_index]
        return None

    def submit_answer(self, value):
        """Adds points to score and advances index. Handles special lactose override."""
        # Check for the special lactose flag
        if value == "LACTOSE_YES":
            self.current_score = -100
        else:
            # Only add points if it's not the lactose override (which sets it directly)
            # and if the current score isn't already -100 (though this is the last question anyway)
            if isinstance(value, (int, float)):
                self.current_score += value
        
        self.question_index += 1

    def calculate_result(self):
        """Determines the cheese persona based on final score with Coin Flip Rounding."""
        # 1. Handle Special Cases (Lactose Intolerant)
        if self.current_score == -100:
            for cheese in self.cheeses:
                if cheese.get("score") == -100:
                    return cheese
            return None # Should not happen if data is correct

        # 2. Find Exact Match
        for cheese in self.cheeses:
            if cheese.get("score") == self.current_score:
                return cheese

        # 3. No Exact Match -> Find Neighbors (Floor and Ceiling)
        # Sort cheeses by score
        sorted_cheeses = sorted(self.cheeses, key=lambda x: x.get("score", 0))
        
        lower_cheese = None
        upper_cheese = None

        for cheese in sorted_cheeses:
            s = cheese.get("score", 0)
            if s < self.current_score:
                lower_cheese = cheese
            elif s > self.current_score:
                upper_cheese = cheese
                break # Found the immediate upper bound

        # 4. Coin Flip Logic
        # If we are between two cheeses, flip a coin
        if lower_cheese and upper_cheese:
            return random.choice([lower_cheese, upper_cheese])
        
        # Edge Cases: Score is lower than lowest cheese or higher than highest
        if lower_cheese and not upper_cheese:
            return lower_cheese # Higher than max -> return max
        if upper_cheese and not lower_cheese:
            return upper_cheese # Lower than min -> return min
            
        return None
