from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout
from ui.ant_instructions.first_view import FirstView
from ui.ant_instructions.second_view import SecondView
from ui.ant_instructions.third_view import ThirdView
from ui.ant_instructions.fourth_view import FourthView
from ui.ant_instructions.fifth_view import FifthView

class AntInstructionWindow(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.stack = QStackedWidget(self)

        # Widoki instrukcji
        self.first_view = FirstView(self.show_second_view)
        self.second_view = SecondView(self.show_third_view)
        self.third_view = ThirdView(self.show_fourth_view)
        self.fourth_view = FourthView(self.show_fifth_view)
        self.fifth_view = FifthView(self.start_trial_ant_test)

        # Dodanie widoków do stosu
        self.stack.addWidget(self.first_view)
        self.stack.addWidget(self.second_view)
        self.stack.addWidget(self.third_view)
        self.stack.addWidget(self.fourth_view)
        self.stack.addWidget(self.fifth_view)

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.stack)
        self.setLayout(layout)

    def show_first_view(self):
        self.stack.setCurrentWidget(self.first_view)

    def show_second_view(self):
        self.stack.setCurrentWidget(self.second_view)

    def show_third_view(self):
        self.stack.setCurrentWidget(self.third_view)

    def show_fourth_view(self):
        self.stack.setCurrentWidget(self.fourth_view)

    def show_fifth_view(self):
        self.stack.setCurrentWidget(self.fifth_view)

    def start_trial_ant_test(self):
        """Przełącza na ekran 'Trial in Progress' i uruchamia test w osobnym wątku."""
        print("Delegating to MainApp to start trial ANT test...")
        self.main_app.show_trial_in_progress()  # Przełącza widok na 'Trial in Progress'

        # Uruchomienie testu próbnego w osobnym wątku
        import threading
        threading.Thread(target=self.run_trial_ant).start()

    def run_trial_ant(self):
        """Uruchamia test próbny, a następnie główny test."""
        from ant_test import trial_ant_test
        try:
            trial_ant_test()  # Uruchomienie testu próbnego
        except Exception as e:
            print(f"Error during ANT tests: {e}")
        self.main_app.trial_in_progress_view.show_completion_message()

