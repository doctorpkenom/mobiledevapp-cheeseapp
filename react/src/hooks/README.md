# Custom Hooks Documentation 🪝

This folder contains the game logic encapsulated in React hooks.

## `useQuizEngine.js`

This hook is the "brain" of the frontend application. It manages the entire game state, rules, and navigation.

**State Structure:**
```js
const [gameState, setGameState] = useState({
    screen: 'WELCOME', // Current view: WELCOME | QUIZ | RESULT
    score: 0,          // Running score total
    questionIndex: 0,  // Current question number (0-indexed)
    sessionQuestions: [], // The randomized list of 10 questions + 1 final
    result: null       // The final cheese object
});
```

**Key Functions:**

### `startNewGame()`
- Resets score and index.
- Randomly selects 10 questions from `questions.json`.
- Appends the **Mandatory Lactose Question** at the end.
- Transitions screen to `QUIZ`.

### `submitAnswer(value)`
- Updates the score.
- **Lactose Override Rule:** If `value === "LACTOSE_YES"`, score becomes `-100`.
- Increments `questionIndex`.
- Checks if game is over -> Calculates Result -> Transitions to `RESULT`.

### `calculateResult(finalScore)`
1. **Lactose Check:** If score is -100, returns the Lactose Intolerant result.
2. **Exact Match:** Looks for a cheese with exactly `finalScore`.
3. **Coin Flip Strategy:** If between two cheeses (e.g., score 65, cheeses at 60 and 70), performs a 50/50 random choice between the two neighbors.

**Usage:**
```jsx
const { gameState, startNewGame, submitAnswer } = useQuizEngine();
```
