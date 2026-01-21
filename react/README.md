# Cheese App - React Implementation ⚛️

This is the main web application for the Cheese Personality Test. It is built with **React** and **Vite**.

## 📂 Structure

- `src/components/`: UI Components (Screens, Buttons, Sliders). [Read More](./src/components/README.md)
- `src/hooks/`: Game Logic (`useQuizEngine`). [Read More](./src/hooks/README.md)
- `src/data/`: Static JSON assets (Questions, Results). [Read More](./src/data/README.md)
- `src/assets/`: Images and global styles.

## 🚀 Getting Started

### 1. Install Dependencies
Run this in the `react` folder:
```bash
npm install
```

### 2. Run Development Server
Start the local server:
```bash
npm run dev
```
Open the link (e.g., `http://localhost:5173`) in your browser.

### 3. Build for Production
Create a static build:
```bash
npm run build
```
The output will be in `dist/`.

## 🛠️ Architecture
The app runs entirely client-side. It loads data from JSON files and uses `framer-motion` for smooth screen transitions. The logic mirrors the Python reference implementation exactly, including the "Coin Flip" tie-breaking mechanism.
