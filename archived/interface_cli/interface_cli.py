class Interface:
    def __init__(self, quiz_engine, tracker, asset_manager):
        self.quiz = quiz_engine
        self.tracker = tracker
        self.assets = asset_manager

    def run(self):
        """Main loop for the interface."""
        print("\n--- WELCOME TO THE CHEESE PERSONALITY TEST ---")
        print("Prepare to be judged by dairy products.\n")
        
        while True:
            choice = input("1. Start Quiz\n2. View History\n3. Exit\n> ")
            
            if choice == "1":
                self.run_quiz()
            elif choice == "2":
                self.show_history()
            elif choice == "3":
                print("Stay cheesy!")
                break
            else:
                print("Invalid choice. Try again.")

    def run_quiz(self):
        """Runs a single quiz session."""
        self.quiz.start_new_game()
        print("\nStarting Quiz... (Answer 0-10 or pick an option)\n")
        
        while True:
            question = self.quiz.get_next_question()
            if not question:
                break
            
            self.display_question(question)
            answer = self.get_user_input(question)
            self.quiz.submit_answer(answer)
            
        result = self.quiz.calculate_result()
        self.show_result(result)

    def display_question(self, question):
        print(f"\n[Q{self.quiz.question_index + 1}] {question['text']}")
        
        if question['type'] == 'choice':
            for i, opt in enumerate(question['options']):
                print(f"  {i+1}. {opt['label']}")
        elif question['type'] == 'scale':
            print(f"  Scale: {question['min_label']} (0) <---> {question['max_label']} (10)")

    def get_user_input(self, question):
        while True:
            try:
                user_in = input("Your answer > ")
                
                # Special Lactose Check
                if question.get('id') == 999: # Lactose Question
                    if user_in.lower() in ['1', 'yes', 'y']:
                        return "LACTOSE_YES"
                    return 0

                if question['type'] == 'choice':
                    idx = int(user_in) - 1
                    if 0 <= idx < len(question['options']):
                        return question['options'][idx]['value']
                
                elif question['type'] == 'scale':
                    val = int(user_in)
                    if 0 <= val <= 10:
                        return val
                        
                print("Invalid input. Please try again.")
            except ValueError:
                print("Please enter a number.")

    def show_result(self, cheese):
        print("\n" + "="*40)
        print(f"YOU ARE: {cheese['name']}")
        print("="*40)
        print(f"\n{cheese['description']}\n")
        
        # Save result
        self.tracker.save_result(cheese['name'], self.quiz.current_score)
        input("Press Enter to continue...")

    def show_history(self):
        history = self.tracker.get_all_history()
        print("\n--- Quiz History ---")
        if not history:
            print("No history yet.")
        else:
            for entry in history:
                print(f"[{entry['date']}] {entry['cheese']} (Score: {entry['score']})")
        print("")
