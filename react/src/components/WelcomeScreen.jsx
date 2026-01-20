import { motion } from 'framer-motion';

/**
 * Welcome Screen Component.
 * Displays the title animation, introductory text, and floating cheese particles.
 * 
 * @param {Object} props
 * @param {Function} props.onStart - Callback to start the game
 */
const WelcomeScreen = ({ onStart }) => {
    return (
        <div style={{
            textAlign: 'center',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            height: '100%'
        }}>
            <motion.h1
                initial={{ y: -50, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ type: "spring", stiffness: 100 }}
                style={{
                    fontFamily: 'var(--font-title)',
                    fontSize: '3.5rem',
                    marginBottom: '1rem',
                    color: 'var(--text-color)'
                }}
            >
                WHAT CHEESE<br />ARE YOU?
            </motion.h1>

            <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.3 }}
                style={{ fontSize: '1.2rem', marginBottom: '3rem', maxWidth: '400px' }}
            >
                Discover your inner dairy destiny! Are you a mild Ricotta or a biohazard Vieux-Boulogne?
            </motion.p>

            <motion.button
                className="btn-primary fun-border"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={onStart}
            >
                LET'S GO! 🧀
            </motion.button>

            {/* Basic Particles */}
            {[...Array(5)].map((_, i) => (
                <motion.div
                    key={i}
                    animate={{
                        y: [0, -20, 0],
                        rotate: [0, 10, -10, 0]
                    }}
                    transition={{
                        duration: 3 + i,
                        repeat: Infinity,
                        ease: "easeInOut"
                    }}
                    style={{
                        position: 'absolute',
                        fontSize: '2rem',
                        left: `${20 + i * 15}%`,
                        top: `${20 + (i % 2) * 40}%`,
                        opacity: 0.6,
                        zIndex: -1
                    }}
                >
                    🧀
                </motion.div>
            ))}
        </div>
    );
};

export default WelcomeScreen;
