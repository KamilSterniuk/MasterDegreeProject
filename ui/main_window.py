from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        # Ustawienia tła
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#2E2E2E"))  # Ciemnoszare tło
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(1)

        # Styl przycisków
        button_style = """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 18px;
                padding: 15px;
                border-radius: 10px;
                margin: 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """

        # Przycisk Start
        start_button = QPushButton("Start")
        start_button.setStyleSheet(button_style)
        start_button.clicked.connect(self.on_start)
        layout.addWidget(start_button)

        # Przycisk Settings
        settings_button = QPushButton("Settings")
        settings_button.setStyleSheet(button_style)
        settings_button.clicked.connect(self.on_settings)
        layout.addWidget(settings_button)

        # Przycisk Exit
        exit_button = QPushButton("Exit")
        exit_button.setStyleSheet("""
                    QPushButton {
                        background-color: #f44336;
                        color: white;
                        font-size: 18px;
                        padding: 15px;
                        border-radius: 10px;
                        margin: 20px;
                    }
                    QPushButton:hover {
                        background-color: #d32f2f;
                    }
                """)
        exit_button.clicked.connect(self.on_exit)
        layout.addWidget(exit_button)

        # Ustawienie layoutu
        self.setLayout(layout)

    def on_start(self):
        # Przejdź do ekranu ankiety
        self.main_app.show_start()

    def on_settings(self):
        # Przejdź do ekranu ustawień
        self.main_app.show_settings()

    def on_exit(self):
        # Zamyka aplikację
        self.main_app.close()
