from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


class StaiInstructionWindow(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        # Główny layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#2E2E2E"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # STAI Instructions
        instructions = QLabel()
        instructions.setTextFormat(Qt.TextFormat.RichText)  # Enable RichText formatting
        instructions.setText(
            "<b>STAI Instructions</b><br><br>"
            "Please answer the questions in the STAI form.<br><br>"
            "You will be asked to respond to 20 questions about how you feel.<br><br>"
            "Answer all questions using a scale from 1 to 4:<br>"
            "1 - Not at all<br>"
            "2 - A little<br>"
            "3 - Moderately<br>"
            "4 - Very much<br><br>"
            "<b>Press any key to continue.</b>"
        )
        instructions.setStyleSheet("color: white; font-size: 18px; padding: 20px;")
        instructions.setAlignment(Qt.AlignCenter)

        # Dodanie instrukcji do layoutu
        self.layout.addWidget(instructions)
        self.setLayout(self.layout)

    def keyPressEvent(self, event):
        """Przechodzenie do widoku STAI po naciśnięciu dowolnego klawisza."""
        self.main_app.show_stai()
