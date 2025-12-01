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
        """Resets score and picks random questions."""
        self.current_score = 0
        self.question_index = 0
        # Ensure we don't crash if we have fewer than num_questions
        count = min(len(self.questions), num_questions)
        self.current_session_questions = random.sample(self.questions, count)

    def get_next_question(self):
        """Returns the current question object or None if finished."""
        if self.question_index < len(self.current_session_questions):
            return self.current_session_questions[self.question_index]
        return None

    def submit_answer(self, points):
        """Adds points to score and advances index."""
        self.current_score += points
        self.question_index += 1

    def calculate_result(self):
        """Determines the cheese persona based on final score."""
        # Logic to be implemented: find cheese where score is within range
        pass
