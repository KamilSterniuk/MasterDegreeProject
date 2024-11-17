from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout
from ui.ant_instructions.first_view import FirstView
from ui.ant_instructions.second_view import SecondView
from ui.ant_instructions.third_view import ThirdView
from ui.ant_instructions.fourth_view import FourthView

class AntInstructionWindow(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app  # Referencja do MainApp
        self.stack = QStackedWidget(self)  # Stos widoków instrukcji

        # Inicjalizacja widoków
        self.first_view = FirstView(self.show_second_view)
        self.second_view = SecondView(self.show_third_view)
        self.third_view = ThirdView(self.show_fourth_view)
        self.fourth_view = FourthView(self.main_app.show_main)

        # Dodanie widoków do stosu
        self.stack.addWidget(self.first_view)
        self.stack.addWidget(self.second_view)
        self.stack.addWidget(self.third_view)
        self.stack.addWidget(self.fourth_view)

        # Layout dla AntInstructionWindow
        layout = QVBoxLayout(self)
        layout.addWidget(self.stack)
        self.setLayout(layout)

    def show_first_view(self):
        print("Switching to FirstView")  # Debug
        self.stack.setCurrentWidget(self.first_view)

    def show_second_view(self):
        print("Switching to SecondView")  # Debug
        self.stack.setCurrentWidget(self.second_view)

    def show_third_view(self):
        print("Switching to ThirdView")  # Debug
        self.stack.setCurrentWidget(self.third_view)

    def show_fourth_view(self):
        print("Switching to FourthView")  # Debug
        self.stack.setCurrentWidget(self.fourth_view)
