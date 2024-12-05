from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor

class MisophoniaFailWindow(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        # Ustawienia okna
        self.setWindowTitle("Misophonia Exclusion")
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#2E2E2E"))  # Ciemnoszare tło
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Główny layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # Tytuł
        title_label = QLabel("Exclusion Notice")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white; padding: 15px;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Treść
        content_label = QLabel(
            "Unfortunately, you cannot participate in this study because your sensitivity level "
            "to trigger sounds is too high.\n\nThank you for your interest."
        )
        content_label.setStyleSheet("font-size: 16px; color: #BBBBBB; padding: 15px;")
        content_label.setAlignment(Qt.AlignCenter)
        content_label.setWordWrap(True)
        main_layout.addWidget(content_label)

        # Przycisk zamykający
        close_button = QPushButton("Close")
        close_button.setStyleSheet("""
                    QPushButton {
                        background-color: #f44336;
                        color: white;
                        font-size: 16px;
                        padding: 10px 20px;
                        border-radius: 8px;
                    }
                    QPushButton:hover {
                        background-color: #d32f2f;
                    }
                """)
        close_button.clicked.connect(self.close_application)
        main_layout.addWidget(close_button)

        self.setLayout(main_layout)

    def close_application(self):
        """Zamyka aplikację."""
        self.main_app.show_main()
