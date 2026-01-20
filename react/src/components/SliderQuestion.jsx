import { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';

/**
 * Slider Question Component.
 * Renders a specialized range input with a custom "Cheese Wheel" thumb.
 * 
 * @param {Object} props
 * @param {Object} props.question - Question data (min_label, max_label)
 * @param {Function} props.onAnswer - Callback with the slider value
 */
const SliderQuestion = ({ question, onAnswer }) => {
    const [value, setValue] = useState(5); // 0-10 scale

    return (
        <div style={{ padding: '0 1rem', display: 'flex', flexDirection: 'column', gap: '2rem' }}>

            {/* Labels */}
            <div style={{ display: 'flex', justifyContent: 'space-between', fontFamily: 'var(--font-title)', fontSize: '0.9rem', color: 'var(--text-color)' }}>
                <span style={{ width: '40%', textAlign: 'left' }}>{question.min_label || 'No'}</span>
                <span style={{ width: '40%', textAlign: 'right' }}>{question.max_label || 'Yes'}</span>
            </div>

            {/* Styled Range Input */}
            <div style={{ position: 'relative', height: '40px', display: 'flex', alignItems: 'center' }}>
                <input
                    type="range"
                    min="0"
                    max="10"
                    step="1"
                    value={value}
                    onChange={(e) => setValue(parseInt(e.target.value))}
                    style={{
                        width: '100%',
                        height: '12px',
                        borderRadius: '6px',
                        background: 'var(--border-color)',
                        outline: 'none',
                        appearance: 'none',
                        border: '2px solid white',
                        cursor: 'pointer'
                    }}
                />
                {/* Custom Thumb Style Injection (since inline styles can't target pseudo-elements easily) */}
                <style>{`
          input[type=range]::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 50px;
            height: 50px;
            background-image: url('/assets/slider_knob_cheese.png');
            background-size: cover;
            border: none;
            cursor: grab;
            transition: transform 0.1s;
          }
          input[type=range]::-webkit-slider-thumb:active {
            transform: scale(1.1);
            cursor: grabbing;
          }
        `}</style>
            </div>

            <motion.button
                className="btn-primary fun-border"
                onClick={() => onAnswer(value)}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                style={{ alignSelf: 'center', marginTop: '1rem', fontSize: '1.2rem' }}
            >
                LOCK IT IN! 🔒
            </motion.button>
        </div>
    );
};

export default SliderQuestion;
