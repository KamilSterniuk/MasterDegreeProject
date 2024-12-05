from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPalette, QColor


class IntroWindow(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        # Ustawienie ciemnego tła
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#2E2E2E"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Główny layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Usuń marginesy wokół layoutu
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)  # Wyśrodkowanie wszystkiego

        # Nagłówek
        header_label = QLabel("Welcome to the ASMR Video Evaluation")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("color: white; font-weight: bold;")
        header_label.setFont(QFont("Arial", 22))
        layout.addWidget(header_label)

        # Treść instrukcji z użyciem HTML
        instructions = """
        <p style='font-size: 18px; color: #BBBBBB; text-align: center;'>
        <b>ASMR</b> (Autonomous Sensory Meridian Response) is a relaxing, tingling sensation<br>
        often triggered by specific sounds, visuals, or personal attention stimuli.<br><br>
        In this task, you will be presented with <b>7 short ASMR videos</b>. Your goal is to evaluate each<br>
        video based on your personal preference. Please consider the following:<br>
        <ul style='text-align: left;'>
            <li>Visual and auditory quality.</li>
            <li>How much you enjoyed the video.</li>
        </ul>
        <br>
        Use the rating scale from <b>0</b> to <b>10</b>:<br>
        <b>0:</b> Strongly disliked<br>
        <b>5:</b> Neutral<br>
        <b>10:</b> Highly preferred<br><br>
        After rating all videos, you will proceed to the next phase of the experiment.<br><br>
        <b>Press any key to continue.</b>
        </p>
        """
        instruction_label = QLabel()
        instruction_label.setTextFormat(Qt.TextFormat.RichText)  # Włączenie obsługi HTML
        instruction_label.setText(instructions)
        instruction_label.setAlignment(Qt.AlignCenter)
        instruction_label.setStyleSheet("color: white;")
        layout.addWidget(instruction_label)

        # Ustawienie layoutu
        self.setLayout(layout)

    def keyPressEvent(self, event):
        """Obsługa naciśnięcia klawisza."""
        self.main_app.show_asmr_select_window()
        self.close()
