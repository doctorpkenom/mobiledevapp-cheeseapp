import { useState, useCallback } from 'react';
import QUESTIONS from '../data/questions.json';
import CHEESES from '../data/cheeses.json';

/**
 * Custom hook to manage the Cheese Quiz logic.
 * Handles state interactions, scoring, and result calculation.
 * 
 * @typedef {Object} GameState
 * @property {'WELCOME' | 'QUIZ' | 'RESULT'} screen - Current game screen
 * @property {number} score - Current accumulated score
 * @property {number} questionIndex - Index of the current question
 * @property {Array} sessionQuestions - List of questions for this session
 * @property {Object|null} result - Final cheese result object
 * 
 * @returns {{
 *   gameState: GameState,
 *   startNewGame: () => void,
 *   submitAnswer: (value: number|string) => void
 * }}
 */
export const useQuizEngine = () => {
    const [gameState, setGameState] = useState({
        screen: 'WELCOME', // WELCOME, QUIZ, RESULT
        score: 0,
        questionIndex: 0,
        sessionQuestions: [],
        result: null
    });

    const startNewGame = useCallback(() => {
        // 1. Pick 10 random questions
        const shuffled = [...QUESTIONS].sort(() => 0.5 - Math.random());
        const selected = shuffled.slice(0, 10);

        // 2. Add Mandatory Lactose Question
        const lactoseQuestion = {
            id: 999,
            type: "choice",
            text: "Final Question: Are you lactose intolerant?",
            options: [
                { label: "Yes, sadly.", value: "LACTOSE_YES" },
                { label: "No, I am strong.", value: 0 }
            ]
        };
        selected.push(lactoseQuestion);

        setGameState({
            screen: 'QUIZ',
            score: 0,
            questionIndex: 0,
            sessionQuestions: selected,
            result: null
        });
    }, []);

    const submitAnswer = useCallback((value) => {
        setGameState(prev => {
            let newScore = prev.score;

            // Handle Lactose Override
            if (value === "LACTOSE_YES") {
                newScore = -100;
            } else if (typeof value === 'number') {
                // Only add if not already overridden (though -100 is end game)
                if (newScore !== -100) {
                    newScore += value;
                }
            }

            const nextIndex = prev.questionIndex + 1;

            // Check if finished
            if (nextIndex >= prev.sessionQuestions.length) {
                const finalResult = calculateResult(newScore);
                return { ...prev, score: newScore, questionIndex: nextIndex, screen: 'RESULT', result: finalResult };
            }

            return { ...prev, score: newScore, questionIndex: nextIndex };
        });
    }, []);

    const calculateResult = (finalScore) => {
        // 1. Lactose Intolerant Case
        if (finalScore === -100) {
            return CHEESES.find(c => c.score === -100) || CHEESES[0];
        }

        // 2. Exact Match
        const exact = CHEESES.find(c => c.score === finalScore);
        if (exact) return exact;

        // 3. Find Ties / Closest
        // Sort cheeses by score
        const sorted = [...CHEESES].sort((a, b) => a.score - b.score);

        let lower = null;
        let upper = null;

        for (const cheese of sorted) {
            if (cheese.score < finalScore) lower = cheese;
            else if (cheese.score > finalScore) {
                upper = cheese;
                break;
            }
        }

        // Coin Flip logic for ties/between
        if (lower && upper) {
            return Math.random() < 0.5 ? lower : upper;
        }

        return lower || upper || CHEESES[0]; // Fallback
    };

    return {
        gameState,
        startNewGame,
        submitAnswer
    };
};
