# Cheese Personality Test 🧀

A playful, nostalgic, and slightly chaotic personality test app. Answer questions, get judged by dairy products, and find out if you are a "Reliable Cheddar" or a "Certified Biohazard Vieux-Boulogne".

## 🚀 Features
- **30+ Questions**: Ranging from deep philosophical inquiries to laundry habits.
- **Coin Flip Scoring**: If you fall between two cheese personalities, a coin flip decides your fate.
- **Lactose Intolerance Mode**: A secret ending for the weak of stomach.
- **Web Interface**: Modern React-based UI with smooth animations.

## 📂 Project Structure

This project is divided into two main parts:

### 1. `react/` (The Application)
The active web application.
- **Core Logic:** `src/hooks/useQuizEngine.js`
- **UI:** `src/components/`
- [Read Frontend Documentation](./react/README.md)

### 2. `quiz/` (The Reference)
The original Python reference implementation of the logic.
- **Engine:** `quiz_engine.py`
- **Data:** `questions.json`, `cheeses.json`
- [Read Backend Documentation](./quiz/README.md)

## 🏃 Quick Start Walkthrough

Follow these steps to run the application on your computer.

### Step 1: Prerequisites
Make sure you have **Node.js** installed.
- Check by running: `node -v` in your terminal.
- If not installed, download it from [nodejs.org](https://nodejs.org/).

### Step 2: Setup
1. Open your terminal.
2. Navigate to the `react` folder:
   ```bash
   cd react
   ```
3. Install the dependencies:
   ```bash
   npm install
   ```

### Step 3: Run the App
Start the development server:
```bash
npm run dev
```
You will see a link like `http://localhost:5173`. **Ctrl + Click** it (or copy-paste it into your browser) to start the test!

### Optional: Python Reference
If you want to look at the python logic:
```bash
# From the root folder
python -m quiz.quiz_engine
```
*(Note: The main interface is now the web app)*
