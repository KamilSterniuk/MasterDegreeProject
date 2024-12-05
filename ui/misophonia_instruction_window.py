from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


class MisophoniaInstructionWindow(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        # Ustawienie ciemnego tła
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#2E2E2E"))  # Ciemnoszare tło
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Główny layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # Tytuł
        title_label = QLabel("Instructions for the Misophonia Questionnaire")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: white; padding: 20px;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Instrukcja
        instructions_label = QLabel()
        instructions_label.setTextFormat(Qt.TextFormat.RichText)  # Użycie HTML dla formatowania
        instructions_label.setText(
            "<p style='font-size: 20px; color: #BBBBBB; text-align: center;'>"
            "The <b>Misophonia Questionnaire</b> is designed to assess your emotional and physical responses "
            "to common trigger sounds. You will be presented with a series of questions about your experiences.<br><br>"
            "For each question, use the slider to rate your reaction on a scale from <b>0</b> to <b>10</b>, where:"
            "<ul style='text-align: left;'>"
            "<li><b>0:</b> No reaction or discomfort.</li>"
            "<li><b>5:</b> Moderate reaction or discomfort.</li>"
            "<li><b>10:</b> Extreme reaction or discomfort, including physical symptoms.</li>"
            "</ul>"
            "Please answer all questions as honestly as possible, based on your current or recent experiences.<br><br>"
            "<b>Press any key to proceed to the questionnaire.</b>"
            "</p>"
        )
        instructions_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(instructions_label)

        self.setLayout(main_layout)

    def keyPressEvent(self, event):
        """Przechodzenie do widoku Misophonia po naciśnięciu dowolnego klawisza."""
        self.main_app.show_misophonia()

