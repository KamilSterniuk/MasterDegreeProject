from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPalette, QColor, Qt


class AsmrSelectWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Ustawienia ciemnego tła
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#2E2E2E"))  # Ciemnoszare tło
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Główny layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Tekst nagłówka
        label = QLabel("This is the ASMR Select Window")
        label.setStyleSheet("font-size: 24px; font-weight: bold; color: white; padding: 20px;")
        label.setAlignment(Qt.AlignCenter)

        # Dodanie nagłówka do layoutu
        layout.addWidget(label)
        self.setLayout(layout)
