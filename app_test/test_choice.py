from main import CheeseApp

Q_DATA = {
    'text': "How do you handle conflict?",
    'type': 'choice',
    'options': [
        {'label': "I melt immediately.", 'value': 0},
        {'label': "I get hard and salty.", 'value': 10},
        {'label': "I stink up the room.", 'value': 20},
        {'label': "I crumble under pressure.", 'value': 5}
    ]
}

if __name__ == "__main__":
    app = CheeseApp(start_screen="QUIZ", test_data={'q': Q_DATA})
    app.mainloop()
