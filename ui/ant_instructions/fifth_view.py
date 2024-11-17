from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSpacerItem, QSizePolicy
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt
import threading

class FifthView(QWidget):
    def __init__(self, start_trial_callback):
        super().__init__()
        self.start_trial_callback = start_trial_callback  # Referencja do funkcji `start_trial_ant_test`

        # Ustawienie tła
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#C0C0C0"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        layout = QVBoxLayout(self)

        # Spacer na górze
        layout.addSpacerItem(QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Główna instrukcja
        instruction_text = QLabel(
            "<h1 style='text-align: center;'>Get Ready</h1>"
            "<p style='font-size: 18px; text-align: center;'>You are now about to perform a trial ANT test<br>"
            "to get familiar with the task.</p>"
            "<p style='font-size: 16px; text-align: center;'>Please pay attention and follow the instructions<br>"
            "as this will help you prepare for the actual test.</p>"
        )
        instruction_text.setAlignment(Qt.AlignCenter)
        layout.addWidget(instruction_text)

        # Tekst kontynuacji
        continue_text = QLabel("<b>Press any key to start the trial test ...</b>")
        continue_text.setAlignment(Qt.AlignCenter)
        continue_text.setStyleSheet("font-size: 18px; color: #333333; padding-top: 20px;")
        layout.addWidget(continue_text)

        # Spacer na dole
        layout.addSpacerItem(QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    def keyPressEvent(self, event):
        # Wywołanie funkcji `start_trial_callback` (czyli `start_trial_ant_test` z `AntInstructionWindow`)
        self.start_trial_callback()
