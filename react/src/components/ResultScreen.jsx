import { motion } from 'framer-motion';

/**
 * Result Screen Component.
 * Displays the final "Cheese Persona" with a dynamic image and description.
 * 
 * @param {Object} props
 * @param {Object} props.result - The final result object (name, description, image path)
 * @param {Function} props.onRestart - Callback to restart the game
 */
const ResultScreen = ({ result, onRestart }) => {
    // Construct image path
    // cheeses.json usually provides "cheeses/filename.png"
    // our assets are in /assets/cheeses/filename.png
    // so we prepend /assets/ if not present
    const imgPath = result?.image ? `/assets/${result.image}` : null;

    return (
        <div className="card fun-border" style={{ padding: '1rem', maxWidth: '500px' }}>
            <motion.h3
                initial={{ y: -20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                style={{ fontFamily: 'var(--font-title)', color: 'var(--text-color)', marginBottom: '0.5rem' }}
            >
                THE UNIVERSE SAYS...
            </motion.h3>

            {/* Polaroid Image */}
            {imgPath && (
                <motion.div
                    initial={{ scale: 0.8, rotate: -5, opacity: 0 }}
                    animate={{ scale: 1, rotate: Math.random() * 6 - 3, opacity: 1 }}
                    transition={{ delay: 0.2, type: 'spring' }}
                    style={{
                        background: 'white',
                        padding: '0.5rem 0.5rem 2rem 0.5rem',
                        boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
                        display: 'inline-block',
                        marginBottom: '1rem',
                        border: '1px solid #ddd'
                    }}
                >
                    <img
                        src={imgPath}
                        alt={result.name}
                        style={{ width: '100%', maxWidth: '250px', display: 'block' }}
                    />
                </motion.div>
            )}

            <motion.h1
                initial={{ scale: 0.5, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ delay: 0.4 }}
                style={{
                    fontFamily: 'var(--font-title)',
                    color: 'var(--accent-dark)',
                    fontSize: '1.8rem',
                    lineHeight: '1.1',
                    textTransform: 'uppercase',
                    marginBottom: '1rem'
                }}
            >
                {result?.name}
            </motion.h1>

            <motion.div
                className="fun-border"
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.6 }}
                style={{
                    background: 'var(--bg-color)',
                    padding: '1rem',
                    marginBottom: '1.5rem',
                    fontSize: '1rem'
                }}
            >
                {result?.description}
            </motion.div>

            <motion.button
                className="btn-primary fun-border"
                onClick={onRestart}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
            >
                ROAST ME AGAIN 🧀
            </motion.button>
        </div>
    );
};

export default ResultScreen;
