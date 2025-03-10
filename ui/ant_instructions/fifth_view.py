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
            "<h1 style='text-align: center;'>Przygotuj się</h1>"
            "<p style='font-size: 18px; text-align: center;'>Zaraz wykonasz próbny test ANT,<br>"
            "aby zapoznać się z zadaniem.</p>"
            "<p style='font-size: 16px; text-align: center;'>Proszę uważnie śledzić polecenia,<br>"
            "ponieważ pomoże to w przygotowaniu do właściwego testu.</p>"
        )
        instruction_text.setAlignment(Qt.AlignCenter)
        layout.addWidget(instruction_text)

        # Tekst kontynuacji
        continue_text = QLabel("<b>Naciśnij dowolny klawisz, aby rozpocząć próbny test ...</b>")
        continue_text.setAlignment(Qt.AlignCenter)
        continue_text.setStyleSheet("font-size: 18px; color: #333333; padding-top: 20px;")
        layout.addWidget(continue_text)

        # Spacer na dole
        layout.addSpacerItem(QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    def keyPressEvent(self, event):
        # Wywołanie funkcji `start_trial_callback` (czyli `start_trial_ant_test` z `AntInstructionWindow`)
        self.start_trial_callback()
