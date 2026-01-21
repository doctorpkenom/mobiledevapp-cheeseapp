# React Components Documentation 🧩

This directory contains the Reusable UI components for the Cheese Personality Test.

## Core Screens

### 1. `WelcomeScreen.jsx`
The entry point of the application. Displays the title, logo, and a "Start Quiz" button.

**Props:**
- `onStart` (function): Callback triggered when the user clicks the start button.

**Usage:**
```jsx
<WelcomeScreen onStart={() => setGameState('QUIZ')} />
```

### 2. `QuizScreen.jsx`
Displays the current question and handles user input. It dynamically renders either a `SliderQuestion` or `MultipleChoice` component based on the question type.

**Props:**
- `question` (object): The current question object (from `questions.json`).
- `onAnswer` (function): Callback with the answer value.

**Usage:**
```jsx
<QuizScreen 
    question={currentQuestion} 
    onAnswer={(val) => handleAnswer(val)} 
/>
```

### 3. `ResultScreen.jsx`
Displays the final result cheese, description, and image.

**Props:**
- `result` (object): The final cheese object (from `cheeses.json`).
- `onRestart` (function): Callback to reset the game.

**Usage:**
```jsx
<ResultScreen 
    result={finalResult} 
    onRestart={resetGame} 
/>
```

## UI Components

### `SliderQuestion.jsx`
A range slider input for "scale" type questions (0-10).

**Props:**
- `label` (string): The question text.
- `minLabel` (string): Label for 0.
- `maxLabel` (string): Label for 10.
- `onAnswer` (function): Callback when the user confirms their choice.

### `MultipleChoice.jsx`
A set of buttons for "choice" type questions.

**Props:**
- `label` (string): The question text.
- `options` (array): List of `{label, value}` objects.
- `onAnswer` (function): Callback with selected option's value.
