from PySide6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QPushButton
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

        # Checkbox ASMR
        self.asm_checkbox = QCheckBox("ASMR Mode")
        self.asm_checkbox.setTristate(False)  # Ustawienie checkboxa na dwustanowy
        self.asm_checkbox.setStyleSheet("color: white; font-size: 18px;")
        self.asm_checkbox.setChecked(self.main_app.asmr_enabled)
        self.asm_checkbox.stateChanged.connect(self.on_checkbox_changed)
        layout.addWidget(self.asm_checkbox)

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

    def on_checkbox_changed(self, state):
        # Użycie isChecked() zamiast state
        self.main_app.asmr_enabled = self.asm_checkbox.isChecked()
        print(f"Checkbox isChecked: {self.asm_checkbox.isChecked()}, ASMR Mode updated to: {self.main_app.asmr_enabled}")

    def on_back(self):
        # Powrót do ekranu głównego
        self.main_app.show_main()
