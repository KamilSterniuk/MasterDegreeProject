from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSpacerItem, QSizePolicy
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt

class FirstView(QWidget):
    def __init__(self, next_view_callback):
        super().__init__()
        self.next_view_callback = next_view_callback

        # Wymuszenie tła za pomocą QPalette
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#C0C0C0"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self.setFocusPolicy(Qt.StrongFocus)

        layout = QVBoxLayout(self)

        # Spacer na górze
        layout.addSpacerItem(QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding))

        instruction_text = QLabel(
            "Before beginning the experiment\n"
            "please read the instructions carefully\n\n"
            "Press a key to continue reading instructions ..."
        )
        instruction_text.setAlignment(Qt.AlignCenter)
        instruction_text.setStyleSheet(
            "font-size: 22px; font-weight: bold; color: #333333; font-family: Arial; padding: 20px;"
        )
        layout.addWidget(instruction_text)

        # Spacer na dole
        layout.addSpacerItem(QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    def keyPressEvent(self, event):
        self.next_view_callback()
