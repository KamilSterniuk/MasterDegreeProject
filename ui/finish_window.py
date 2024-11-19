from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


class EndOfStudyWindow(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        # Layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#2E2E2E"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Thank you message
        message_label = QLabel("Thank you for participating in the study!\nThis is the end of the test.")
        message_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white; padding: 20px;")
        message_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(message_label)

        # Instruction to continue
        continue_label = QLabel("Press any key to end...")
        continue_label.setStyleSheet("font-size: 18px; color: #BBBBBB; padding: 10px;")
        continue_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(continue_label)

        self.setLayout(layout)

    def keyPressEvent(self, event):
        """Handles key press events to return to the main menu."""
        self.main_app.show_main()