from quiz.quiz_engine import QuizEngine

def test_quiz():
    engine = QuizEngine()
    engine.load_data()
    
    print(f"Loaded {len(engine.questions)} questions and {len(engine.cheeses)} cheeses.")
    
    # Test 1: Normal Game
    print("\n--- Test 1: Normal Game ---")
    engine.start_new_game()
    print(f"Session has {len(engine.current_session_questions)} questions.")
    
    # Answer first 10 questions with random points
    for i in range(10):
        q = engine.get_next_question()
        print(f"Q{i+1}: {q['text']}")
        engine.submit_answer(5) # Give 5 points for each
        
    # Answer last question (Lactose) with NO
    q = engine.get_next_question()
    print(f"Q11: {q['text']}")
    engine.submit_answer(0)
    
    result = engine.calculate_result()
    print(f"Final Score: {engine.current_score}")
    print(f"Result: {result['name']}")
    
    # Test 2: Lactose Intolerant Game
    print("\n--- Test 2: Lactose Intolerant Game ---")
    engine.start_new_game()
    
    # Answer first 10 questions
    for i in range(10):
        engine.get_next_question()
        engine.submit_answer(10) # Max points
        
    # Answer last question (Lactose) with YES
    q = engine.get_next_question()
    print(f"Q11: {q['text']}")
    engine.submit_answer("LACTOSE_YES")
    
    result = engine.calculate_result()
    print(f"Final Score: {engine.current_score}")
    print(f"Result: {result['name']}")

if __name__ == "__main__":
    test_quiz()
