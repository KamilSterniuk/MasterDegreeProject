from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


class StaiInstructionWindow(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        # Ustawienie ciemnego tła
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#2E2E2E"))  # Ciemnoszare tło
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Główny layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # Tytuł
        title_label = QLabel("Instrukcje do Kwestionariusza STAI")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: white; padding: 20px;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Instrukcja
        instructions_label = QLabel()
        instructions_label.setTextFormat(Qt.TextFormat.RichText)  # Użycie HTML dla formatowania
        instructions_label.setText(
            "<p style='font-size: 20px; color: #BBBBBB; text-align: center;'>"
            "<b>State-Trait Anxiety Inventory (STAI)</b> to kwestionariusz samooceny zaprojektowany do oceny tego, "
            "jak się czujesz w danym momencie.<br><br>"
            "Odpowiesz na <b>20 pytań</b> dotyczących Twojego aktualnego samopoczucia. "
            "Dla każdego pytania wybierz odpowiedź, która najlepiej opisuje Twoje doświadczenie, korzystając z poniższej skali:<br>"
            "<ul style='text-align: left;'>"
            "<li><b>1:</b> Wcale</li>"
            "<li><b>2:</b> Trochę</li>"
            "<li><b>3:</b> Umiarkowanie</li>"
            "<li><b>4:</b> Bardzo</li>"
            "</ul>"
            "Prosimy o udzielanie szczerych odpowiedzi, aby zapewnić dokładność wyników.<br><br>"
            "<b>Naciśnij dowolny klawisz, aby przejść do kwestionariusza.</b>"
            "</p>"
        )
        instructions_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(instructions_label)

        self.setLayout(main_layout)

    def keyPressEvent(self, event):
        """Przechodzenie do widoku STAI po naciśnięciu dowolnego klawisza."""
        self.main_app.show_stai()
