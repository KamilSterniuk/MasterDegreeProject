import sys
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt


class MisophoniaInstructionsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Misophonia Activation Scale - Instructions")
        self.showFullScreen()  # Tryb pełnoekranowy

        # Ustawienie ciemnego tła
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#2E2E2E"))  # Ciemnoszare tło
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Główny layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # Tytuł
        title_label = QLabel("Instructions for the Misophonia Activation Scale")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: white; padding: 20px;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Instrukcja
        instructions_label = QLabel()
        instructions_label.setTextFormat(Qt.TextFormat.RichText)  # Użycie HTML dla formatowania
        instructions_label.setText(
            "<p style='font-size: 20px; color: #BBBBBB; text-align: center;'>"
            "The <b>Misophonia Activation Scale</b> is designed to assess your emotional and physical responses "
            "to trigger sounds commonly associated with misophonia. You will be asked to respond to two parts:<br><br>"
            "<b>Part A: Emotional Response</b><br>"
            "Evaluate the intensity of your emotional reactions to specific sounds.<br><br>"
            "<b>Part B: Physical Sensation</b><br>"
            "Rate the physical sensations you experience in response to these sounds, "
            "ranging from no sensation to severe pain.<br><br>"
            "For each question, select a score from <b>0</b> to <b>10</b>, where:"
            "<ul style='text-align: left;'>"
            "<li><b>0:</b> No discomfort or sensation.</li>"
            "<li><b>5:</b> Moderate discomfort or noticeable physical sensations.</li>"
            "<li><b>10:</b> Extreme emotional or physical reactions, including pain.</li>"
            "</ul>"
            "Please answer all questions honestly based on your current or recent experiences.<br><br>"
            "<b>Press the button below to proceed to the questionnaire.</b>"
            "</p>"
        )
        instructions_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(instructions_label)

        # Przycisk kontynuacji
        continue_button = QPushButton("Continue to Questionnaire")
        continue_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 18px;
                padding: 15px 30px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        continue_button.clicked.connect(self.close)  # Zamknięcie okna
        main_layout.addWidget(continue_button)

        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MisophoniaInstructionsWindow()
    window.show()
    sys.exit(app.exec())
