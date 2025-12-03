from quiz.quiz_engine import QuizEngine
from tracker.tracker import Tracker
from assets.asset_manager import AssetManager
from interface_cli.interface_cli import Interface

def main():
    # 1. Initialize Modules
    quiz = QuizEngine()
    quiz.load_data()
    
    tracker = Tracker()
    assets = AssetManager()
    
    # 2. Launch Interface
    app = Interface(quiz, tracker, assets)
    app.run()

if __name__ == "__main__":
    main()
