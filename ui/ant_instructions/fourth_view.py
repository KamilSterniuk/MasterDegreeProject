from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSpacerItem, QSizePolicy
from PySide6.QtGui import QPalette, QColor, QPixmap
from PySide6.QtCore import Qt

class FourthView(QWidget):
    def __init__(self, next_view_callback):
        super().__init__()
        self.next_view_callback = next_view_callback

        # Ustawienie tła
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#C0C0C0"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        layout = QVBoxLayout(self)

        # Spacer na górze
        layout.addSpacerItem(QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding))

        instruction_text = QLabel("In the center of the screen a cross will appear")
        instruction_text.setAlignment(Qt.AlignCenter)
        instruction_text.setStyleSheet("font-size: 18px; color: #333333; padding-bottom: 10px;")
        layout.addWidget(instruction_text)

        # Obrazek z krzyżem
        cross_image = QLabel()
        cross_image.setPixmap(QPixmap("images/plus.png").scaled(60, 60, Qt.KeepAspectRatio))
        cross_image.setAlignment(Qt.AlignCenter)
        layout.addWidget(cross_image)

        bottom_text = QLabel(
            "The arrows will appear above or below the cross.<br><br>"
            "You should fix your gaze on this cross<br>"
            "throughout the entire experiment.<br><br>"
            "<b>Press a key to continue reading instructions ...</b>"
        )
        bottom_text.setAlignment(Qt.AlignCenter)
        bottom_text.setStyleSheet("font-size: 18px; color: #333333;")
        layout.addWidget(bottom_text)

        # Spacer na dole
        layout.addSpacerItem(QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    def keyPressEvent(self, event):
        self.next_view_callback()
