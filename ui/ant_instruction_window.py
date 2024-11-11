from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt

class AntInstructionWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Tytuł okna
        self.setWindowTitle("Attention Concentration Test with EEG and Eye-Tracking")
        self.setStyleSheet("background-color: #2E2E2E;")  # Ciemnoszare tło

        # Etykieta z instrukcją
        instruction_label = QLabel(
            "Thank you for watching the video.\n"
            "You will soon perform a task to check your concentration.\n\n"
            "Press any key to continue."
        )
        instruction_label.setAlignment(Qt.AlignCenter)
        instruction_label.setStyleSheet("font-size: 20px; font-weight: bold; color: white; padding: 20px;")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(instruction_label)
        self.setLayout(layout)
