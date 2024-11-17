from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSpacerItem, QSizePolicy
from PySide6.QtGui import QPalette, QColor, QPixmap
from PySide6.QtCore import Qt

class ThirdView(QWidget):
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

        # Główna instrukcja
        instruction_text = QLabel(
            "<p style='font-size: 18px; text-align: center;'>Sometimes the central arrow will point in the opposite direction of the other arrows.</p>"
            "<p style='font-size: 16px; text-align: center;'>You should only pay attention to the central arrow!<br>"
            "For instance, the <b>[C]</b>-key is correct for this case:</p>"
        )
        instruction_text.setAlignment(Qt.AlignCenter)
        layout.addWidget(instruction_text)

        # Obrazek z przykładami
        example_image = QLabel()
        example_image.setPixmap(QPixmap("images/incompatible_left.png").scaled(300, 60, Qt.KeepAspectRatio))
        example_image.setAlignment(Qt.AlignCenter)
        layout.addWidget(example_image)

        example_text = QLabel("since the central arrow is pointing to the left.")
        example_text.setAlignment(Qt.AlignCenter)
        example_text.setStyleSheet("font-size: 16px;")
        layout.addWidget(example_text)

        # Tekst kontynuacji
        continue_text = QLabel("<b>Press a key to continue reading instructions ...</b>")
        continue_text.setAlignment(Qt.AlignCenter)
        continue_text.setStyleSheet("font-size: 18px; color: #333333; padding-top: 20px;")
        layout.addWidget(continue_text)

        # Spacer na dole
        layout.addSpacerItem(QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    def keyPressEvent(self, event):
        self.next_view_callback()
