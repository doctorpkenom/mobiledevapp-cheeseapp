import { motion } from 'framer-motion';
import MultipleChoice from './MultipleChoice';
import SliderQuestion from './SliderQuestion';

/**
 * Quiz Screen Component.
 * Orchestrates the display of questions and the progress bar.
 * Dynamically renders either MultipleChoice or SliderQuestion based on type.
 * 
 * @param {Object} props
 * @param {Object} props.question - Current question object
 * @param {number} props.totalQuestions - Total count of questions
 * @param {number} props.currentNumber - Current question number (1-indexed)
 * @param {Function} props.onAnswer - Callback when answer is submitted
 */
const QuizScreen = ({ question, totalQuestions, currentNumber, onAnswer }) => {
    return (
        <div className="card fun-border">
            {/* Progress Bar */}
            <div style={{
                position: 'absolute',
                top: '-20px',
                left: '50%',
                transform: 'translateX(-50%)',
                background: 'var(--accent-color)',
                padding: '0.5rem 1.5rem',
                borderRadius: '20px',
                border: '2px solid var(--border-color)',
                fontWeight: 'bold'
            }}>
                Question {currentNumber} / {totalQuestions}
            </div>

            <motion.h2
                key={question.text}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                style={{ fontFamily: 'var(--font-title)', marginTop: '2rem', marginBottom: '2rem' }}
            >
                {question.text}
            </motion.h2>

            {question.type === 'scale' ? (
                <SliderQuestion question={question} onAnswer={onAnswer} />
            ) : (
                <MultipleChoice question={question} onAnswer={onAnswer} />
            )}
        </div>
    );
};

export default QuizScreen;
