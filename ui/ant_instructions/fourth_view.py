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

        instruction_text = QLabel("Na środku ekranu pojawi się krzyż:")
        instruction_text.setAlignment(Qt.AlignCenter)
        instruction_text.setStyleSheet("font-size: 18px; color: #333333; padding-bottom: 10px;")
        layout.addWidget(instruction_text)

        # Obrazek z krzyżem
        cross_image = QLabel()
        cross_image.setPixmap(QPixmap("images/plus.png").scaled(40, 40, Qt.KeepAspectRatio))
        cross_image.setAlignment(Qt.AlignCenter)
        layout.addWidget(cross_image)

        bottom_text = QLabel(
            "Strzałki pojawią się powyżej lub poniżej krzyża.<br><br>"
            "Powinieneś skupić wzrok na tym krzyżu<br>"
            "przez cały czas trwania eksperymentu.<br><br>"
            "<b>Naciśnij klawisz, aby kontynuować czytanie instrukcji ...</b>"
        )
        bottom_text.setAlignment(Qt.AlignCenter)
        bottom_text.setStyleSheet("font-size: 18px; color: #333333;")
        layout.addWidget(bottom_text)

        # Spacer na dole
        layout.addSpacerItem(QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    def keyPressEvent(self, event):
        self.next_view_callback()
