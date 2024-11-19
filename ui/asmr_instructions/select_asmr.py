from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPalette, QColor


class IntroWindow(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#2E2E2E"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Główny układ
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Usuń marginesy wokół layoutu
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)  # Wyśrodkowanie wszystkiego

        # Nagłówek
        header_label = QLabel("Welcome to the ASMR Video Evaluation")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("color: white; font-weight: bold;")
        header_label.setFont(QFont("Arial", 18))
        layout.addWidget(header_label)

        # Treść instrukcji z ręcznie dodanymi podziałami linii
        instructions = """ASMR (Autonomous Sensory Meridian Response) refers to a relaxing, tingling sensation<br>
        that typically begins on the scalp and moves down the neck and spine. It is often triggered<br>
        by specific sounds, visuals, or personal attention stimuli.<br><br>
        You will now be presented with 7 ASMR videos. Please rate each video subjectively on a scale<br>
        from 0 to 10 based on your personal preference, considering visual appeal or its overall effect.<br><br>
        Ratings are defined as follows:<br>
        0 - Strongly disliked<br>
        5 - Neutral<br>
        10 - Highly preferred<br><br>
        <b>Press any key to continue.</b>"""  # Użycie znaczników HTML

        instruction_label = QLabel()
        instruction_label.setTextFormat(Qt.TextFormat.RichText)  # Informuje QLabel, że ma renderować HTML
        instruction_label.setText(instructions)
        instruction_label.setAlignment(Qt.AlignCenter)
        instruction_label.setStyleSheet("color: white; font-size: 18px;")
        layout.addWidget(instruction_label)

        # Ustawienie layoutu
        self.setLayout(layout)

    def keyPressEvent(self, event):
        """Obsługa naciśnięcia klawisza."""
        self.main_app.show_asmr_select_window()
        self.close()
