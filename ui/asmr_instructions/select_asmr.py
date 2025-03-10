from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPalette, QColor


class IntroWindow(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        # Ustawienie ciemnego tła
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#2E2E2E"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Główny layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Usuń marginesy wokół layoutu
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)  # Wyśrodkowanie wszystkiego

        # Nagłówek
        header_label = QLabel("Witamy w segmenicie oceny wideo ASMR")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("color: white; font-weight: bold;")
        header_label.setFont(QFont("Arial", 22))
        layout.addWidget(header_label)

        # Treść instrukcji z użyciem HTML
        instructions = """
        <p style='font-size: 18px; color: #BBBBBB; text-align: center;'>
        <b>ASMR</b> (Autonomous Sensory Meridian Response) to relaksujące, przyjemne mrowienie,<br>
        które często jest wywoływane przez określone dźwięki, obrazy lub bodźce związane z osobistą uwagą.<br><br>
        W tym zadaniu zostaną Ci zaprezentowane <b>7 krótkich filmów ASMR</b>. Twoim celem jest ocena każdego<br>
        filmu na podstawie własnych preferencji. Weź pod uwagę następujące aspekty:<br>
        <ul style='text-align: left;'>
            <li>Jakość wizualna i dźwiękowa.</li>
            <li>Poziom przyjemności, jaką odczuwałeś podczas oglądania.</li>
        </ul>
        <br>
        Użyj skali ocen od <b>0</b> do <b>10</b>:<br>
        <b>0:</b> Zdecydowanie nie podobało się<br>
        <b>5:</b> Neutralne odczucia<br>
        <b>10:</b> Bardzo się podobało<br><br>
        Po ocenieniu wszystkich filmów przejdziesz do następnej fazy eksperymentu.<br><br>
        <b>Naciśnij dowolny klawisz, aby kontynuować.</b>
        </p>
        """
        instruction_label = QLabel()
        instruction_label.setTextFormat(Qt.TextFormat.RichText)  # Włączenie obsługi HTML
        instruction_label.setText(instructions)
        instruction_label.setAlignment(Qt.AlignCenter)
        instruction_label.setStyleSheet("color: white;")
        layout.addWidget(instruction_label)

        # Ustawienie layoutu
        self.setLayout(layout)

    def keyPressEvent(self, event):
        """Obsługa naciśnięcia klawisza."""
        self.main_app.show_asmr_select_window()
        self.close()
