from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QSpacerItem, QSizePolicy, QHBoxLayout
from PySide6.QtGui import QPalette, QColor, QPixmap
from PySide6.QtCore import Qt

class SecondView(QWidget):
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
            "<h1 style='text-align: center;'>Instruction</h1>"
            "<p style='font-size: 18px; text-align: center;'>Na środku ekranu pojawi się zestaw pięciu strzałek.<br>"
            "Twoim zadaniem jest określenie, w którą stronę wskazuje środkowa strzałka.</p>"
            "<p style='font-size: 20px; text-align: center; font-weight: bold;'>"
            "[←] jeśli środkowa strzałka wskazuje na <b>LEWO</b><br>"
            "[→] jeśli środkowa strzałka wskazuje na <b>PRAWO</b></p>"
        )
        instruction_text.setAlignment(Qt.AlignCenter)
        layout.addWidget(instruction_text)

        # Pierwszy zestaw strzałek (LEWY)
        example_left = QLabel()
        example_left.setPixmap(QPixmap("images/compatible_left.png").scaled(300, 60, Qt.KeepAspectRatio))
        example_left.setAlignment(Qt.AlignCenter)
        layout.addWidget(example_left)

        example_left_text = QLabel("Powinieneś nacisnąć klawisz <b>[←]</b> w powyższym przykładzie")
        example_left_text.setAlignment(Qt.AlignCenter)
        example_left_text.setStyleSheet("font-size: 16px;")
        layout.addWidget(example_left_text)

        # Drugi zestaw strzałek (PRAWY)
        example_right = QLabel()
        example_right.setPixmap(QPixmap("images/compatible_right.png").scaled(300, 60, Qt.KeepAspectRatio))
        example_right.setAlignment(Qt.AlignCenter)
        layout.addWidget(example_right)

        example_right_text = QLabel("a w tym przykładzie powinieneś nacisnąć klawisz <b>[→]</b>.")
        example_right_text.setAlignment(Qt.AlignCenter)
        example_right_text.setStyleSheet("font-size: 16px;")
        layout.addWidget(example_right_text)

        # Tekst kontynuacji
        continue_text = QLabel("<b>Naciśnij klawisz, aby kontynuować czytanie instrukcji ...</b>")
        continue_text.setAlignment(Qt.AlignCenter)
        continue_text.setStyleSheet("font-size: 18px; color: #333333; padding-top: 20px;")
        layout.addWidget(continue_text)

        # Spacer na dole
        layout.addSpacerItem(QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    def keyPressEvent(self, event):
        self.next_view_callback()
