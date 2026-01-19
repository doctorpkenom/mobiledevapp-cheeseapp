# Cheese App v2: Cute & Cartoony (Test Branch)

**Goal**: Build a robust, fun, and visually cohesive quiz app from scratch in `test/`.
**Constraint**: Reuse ONLY cheese images (result). Draw everything else programmatically or use simple generated patterns.

## Concept: "The Cheese Card Stack"
A playful, bright interface where questions are "cards" stacked on a playful background.

### Visual Style
- **Colors**: Butter Yellow, Cheddar Orange, Cream White, Dark Brown (Outlines).
- **Shapes**: Rounded rectangles, thick borders (comic style).
- **Font**: Comic Sans MS (if available) or Arial Bold.

### Architecture
- `test/main.py`: Single file containing App, Renderer, and Engine logic (for simplicity and robustness).
- `test/assets/`: Directory for the reused cheese images.

## Steps
1.  **Setup**: Create `test/assets` and copy cheese images from `assets/`.
2.  **Logic**: Copy/Adapter for `quiz/questions.json` loading.
3.  **UI Engine (`CheeseGUI`)**:
    - `draw_rounded_rect`: Custom canvas drawing with borders.
    - `draw_button`: Interactive "squishy" buttons.
4.  **Scenes**:
    - **Home**: Bouncing Title ("WHAT CHEESE ARE YOU?").
    - **Quiz**: Progress bar (cheese wedge filling up?). Question Card.
    - **Result**: "You are..." + Image + Description.

## Animation
- Simple "Squash and Stretch" on button clicks.
- Cards slide in from right.
