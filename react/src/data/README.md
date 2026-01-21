# Data Documentation 💽

This folder contains the static JSON data used by the application.

## 1. `questions.json`

A list of all possible questions.

**Schema:**
```json
{
    "id": number,
    "type": "scale" | "choice",
    "text": "Question string",
    
    // For "scale" type:
    "min_label": "Label for left side",
    "max_label": "Label for right side",

    // For "choice" type:
    "options": [
        { "label": "Button Text", "value": number }
    ]
}
```

## 2. `cheeses.json`

A list of all possible cheese results.

**Schema:**
```json
{
    "name": "Cheese Name",
    "score": number, // The target score for this personality (-100 to 100+)
    "description": "Personality description",
    "image": "filename.jpg" // Located in /assets/cheeses/
}
```
