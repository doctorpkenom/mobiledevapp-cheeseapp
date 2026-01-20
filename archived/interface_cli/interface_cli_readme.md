# Interface CLI Module Documentation 🖥️
 
 This folder handles the user interaction via the Command Line Interface (CLI).
 
 ## Files
 
 ### 1. `interface_cli.py`
 The face of the application. It coordinates the Quiz Engine, Tracker, and User Input.

**Key Features:**

*   **Main Menu Loop:**
    Keeps the application running until the user chooses to exit.
    ```python
    def run(self):
        while True:
            choice = input("1. Start Quiz\n2. View History\n3. Exit\n> ")
            if choice == "1":
                self.run_quiz()
            # ...
    ```

*   **Dynamic Question Display:**
    Handles different question types (Multiple Choice vs. Scale) and formats them for the terminal.
    ```python
    def display_question(self, question):
        print(f"\n[Q{self.quiz.question_index + 1}] {question['text']}")
        
        if question['type'] == 'choice':
            for i, opt in enumerate(question['options']):
                print(f"  {i+1}. {opt['label']}")
        elif question['type'] == 'scale':
            print(f"  Scale: {question['min_label']} (0) <---> {question['max_label']} (10)")
    ```

*   **Input Validation:**
    Ensures the user enters valid numbers and handles the special "Lactose Intolerance" check.
    ```python
    def get_user_input(self, question):
        # ...
        if question.get('id') == 999: # Lactose Question
            if user_in.lower() in ['1', 'yes', 'y']:
                return "LACTOSE_YES"
        # ...
    ```
