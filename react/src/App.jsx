import { useState, useEffect } from 'react'
import { useQuizEngine } from './hooks/useQuizEngine'
import { motion, AnimatePresence } from 'framer-motion'
import './App.css'

// Screens (We'll define these next)
import WelcomeScreen from './components/WelcomeScreen'
import QuizScreen from './components/QuizScreen'
import ResultScreen from './components/ResultScreen'

/**
 * Main Application Component.
 * Routes between Welcome, Quiz, and Result screens based on game state.
 * Uses Framer Motion for page transitions.
 */
function App() {
  const { gameState, startNewGame, submitAnswer } = useQuizEngine();

  // Simple Screen Router
  const renderScreen = () => {
    switch (gameState.screen) {
      case 'WELCOME':
        return <WelcomeScreen onStart={startNewGame} />;
      case 'QUIZ':
        return (
          <QuizScreen
            question={gameState.sessionQuestions[gameState.questionIndex]}
            totalQuestions={gameState.sessionQuestions.length}
            currentNumber={gameState.questionIndex + 1}
            onAnswer={submitAnswer}
          />
        );
      case 'RESULT':
        return <ResultScreen result={gameState.result} onRestart={startNewGame} />;
      default:
        return <WelcomeScreen onStart={startNewGame} />;
    }
  };

  return (
    <div className="app-container">
      <AnimatePresence mode="wait">
        <motion.div
          key={gameState.screen}
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 1.05 }}
          transition={{ duration: 0.3 }}
          style={{ width: '100%', height: '100%', display: 'flex', justifyContent: 'center' }}
        >
          {renderScreen()}
        </motion.div>
      </AnimatePresence>
    </div>
  )
}

export default App
