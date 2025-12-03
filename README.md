# Cheese Personality Test 🧀

A playful, nostalgic, and slightly chaotic personality test app. Answer questions, get judged by dairy products, and find out if you are a "Reliable Cheddar" or a "Certified Biohazard Vieux-Boulogne".

## 🚀 Features
- **30+ Questions**: Ranging from deep philosophical inquiries to laundry habits.
- **Coin Flip Scoring**: If you fall between two cheese personalities, a coin flip decides your fate.
- **Lactose Intolerance Mode**: A secret ending for the weak of stomach.
- **History Tracker**: Remembers your past results so you can see your evolution.
- **Modular Design**: Built with separate modules for Quiz Logic, Interface, Assets, and Tracking.

## 📂 Project Structure
```
/mobiledevapp-cheeseapp
├── /quiz           # The Brain (Logic & Data)
│   ├── quiz_engine.py
│   ├── questions.json
│   └── cheeses.json
├── /tracker        # The Memory (History)
│   ├── tracker.py
│   └── history.json
├── /assets         # The Looks (Images)
│   └── asset_manager.py
├── /interface      # The Face (CLI/GUI)
│   └── interface.py
├── /tests          # Verification Scripts
└── app_cli_mode.py # Entry Point
```

## 🛠️ Getting Started

### Prerequisites
- Python 3.x

### Installation
1. Clone the repository.
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate
   ```
3. Install dependencies (currently none required for the core CLI).

### Usage
Run the main application:
```bash
python app_cli_mode.py
```

### Testing
Run the verification scripts to check the modules:
```bash
python -m tests.test_quiz
python -m tests.test_tracker
python -m tests.test_assets
```

