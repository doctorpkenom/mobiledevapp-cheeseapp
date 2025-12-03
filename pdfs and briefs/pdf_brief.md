# Cheese Personality Test - Project Brief

## 1. Project Overview
The **Cheese Personality Test** is a Python-based application that determines a user's "Cheese Persona" based on a series of quirky, mixed-format questions. The project is modular, separating logic, data, and interface to allow for future expansion (e.g., GUI, Web, Mobile).

## 2. Module Documentation
For detailed technical documentation on each module, please refer to the following files in the repository:

*   **Quiz Logic & Data**: [`quiz/quiz_readme.md`](quiz/quiz_readme.md) - Explains the scoring engine, question formats, and cheese data.
*   **Tracker (History)**: [`tracker/tracker_readme.md`](tracker/tracker_readme.md) - Details how user results are persisted.
*   **Assets**: [`assets/assets_readme.md`](assets/assets_readme.md) - Covers image and resource management.
*   **Interface (CLI)**: [`interface_cli/interface_cli_readme.md`](interface_cli/interface_cli_readme.md) - Describes the current command-line interface structure.
*   **Tests**: [`tests/tests_readme.md`](tests/tests_readme.md) - Outlines the verification scripts.

## 3. Current Interface (CLI Version)
The current application runs in a terminal/command prompt environment (`interface_cli`).

**User Flow:**
1.  **Main Menu**: Users are presented with options to Start Quiz, View History, or Exit.
2.  **Quiz Session**:
    *   **Questions**: Presented sequentially.
    *   **Input**: Users type numbers (1-4) for multiple choice or (0-10) for sliders.
    *   **Lactose Check**: A final mandatory question checks for lactose intolerance.
3.  **Results Screen**: Displays the calculated Cheese Persona and its description.
4.  **History View**: Shows a list of past results with timestamps.

## 4. Planned UI/UX
The roadmap includes moving from the CLI to a rich Graphical User Interface (GUI).

> **Note**: Detailed designs, wireframes, and specifications for the planned screens are located in the **UI/UX Document** (available in this GitHub repository).

This future document outlines:
*   Visual design language (colors, typography).
*   Screen layouts (Welcome, Question, Result).
*   Asset usage (images from the `assets/` folder).
