from PySide6.QtWidgets import QWidget, QVBoxLayout, QRadioButton, QPushButton
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt

class SettingsWindow(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        # Ustawienia tła
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#2E2E2E"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Radio Button dla Control Group
        self.control_radio = QRadioButton("Control Group")
        self.control_radio.setStyleSheet("color: white; font-size: 18px;")
        self.control_radio.setChecked(not self.main_app.asmr_enabled)  # Zaznaczone, jeśli ASMR jest wyłączony
        self.control_radio.toggled.connect(self.on_radio_changed)
        layout.addWidget(self.control_radio)

        # Radio Button dla ASMR Group
        self.asmr_radio = QRadioButton("ASMR Group")
        self.asmr_radio.setStyleSheet("color: white; font-size: 18px;")
        self.asmr_radio.setChecked(self.main_app.asmr_enabled)  # Zaznaczone, jeśli ASMR jest włączony
        self.asmr_radio.toggled.connect(self.on_radio_changed)
        layout.addWidget(self.asmr_radio)

        # Przycisk Powrót
        back_button = QPushButton("Back")
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-size: 18px;
                padding: 15px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        back_button.clicked.connect(self.on_back)
        layout.addWidget(back_button)

        # Ustawienie layoutu
        self.setLayout(layout)

        # Debugging - wyświetlenie początkowego stanu
        print(f"Initial ASMR Mode state: {self.main_app.asmr_enabled}")

    def on_radio_changed(self):
        # Aktualizacja stanu na podstawie wybranego radio buttona
        if self.control_radio.isChecked():
            self.main_app.asmr_enabled = False
        elif self.asmr_radio.isChecked():
            self.main_app.asmr_enabled = True
        print(f"ASMR Mode updated to: {self.main_app.asmr_enabled}")

    def on_back(self):
        # Powrót do ekranu głównego
        self.main_app.show_main()