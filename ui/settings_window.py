from PySide6.QtWidgets import QWidget, QVBoxLayout, QRadioButton, QPushButton
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt


class SettingsWindow(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        # Słownik tłumaczeń
        self.translations = {
            "en": {
                "control_group": "Control Group",
                "asmr_group": "ASMR Group",
                "back": "Back",
            },
            "pl": {
                "control_group": "Grupa kontrolna",
                "asmr_group": "Grupa ASMR",
                "back": "Powrót",
            },
        }

        # Ustawienia tła
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#2E2E2E"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Radio Button dla Control Group
        self.control_radio = QRadioButton()
        self.control_radio.setStyleSheet("color: white; font-size: 18px;")
        self.control_radio.setChecked(not self.main_app.asmr_enabled)  # Zaznaczone, jeśli ASMR jest wyłączony
        self.control_radio.toggled.connect(self.on_radio_changed)
        layout.addWidget(self.control_radio)

        # Radio Button dla ASMR Group
        self.asmr_radio = QRadioButton()
        self.asmr_radio.setStyleSheet("color: white; font-size: 18px;")
        self.asmr_radio.setChecked(self.main_app.asmr_enabled)  # Zaznaczone, jeśli ASMR jest włączony
        self.asmr_radio.toggled.connect(self.on_radio_changed)
        layout.addWidget(self.asmr_radio)

        # Przycisk Powrót
        self.back_button = QPushButton()
        self.back_button.setStyleSheet("""
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
        self.back_button.clicked.connect(self.on_back)
        layout.addWidget(self.back_button)

        # Ustawienie layoutu
        self.setLayout(layout)

        # Przetłumacz interfejs
        self.translate()

        # Debugging - wyświetlenie początkowego stanu
        print(f"Initial ASMR Mode state: {self.main_app.asmr_enabled}")

    def translate(self):
        """Tłumaczy wszystkie teksty w oknie."""
        current_translations = self.translations[self.main_app.language]
        self.control_radio.setText(current_translations["control_group"])
        self.asmr_radio.setText(current_translations["asmr_group"])
        self.back_button.setText(current_translations["back"])

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
