import { motion } from 'framer-motion';

const MultipleChoice = ({ question, onAnswer }) => {
    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {question.options.map((opt, i) => (
                <motion.button
                    key={i}
                    className="fun-border"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: i * 0.1 }}
                    whileHover={{ scale: 1.02, backgroundColor: 'var(--bg-color)' }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => onAnswer(opt.value)}
                    style={{
                        padding: '1rem',
                        background: 'var(--bg-color)', // Cream bg for buttons
                        fontSize: '1.1rem',
                        textAlign: 'left',
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center'
                    }}
                >
                    {opt.label}
                </motion.button>
            ))}
        </div>
    );
};

export default MultipleChoice;
