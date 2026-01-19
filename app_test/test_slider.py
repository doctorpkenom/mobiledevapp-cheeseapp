from main import CheeseApp

Q_DATA = {
    'text': "How much do you love dairy?",
    'type': 'scale',
    'min_label': "I'm lactose intolerant but I try anyway because I have no self preservation.",
    'max_label': "Liquid cheese flows through my veins."
}

if __name__ == "__main__":
    app = CheeseApp(start_screen="QUIZ", test_data={'q': Q_DATA})
    app.mainloop()
