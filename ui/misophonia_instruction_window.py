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
            "<b>Press any key to proceed to the questionnaire.</b>"
            "</p>"
        )
        instructions_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(instructions_label)

        self.setLayout(main_layout)

    def keyPressEvent(self, event):
        """Przechodzenie do widoku STAI po naciśnięciu dowolnego klawisza."""
        self.main_app.show_misophonia()
