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
        """Determines the cheese persona based on final score."""
        # If they are lactose intolerant, they are the Wisp (-100)
        if self.current_score == -100:
            # Find the specific Wisp entry or fallback
            for cheese in self.cheeses:
                if cheese.get("score") == -100:
                    return cheese
        
        # Normal logic: Find the closest match or range
        # The cheeses.json uses "score" as a target/min value. 
        # Let's assume we find the cheese with the highest score that is <= current_score
        # Sort cheeses by score descending to find the best match
        
        sorted_cheeses = sorted(self.cheeses, key=lambda x: x.get("score", 0), reverse=True)
        
        for cheese in sorted_cheeses:
            if self.current_score >= cheese.get("score", 0):
                return cheese
                
        # Fallback to the lowest scoring cheese if nothing matches
        return sorted_cheeses[-1] if sorted_cheeses else None
